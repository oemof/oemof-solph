# -*- coding: utf-8 -*-

import os
import sys

import matplotlib
from sphinx.ext.autodoc import between

from oemof.solph import __version__


matplotlib.use("agg")
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "examples"))


def setup(app):
    # Register a sphinx.ext.autodoc.between listener to ignore everything
    # between lines that contain the word IGNORE
    app.connect("autodoc-process-docstring", between("^SPDX.*$", exclude=True))
    return app


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
source_suffix = ".rst"
master_doc = "index"
project = "oemof.solph"
year = "2014-2023"
author = "oemof-developer-group"
copyright = "{0}, {1}".format(year, author)
version = release = __version__

pygments_style = "trac"
templates_path = ["."]
extlinks = {
    "issue": ("https://github.com/oemof/oemof-solph/issues/%s", "#%s"),
    "pr": ("https://github.com/oemof/oemof-solph/pull/%s", "PR #%s"),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = "sphinx_rtd_theme"

html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_sidebars = {
    "**": ["searchbox.html", "globaltoc.html", "sourcelink.html"],
}
html_short_title = "%s-%s" % (project, version)
html_logo = "./_logo/logo_oemof_solph_COMPACT_bg.svg"

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
nitpicky = False

exclude_patterns = ["_build", "whatsnew/*"]

linkcheck_ignore = [
    r"https://requires.io/.*",
    r"https://matrix.to/*",
    r"https://forum.openmod-initiative.org/*",
] + (
    [
        r"https://github.com/oemof/oemof-solph/issues/*",
        r"https://github.com/oemof/oemof-solph/pull/*",
    ]
    if "TRAVIS" not in os.environ
    else []
)
