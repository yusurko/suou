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
    _has_verbose: bool = False

    def __init__(self, parser : argparse.ArgumentParser, *, dest: str = 'action', **kwargs):
        self._parser = parser
        self._letters = {}
        self._subparsers = parser.add_subparsers(dest = dest, **kwargs)

    def add_verbose(self, *, help: str = "show more logs (e.g. debug)"):
        """
        Add a "-v" / "--verbose" argument to the main parser.

        This allows the argument to be everywhere in the argv.
        """
        self._parser.add_argument('-v', '--verbose', action='count', default = 0, help=help)
        self._has_verbose = True

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

    def parse_args(self, argv: list[str] = None, system_exit: bool = True):
        """
        Variation of ArgumentParser.parse_args() that takes shortcut letters into account.

        Best used together with .action().
        """
        
        if argv is None:
            argv = sys.argv[1:]
        else:
            argv = list(argv)

        opt_start = 0

        # preprocess the letters
        if len(argv) > 0:
            first_arg = argv.pop(0)
            
            if first_arg.startswith('-') and len(first_arg) >= 2:
                for idx, letter in enumerate(first_arg):
                    rest = first_arg[1:idx] + first_arg[idx+1:]
                    if letter in self._letters:
                        argv.insert(0, self._letters[letter])
                        if rest:
                            argv.insert(1, "-" + rest)
                        opt_start = 1
                        break
                else:
                    # put it back
                    argv.insert(0, first_arg)
            else:
                # put it back
                argv.insert(0, first_arg)

        # preprocess the verbose
        if self._has_verbose and len(argv) > opt_start:
            nargv = argv[:opt_start]
            vc = 0
            for arg in argv[opt_start:]:
                if arg.startswith('-') and not arg.startswith('--'):
                    arg_vc = sum(1 for l in arg[1:] if l == 'v')
                    arg_vless = arg.replace('v', '')
                    if arg_vless != '-':
                        nargv.append(arg_vless)
                    vc += arg_vc
                elif arg == '--verbose':
                    vc += 1
                else:
                    nargv.append(arg)
            argv = ["--verbose"] * vc + nargv
        
        try:
            args = self._parser.parse_args(argv)
        except SystemExit:
            # prevent SystemExit at parse fail
            if system_exit:
                raise
        else:
            return args


__all__ = ('LetterSubparsers',)

