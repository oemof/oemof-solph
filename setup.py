#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fh:
        return fh.read()


long_description = "%s" % (
    re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
        "", read("README.rst")
    )
)


setup(
    name="oemof.solph",
    version="0.5.2dev0",
    license="MIT",
    description=(
        "A model generator for energy system modelling and optimisation."
    ),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="oemof developer group",
    author_email="contact@oemof.org",
    url="https://oemof.org",
    packages=["oemof"] + ["oemof." + p for p in find_packages("src/oemof")],
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://oemof-solph.readthedocs.io/",
        "Changelog": (
            "https://oemof-solph.readthedocs.io/en/latest/changelog.html"
        ),
        "Issue Tracker": "https://github.com/oemof/oemof-solph/issues",
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires=">=3.8",
    install_requires=[
        "blinker",
        "dill",
        "numpy",
        "pandas >= 1.5.3",
        "pyomo >= 6.6.0, < 7.0",
        "networkx",
        "oemof.tools >= 0.4.2",
        "oemof.network >= 0.5.0a1",
    ],
    extras_require={
        "dev": [
            "matplotlib",
            "nbformat",
            "pytest",
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx-copybutton",
            "sphinx-design",
            "termcolor",
        ],
        "examples": ["matplotlib"],
        "dummy": ["oemof"],
    },
    entry_points={
        "console_scripts": [
            "oemof_installation_test = "
            + "oemof.solph._console_scripts:check_oemof_installation"
        ]
    },
)
