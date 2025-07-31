"""
Helpers for asynchronous user of SQLAlchemy

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from sqlalchemy import Engine, Select, func, select
from sqlalchemy.orm import DeclarativeBase, Session, lazyload
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from flask_sqlalchemy.pagination import Pagination

from suou.exceptions import NotFoundError

class SQLAlchemy:
    """
    Drop-in (?) replacement for flask_sqlalchemy.SQLAlchemy()
    eligible for async environments

    NEW 0.5.0
    """
    base: DeclarativeBase
    engine: Engine
    NotFound = NotFoundError

    def __init__(self, model_class: DeclarativeBase):
        self.base = model_class
        self.engine = None
    def bind(self, url: str):
        self.engine = create_async_engine(url)
    async def begin(self) -> Session:
        if self.engine is None:
            raise RuntimeError('database is not connected')
        return await self.engine.begin()
    __aenter__ = begin
    async def __aexit__(self, e1, e2, e3):
        return await self.engine.__aexit__(e1, e2, e3)
    async def paginate(self, select: Select, *, 
        page: int | None = None, per_page: int | None = None,
        max_per_page: int | None = None, error_out: bool = True,
        count: bool = True):
        """
        """
        async with self as session:
            return AsyncSelectPagination(
                select = select,
                session = session,
                page = page,
                per_page=per_page, max_per_page=max_per_page,
                error_out=self.NotFound if error_out else None, count=count
            )



class AsyncSelectPagination(Pagination):
    """
    flask_sqlalchemy.SelectPagination but asynchronous
    """

    async def _query_items(self) -> list:
        select_q: Select = self._query_args["select"]
        select = select_q.limit(self.per_page).offset(self._query_offset)
        session: AsyncSession = self._query_args["session"]
        out = (await session.execute(select)).scalars()

    async def _query_count(self) -> int:
        select_q: Select = self._query_args["select"]
        sub = select_q.options(lazyload("*")).order_by(None).subquery()
        session: AsyncSession = self._query_args["session"]
        out = await session.execute(select(func.count()).select_from(sub))
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

    async def __await__(self):
        self.items = await self._query_items()
        if not self.items and self.page != 1 and self.error_out:
            raise self.error_out
        if self.has_count:
            self.total = await self._query_count()
        return self

__all__ = ('SQLAlchemy', )