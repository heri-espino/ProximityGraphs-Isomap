"""Sphinx build settings for source-generated Python API documentation."""

project = "ProximityGraphs-Isomap"
author = "Research contributors"
release = "0.1.0"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "myst_parser"]
html_theme = "furo"
exclude_patterns = ["_build"]
autodoc_typehints = "description"
autodoc_member_order = "bysource"
napoleon_numpy_docstring = True
napoleon_google_docstring = False
