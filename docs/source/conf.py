# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'codix'
copyright = '2025, L. Pezard'
author = 'L. Pezard'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sys
sys.path.append('../src/')
#sys.path.append('../../src/encoder/')
#sys.path.append('../../src/analyzer/')
print(sys.path)

extensions = ["myst_parser", # allow .md files
              "sphinxcontrib.mermaid", 
              "sphinx.ext.autodoc",
              'sphinx.ext.todo'
              # 'sphinxcontrib.bibtex' not used yet
              ]

templates_path = ['_templates']
exclude_patterns = []

todo_include_todos = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
