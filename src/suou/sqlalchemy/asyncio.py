
"""
Helpers for asynchronous use of SQLAlchemy.

NEW 0.5.0; moved to current location 0.6.0

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from __future__ import annotations
from functools import wraps


from sqlalchemy import Engine, Select, Table, func, select
from sqlalchemy.orm import DeclarativeBase, lazyload
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from flask_sqlalchemy.pagination import Pagination

from suou.exceptions import NotFoundError

class SQLAlchemy:
    """
    Drop-in (in fact, almost) replacement for flask_sqlalchemy.SQLAlchemy()
    eligible for async environments.

    Notable changes:
    + You have to create the session yourself. Easiest use case:

    async def handler (userid):
        async with db as session:
            # do something
            user = (await session.execute(select(User).where(User.id == userid))).scalar()
            # ...

    NEW 0.5.0

    UPDATED 0.6.0: added wrap=True
    """
    base: DeclarativeBase
    engine: AsyncEngine
    _sessions: list[AsyncSession]
    _wrapsessions: bool
    NotFound = NotFoundError

    def __init__(self, model_class: DeclarativeBase, *, wrap = False):
        self.base = model_class
        self.engine = None
        self._wrapsessions = wrap
        self._sessions = []
    def bind(self, url: str):
        self.engine = create_async_engine(url)
    def _ensure_engine(self):
        if self.engine is None:
            raise RuntimeError('database is not connected')
    async def begin(self, *, expire_on_commit = False, wrap = False, **kw) -> AsyncSession:
        self._ensure_engine()
        ## XXX is it accurate?
        s = AsyncSession(self.engine, expire_on_commit=expire_on_commit, **kw)
        if wrap:
            s = SessionWrapper(s)
        self._sessions.append(s)
        return s
    async def __aenter__(self) -> AsyncSession:
        return await self.begin()
    async def __aexit__(self, e1, e2, e3):
        ## XXX is it accurate?
        s = self._sessions.pop()
        if e1:
            await s.rollback()
        else:
            await s.commit()
        await s.close()
    async def paginate(self, select: Select, *, 
        page: int | None = None, per_page: int | None = None,
        max_per_page: int | None = None, error_out: bool = True,
        count: bool = True) -> AsyncSelectPagination:
        """
        Return a pagination. Analogous to flask_sqlalchemy.SQLAlchemy.paginate().
        """
        async with self as session:
            return AsyncSelectPagination(
                select = select,
                session = session,
                page = page,
                per_page=per_page, max_per_page=max_per_page,
                error_out=self.NotFound if error_out else None, count=count
            )
    async def create_all(self, *, checkfirst = True):
        """
        Initialize database
        """
        self._ensure_engine()
        self.base.metadata.create_all(
            self.engine, checkfirst=checkfirst
        )



class AsyncSelectPagination(Pagination):
    """
    flask_sqlalchemy.SelectPagination but asynchronous.

    Pagination is not part of the public API, therefore expect that it may break
    """

    async def _query_items(self) -> list:
        select_q: Select = self._query_args["select"]
        select = select_q.limit(self.per_page).offset(self._query_offset)
        session: AsyncSession = self._query_args["session"]
        out = (await session.execute(select)).scalars()
        return out

    async def _query_count(self) -> int:
        select_q: Select = self._query_args["select"]
        sub = select_q.options(lazyload("*")).order_by(None).subquery()
        session: AsyncSession = self._query_args["session"]
        out = (await session.execute(select(func.count()).select_from(sub))).scalar()
        return out

    def __init__(self,
        page: int | None = None,
        per_page: int | None = None,
        max_per_page: int | None = 100,
        error_out: Exception | None = NotFoundError,
        count: bool = True,
        **kwargs):
        ## XXX flask-sqlalchemy says Pagination() is not public API.
        ## Things may break; beware.
        self._query_args = kwargs
        page, per_page = self._prepare_page_args(
            page=page,
            per_page=per_page,
            max_per_page=max_per_page,
            error_out=error_out,
        )

        self.page: int = page
        """The current page."""

        self.per_page: int = per_page
        """The maximum number of items on a page."""

        self.max_per_page: int | None = max_per_page
        """The maximum allowed value for ``per_page``."""

        self.items = None
        self.total = None
        self.error_out = error_out
        self.has_count = count

    async def __aiter__(self):
        self.items = await self._query_items()
        if self.items is None:
            raise RuntimeError('query returned None')
        if not self.items and self.page != 1 and self.error_out:
            raise self.error_out
        if self.has_count:
            self.total = await self._query_count()
        for i in self.items:
            yield i


def async_query(db: SQLAlchemy, multi: False):
    """
    Wraps a query returning function into an executor coroutine.

    The query function remains available as the .q or .query attribute.
    """
    def decorator(func):
        @wraps(func)
        async def executor(*args, **kwargs):
            async with db as session:
                result = await session.execute(func(*args, **kwargs))
                return result.scalars() if multi else result.scalar()
        executor.query = executor.q = func
        return executor
    return decorator
        
class SessionWrapper:
    """
    Wrap a SQLAlchemy() session (context manager) adding several QoL utilitites.

    It can be applied to:
    + sessions created by SQLAlchemy() - it must receive a wrap=True argument in constructor;
    + sessions created manually - by constructing SessionWrapper(session).

    This works in async context; DO NOT USE with regular SQLAlchemy.

    NEW 0.6.0
    """

    def __init__(self, db_or_session: SQLAlchemy | AsyncSession):
        self._wrapped = db_or_session
    async def __aenter__(self):
        if isinstance(self._wrapped, SQLAlchemy):
            self._wrapped = await self._wrapped.begin()
        return self
    
    async def __aexit__(self, *exc_info):
        await self._wrapped.__aexit__(*exc_info)

    @property
    def _session(self):
        if isinstance(self._wrapped, AsyncSession):
            return self._wrapped
        raise RuntimeError('active session is required')
    
    async def get_one(self, query: Select):
        result = await self._session.execute(query)
        return result.scalar()

    async def get_by_id(self, table: Table, key) :
        return await self.get_one(select(table).where(table.id == key))  # pyright: ignore[reportAttributeAccessIssue]

    async def get_list(self, query: Select, limit: int | None = None):
        if limit:
            query = query.limit(limit)
        result = await self._session.execute(query)
        return list(result.scalars())

    def __getattr__(self, key):
        """
        Fall back to the wrapped session
        """
        return getattr(self._session, key)

# Optional dependency: do not import into __init__.py
__all__ = ('SQLAlchemy', 'AsyncSelectPagination', 'async_query', 'SessionWrapper')