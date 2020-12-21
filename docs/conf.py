""" Documentation configuration and workflow for wxyz
"""
# pylint: disable=invalid-name,redefined-builtin,import-error
import os
import pathlib
import sys
from subprocess import check_call

import nbsphinx

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent

nbsphinx.RST_TEMPLATE = nbsphinx.RST_TEMPLATE.replace(
    """{% block input -%}""",
    """{% block input -%}""" """{% if not cell.metadata.get("hide_input", False) -%}""",
).replace("""{% endblock input %}""", """{%- endif -%}{%- endblock input %}""")


# -- Project information -----------------------------------------------------
project = "WXYZ"
author = "WXYZ Contributors"
copyright = f"2020, {author}"

# The short X.Y version
version = "0.4.0"
# The full version, including alpha/beta/rc tags
release = "0.4.0a0"


# -- General configuration ---------------------------------------------------
extensions = [
    "recommonmark",
    "sphinx_markdown_tables",
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.githubpages",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_autodoc_typehints",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [".ipynb_checkpoints", "**/.ipynb_checkpoints", "**/~.*"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "monokai"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "wxyzdoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "wxyz.tex",
        "WXYZ Documentation",
        "WXYZ Contributors",
        "manual",
    )
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "wxyz", "WXYZ Documentation", [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "wxyz",
        "WXYZ Documentation",
        author,
        "wxyz",
        "Some Experiemental Jupyter Widgets",
        "Miscellaneous",
    )
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "jsonschema": ("https://python-jsonschema.readthedocs.io/en/stable/", None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


github_url = "https://github.com"
github_repo_org = "deathbeds"
github_repo_name = "wxyz"
github_repo_slug = f"{github_repo_org}/{github_repo_name}"
github_repo_url = f"{github_url}/{github_repo_slug}"

extlinks = {
    "issue": (f"{github_repo_url}/issues/%s", "#"),
    "pr": (f"{github_repo_url}/pull/%s", "PR #"),
    "commit": (f"{github_repo_url}/commit/%s", ""),
    "gh": (f"{github_url}/%s", "GitHub: "),
}

html_show_sourcelink = False  # True will show link to source

html_context = {
    "display_github": True,
    "github_user": github_repo_org,
    "github_repo": github_repo_name,
    "github_version": "master",
    "conf_py_path": "/docs/",
}

# html_logo = "../packages/jupyterlab-starters/style/icons/starter.svg"

# sphinx-autodoc-typehints
# set_type_checking_flag = True
# always_document_param_types = True
# typehints_document_rtype = True
