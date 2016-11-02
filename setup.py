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
      namespace_package=['oemof'],
      packages=find_packages(),
      package_data={
          'examples': [
              os.path.join('solph',
                           'csv_reader',
                           'investment_example',
                           'data',
                           '*.csv'),
              os.path.join('solph',
                           'csv_reader',
                           'operational_example',
                           'scenarios',
                           '*.csv'),
              os.path.join('solph', 'simple_least_costs','*.csv'),
              os.path.join('solph', 'storage_optimization','*.csv')
          ],
            'oemof': [os.path.join('tools', 'default_files', '*.ini')]},
      install_requires=['dill',
                        'numpy >= 1.7.0',
                        'pandas >= 0.18.0',
                        'pyomo >= 4.2.0, != 4.3.11377',
                        'matplotlib'],
      entry_points={
          'console_scripts': [
              'oemof_examples = examples.examples:examples']}
     )
