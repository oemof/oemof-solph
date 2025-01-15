# -*- coding: utf-8 -*-

import os
import sys
import oemof.solph

import matplotlib
from sphinx.ext.autodoc import between


matplotlib.use("agg")
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "examples"))


def setup(app):
    # Register a sphinx.ext.autodoc.between listener to ignore everything
    # between lines that contain the word IGNORE
    app.connect("autodoc-process-docstring", between("^SPDX.*$", exclude=True))
    return app


# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
]

# landing page
# master_doc = 'contents'
# names, years, etc
project = "oemof.solph"
year = "2024"
author = "oemof developer group"
copyright = "{0}, {1}".format(year, author)

# The short X.Y version.
version = oemof.solph.__version__.split(" ")[0]
# The full version, including alpha/beta/rc tags.
release = oemof.solph.__version__

# The suffix of source filenames.
source_suffix = ".rst"
# folder for templates
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "some"
# pygments_dark_style = "someother"

# show all class members
# numpydoc_show_class_members = False

# place for bibtex references
bibtex_bibfiles = ["references.bib"]

# links to github
github_repo_url = "https://github.com/oemof/oemof-solph/"
extlinks = {
    "issue": (f"{github_repo_url}/issues/%s", "#%s"),  # noqa: WPS323
    "pr": (f"{github_repo_url}/pull/%s", "PR #%s"),  # noqa: WPS323
    "commit": (f"{github_repo_url}/commit/%s", "%s"),  # noqa: WPS323
}

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = "furo"

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".


# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "%s-%s" % (project, version)

# Some more stuff
html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
# html_additional_pages = {
#     "index": "index.html"
# }

html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
        "sidebar/variant-selector.html",
    ],
}

html_theme_options = {
    "light_logo": "./_logo/logo_oemof_solph_COMPACT.svg",
    "dark_logo": "./_logo/logo_oemof_solph_COMPACT_darkmode.svg",
    "announcement": """
    <div oemof-announcement=\"https://raw.githubusercontent.com/oemof/oemof-solph/announcements/announcement.html\"></div>
    """,
}

html_js_files = [
    "js/custom.js",
]


html_favicon = "./_static/_logo/logo_oemof_solph_ICON.svg"

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

# copybutton configuration
copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True

# Output file base name for HTML help builder.
htmlhelp_basename = "oemof.solph_doc"

linkcheck_ignore = [
    r"https://requires.io/.*",
    r"https://matrix.to/*",
    r"https://forum.openmod-initiative.org/*",
    r"https://github.com/oemof/oemof-solph/issues/*",
    r"https://github.com/oemof/oemof-solph/pull/*",
    # Due to traffic limitation, the folowwing creates a 403 in CI pipeline:
    "https://www.sciencedirect.com/science/article/abs/pii/S036054421500331X",
]
