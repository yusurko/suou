"""
The SUOU (SIS Unified Object Underarmor) library's entry point.

See README.md for a description.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from .iding import Siq, SiqCache, SiqType, SiqGen
from .codecs import StringCase
from .configparse import MissingConfigError, MissingConfigWarning, ConfigOptions, ConfigParserConfigSource, ConfigSource, ConfigValue, EnvConfigSource
from .functools import deprecated, not_implemented
from .classtools import Wanted, Incomplete
from .itertools import makelist, kwargs_prefix
from .i18n import I18n, JsonI18n, TomlI18n

__version__ = "0.2.0-dev21"

__all__ = (
    'Siq', 'SiqCache', 'SiqType', 'SiqGen', 'StringCase',
    'MissingConfigError', 'MissingConfigWarning', 'ConfigOptions', 'ConfigParserConfigSource', 'ConfigSource', 'ConfigValue', 'EnvConfigSource',
    'deprecated', 'not_implemented', 'Wanted', 'Incomplete',
    'makelist', 'kwargs_prefix', 'I18n', 'JsonI18n', 'TomlI18n'
)
