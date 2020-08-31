# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'oemof.solph'
year = '2014-2020'
author = 'oemof-developer-group'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.4.2.dev0'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/oemof/oemof-solph/issues/%s', '#'),
    'pr': ('https://github.com/oemof/oemof-solph/pull/%s', 'PR #'),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
    '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

exclude_patterns = ['_build', 'whatsnew/*']

linkcheck_ignore = [r"https://requires.io/.*"] + (
    [
        r"https://github.com/oemof/oemof-solph/issues/*",
        r"https://github.com/oemof/oemof-solph/pull/*",
    ]
    if "TRAVIS" not in os.environ
    else []
)
