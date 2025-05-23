"""
Utilities for Flask

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from flask import Flask
from .configparse import ConfigOptions


def add_context_from_config(app: Flask, config: ConfigOptions) -> Flask:
    '''
    Add a ConfigOptions() object's public properties into a Flask app's context
    (i.e. variables available in templates).
    '''
    @app.context_processor
    def _add_context():
        return config.to_dict()
    return app

__all__ = ('add_context_from_config', )


