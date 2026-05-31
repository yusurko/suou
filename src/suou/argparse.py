"""
Utilities for parsing arguments. Based on argparse.

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

import argparse
import sys
from typing import Callable

class LetterSubparsers(object):
    """
    Subparsers in pacman style, where action name can be shortened to a single letter, prefixed by a hyphen

    (i.e. "-S" is expanded to "sync")

    *New in 0.13.0*
    """

    _parser: argparse.ArgumentParser
    _letters: dict[str, str]
    _subparsers: argparse._SubParsersAction[argparse.ArgumentParser]

    def __init__(self, parser : argparse.ArgumentParser, *, dest: str = 'action', **kwargs):
        self._parser = parser
        self._letters = {}
        self._subparsers = parser.add_subparsers(dest = dest, **kwargs)

    def action(self, /, letter: str, name: str | None = None, **kwargs):
        """
        Decorator which adds a subparser of an argument parser's subparsers, and specifies a letter to make a shorthand in pacman style.

        For example, assuming name="sync" and letter="S", if the first argument is "-S", it will be turned to "sync", .

        The first argument is always the object returned by ArgumentParser.add_subparsers().

        Additional kwargs are passed to the add_parser constructor.
        """

        if len(letter) != 1:
            raise ValueError('letter must be one character')

        o_name = name

        def decorator(func: Callable[argparse.ArgumentParser, ...]):
            name = o_name or func.__name__
            parser = self._subparsers.add_parser(name, **kwargs)
            func(parser)

            self._letters[letter] = name

            return func
        return decorator

    def parse_args(self, argv = None, system_exit: bool = True):
        """
        Variation of ArgumentParser.parse_args() that takes shortcut letters into account.

        Best used together with letter_action().
        """
        
        if argv is None:
            argv = sys.argv[1:]
        else:
            argv = list(argv)

        if len(argv) > 0:
            first_arg = argv.pop(0)

            if first_arg.startswith('-') and len(first_arg) >= 2:
                letter, rest = first_arg[1], first_arg[2:]
                if letter in self._letters:
                    argv.insert(0, self._letters[letter])
                    if rest:
                        argv.insert(1, "-" + rest)
                else:
                    # put it back
                    argv.insert(0, first_arg)
            else:
                # put it back
                argv.insert(0, first_arg)

        try:
            return self._parser.parse_args(argv)
        except SystemExit:
            # prevent SystemExit at parse fail
            if system_exit:
                raise


__all__ = ('LetterSubparsers',)

