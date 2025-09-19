"""
Colors for coding artists

NEW 0.7.0

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

"""


from functools import lru_cache


class Chalk:
    """
    ANSI escape codes for terminal colors, similar to JavaScript's `chalk` library.

    Best used with Python 3.12+ that allows arbitrary nesting of f-strings.

    Yes, I am aware colorama exists.

    UNTESTED

    NEW 0.7.0
    """
    CSI = '\x1b['
    RED = CSI + "31m"
    GREEN = CSI + "32m"
    YELLOW = CSI + "33m"
    BLUE = CSI + "34m"
    CYAN = CSI + "36m"
    PURPLE = CSI + "35m" 
    GREY = CSI + "90m"
    END_COLOR = CSI + "39m"
    BOLD = CSI + "1m"
    END_BOLD = CSI + "22m"
    FAINT = CSI + "2m"
    def __init__(self, flags = (), ends = ()):
        self._flags = tuple(flags)
        self._ends = tuple(ends)
    @lru_cache()
    def _wrap(self, beg, end):
        return Chalk(self._flags + (beg,), self._ends + (end,))
    def __call__(self, s: str) -> str:
        return ''.join(self._flags) + s + ''.join(reversed(self._ends))
    def red(self):
        return self._wrap(self.RED, self.END_COLOR)
    def green(self):
        return self._wrap(self.GREEN, self.END_COLOR)
    def blue(self):
        return self._wrap(self.BLUE, self.END_COLOR)
    def yellow(self):
        return self._wrap(self.YELLOW, self.END_COLOR)
    def cyan(self):
        return self._wrap(self.CYAN, self.END_COLOR)
    def purple(self):
        return self._wrap(self.PURPLE, self.END_COLOR)
    def grey(self):
        return self._wrap(self.GREY, self.END_COLOR)
    gray = grey
    marine = blue
    def bold(self):
        return self._wrap(self.BOLD, self.END_BOLD)
    def faint(self):
        return self._wrap(self.FAINT, self.END_BOLD)


## TODO make it lazy?
chalk = Chalk()
