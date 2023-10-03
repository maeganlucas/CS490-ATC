# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# insert source code path into system path. this keeps documentation and code directories
# separate, but still allows us to automatically generate source documentation (autodoc/auto*)
sys.path.insert(0, os.path.abspath("../../source"))

project = "ASR Webapp Demo"
copyright = "2023, Aaron Van De Brook"
author = "Aaron Van De Brook"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx_js",
]

templates_path = ["_templates"]

autodoc_mock_imports = ["flask", "pandas", "opensky_api"]

exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

html_static_path = ["_static"]

autoclass_content = "both"

js_source_path = "../../source/static/js"
