"""
Function utilities (decorators et al.).

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import math
import time
from typing import Callable, TypeVar
import warnings
from functools import wraps, lru_cache

_T = TypeVar('_T')
_U = TypeVar('_U')

try:
    from warnings import deprecated
except ImportError:
    # Python <=3.12 does not implement warnings.deprecated
    def deprecated(message: str, /, *, category=DeprecationWarning, stacklevel: int = 1) -> Callable[[Callable[_T, _U]], Callable[_T, _U]]:
        """
        Backport of PEP 702 for Python <=3.12.
        The stack_level stuff is not reimplemented on purpose because
        too obscure for the average programmer.
        """
        def decorator(func: Callable[_T, _U]) -> Callable[_T, _U]:
            @wraps(func)
            def wrapper(*a, **ka):
                if category is not None:
                    warnings.warn(message, category, stacklevel=stacklevel)
                return func(*a, **ka)
            func.__deprecated__ = True
            wrapper.__deprecated__ = True
            return wrapper
        return decorator

## this syntactic sugar for deprecated() is ... deprecated, which is ironic.
## Needed move because VSCode seems to not sense deprecated_alias()es as deprecated.
@deprecated('use deprecated(message)(func) instead')
def deprecated_alias(func: Callable, /, message='use .{name}() instead', *, category=DeprecationWarning) -> Callable:
    """
    Syntactic sugar helper for renaming functions.

    DEPRECATED use deprecated(message)(func) instead
    """
    return deprecated(message.format(name=func.__name__), category=category)(func)

def not_implemented(msg: Callable | str | None = None):
    """
    A more elegant way to say a method is not implemented, but may get in the future.
    """
    def decorator(func: Callable) -> Callable:
        da_msg = msg if isinstance(msg, str) else 'method {name}() is not implemented'.format(name=func.__name__)
        @wraps(func)
        def wrapper(*a, **k):
            raise NotImplementedError(da_msg)
        return wrapper
    if callable(msg):
        return decorator(msg)
    return decorator


def timed_cache(ttl: int, maxsize: int = 128, typed: bool = False) -> Callable[[Callable], Callable]:
    """
    LRU cache which expires after the TTL in seconds passed as argument.
    
    NEW 0.5.0
    """
    def decorator(func):
        start_time = None

        @lru_cache(maxsize, typed)
        def inner_wrapper(ttl_period: int, *a, **k):
            return func(*a, **k)

        @wraps(func)
        def wrapper(*a, **k):
            nonlocal start_time
            if not start_time:
                start_time = int(time.time())
            return inner_wrapper(math.floor((time.time() - start_time) // ttl), *a, **k)
        return wrapper
    return decorator

def none_pass(func: Callable, *args, **kwargs) -> Callable:
    """
    Wrap callable so that gets called only on not None values.

    Shorthand for func(x) if x is not None else None

    NEW 0.5.0
    """
    @wraps(func)
    def wrapper(x):
        if x is None:
            return x
        return func(x, *args, **kwargs)
    return wrapper

__all__ = (
    'deprecated', 'not_implemented', 'timed_cache', 'none_pass'
)