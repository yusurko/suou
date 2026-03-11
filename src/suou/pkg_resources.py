"""
Drop-in replacement for pkg_resources (kind of), using importlib.resources.

*New in 0.12.3*

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""


from importlib.resources import files

def resource_filename(package_name, resource_name: str) -> str:
    """
    Backport of resource_filename() from pkg_resources, using importlib.resources
    """
    return str(files(package_name) / resource_name)


__all__ = (
    'resource_filename',
)