#! /usr/bin/env python

"""TODO: Maybe add a docstring containing a long description for oemof?

  This would double as something we could put int the `long_description`
  parameter for `setup` and it would squelch some complaints pylint has on
  `setup.py`.

"""

from setuptools import find_packages, setup
import os

import oemof

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='oemof',
      version=oemof.__version__,
      author='oemof developing group',
      author_email='oemof@rl-institut.de',
      description='The open energy modelling framework',
      url='https://oemof.org/',
      namespace_package=['oemof'],
      long_description=read('README.rst'),
      packages=find_packages(),
      package_data={
          'examples': [
              os.path.join('solph',
                           'csv_reader',
                           'investment',
                           'data',
                           '*.csv'),
              os.path.join('solph',
                           'csv_reader',
                           'dispatch',
                           'scenarios',
                           '*.csv'),
              os.path.join('solph', 'simple_dispatch','*.csv'),
              os.path.join('solph', 'variable_chp','*.csv'),
              os.path.join('solph', 'storage_investment','*.csv')
          ],
            'oemof': [os.path.join('tools', 'default_files', '*.ini')]},
      install_requires=['dill <= 0.2.7.1',
                        'numpy >= 1.7.0, < 1.15',
                        'pandas >= 0.18.0, <= 0.22',
                        'pyomo >= 4.2.0, != 4.3.11377, <=5.3',
                        'matplotlib'],
      entry_points={
          'console_scripts': [
              'oemof_examples = examples.examples:examples']}
     )
