# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys 
from pathlib import Path

sys.path.insert(0, str(Path("..", "src").resolve()))

project = 'suou'
copyright = '2025 Sakuragasaki46'
author = 'Sakuragasaki46'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc", 
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_mock_imports = [
    "toml",
    "starlette",
    "itsdangerous",
    "pydantic",
    "quart_schema"
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_path = ["_themes", ]
html_static_path = ['_static']

def polish_module_docstring(app, what, name, obj, options, lines):
    if what == "module" and 'members' in options:
        try:
            del lines[lines.index('---'):]
        except Exception:
            pass

def setup(app):
    app.connect("autodoc-process-docstring", polish_module_docstring)