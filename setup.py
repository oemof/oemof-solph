#! /usr/bin/env python

"""TODO: Maybe add a docstring containing a long description for oemof?

  This would double as something we could put int the `long_description`
  parameter for `setup` and it would squelch some complaints pylint has on
  `setup.py`.

"""

from setuptools import find_packages, setup
import os

import oemof

setup(name='oemof',
      version=oemof.__version__,
      author='oemof developing group',
      author_email='oemof@rl-institut.de',
      description='The open energy modelling framework',
      namespace_package = ['oemof'],
      packages=find_packages(),
      package_data={
          'oemof': [os.path.join('tools', 'default_files', '*.ini')],
          'examples': [
              os.path.join('*.csv'),
              os.path.join('storage_optimization',
                           '*.csv')
          ]},
      package_dir={'oemof': 'oemof'},
      install_requires=['dill',
                        'numpy >= 1.7.0',
                        'pandas >= 0.17.0',
                        'pyomo >= 4.2.0, != 4.3.11377']
     )
