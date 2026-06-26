"""
Experimental AST module

---

Copyright (c) 2026 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from __future__ import annotations
from ast import TypeVar
from typing import Any, Collection

_T = TypeVar('_T')

class Node:
    __slots__ = ('_children', )

    _count: int
    _children: list[Node]
    _types: Collection[type]

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(repr(x) for x in self._children)})"

    def __init__(self, *args):
        if self._count != len(args):
            raise TypeError(f'{self.__class__.__name__} must be instanced with {self._count} arguments, got {len(args)}')

        for i, (a, t) in enumerate(zip(args, self._types)):
            if t != Any and not isinstance(a, t):
                raise TypeError(f"argument {i} must be of type {t.__name__!r}, got {a.__class__.__name__!r}")

        self._children = list(args)

    def eval(self, ctx: dict):
        raise TypeError(f'{self.__class__.__name__} cannot be eval()ed')

    def __getitem__(self, key: int):
        if key >= self._count:
            raise IndexError('child node index out of range')
        return self._children[key]

    def __len__(self):
        return self._count


class ZeroOp(Node):
    _count = 0
    _types = ()


class UnaryOp(Node):
    _count = 1
    _types = (Any,)
    

class BinaryOp(Node):
    _count = 2
    _types = (Any, Any)


class TernaryOp(Node):
    _count = 3
    _types = (Any, Any, Any)


class MultiOp(Node):
    _count = 1
    _types = (list,)

    def __getitem__(self, key: int):
        return self._children[0][key]

    def __iter__(self):
        return iter(self._children[0])

    def __len__(self):
        return len(self._children[0])



class Literal(UnaryOp):
    """A literal evals to the enclosed value."""
    def eval(self, ctx: dict):
        return self[0]


## SUOU provides some ready-made literals, for the sake of ease-of-use.

class IntLiteral(Literal):
    _types = (int,)

class FloatLiteral(Literal):
    """
    WARNING: may be subject to loss of precision.
    """
    _types = (float,)

class StringLiteral(Literal):
    _types = (str,)


# This module is experimental and therefore not re-exported into __init__
__all__ = (
    'Node', 'ZeroOp', 'UnaryOp', 'BinaryOp', 'TernaryOp',
    'MultiOp', 'Literal', 'IntLiteral', 'FloatLiteral',
    'StringLiteral'
)