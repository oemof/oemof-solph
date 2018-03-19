#! /usr/bin/env python

"""
This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/setup.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from setuptools import find_packages, setup
import os

import oemof


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='oemof',
      version=oemof.__version__,
      author='oemof developer group',
      author_email='oemof@rl-institut.de',
      description='The open energy modelling framework',
      url='https://oemof.org/',
      namespace_package=['oemof'],
      long_description=read('README.rst'),
      packages=find_packages(),
      package_data={'oemof': [
          os.path.join('tools', 'default_files', '*.ini')]},
      install_requires=['dill <= 0.2.7.1',
                        'numpy >= 1.7.0, <= 1.14.2',
                        'pandas >= 0.18.0, <= 0.22',
                        'pyomo >= 4.4.0, <= 5.4.3',
                        'networkx <= 2.1',
                        'nose <= 1.3.7'],
      entry_points={
          'console_scripts': [
              'oemof_installation_test = '
              'oemof.tools.console_scripts:check_oemof_installation',
              'test_oemof = '
              'oemof.tools.console_scripts:test_oemof']})
