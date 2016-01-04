#! /usr/bin/env python

from setuptools import setup

setup(name='oemof_base',
      version='0.0.2.1',
      author='oemof developing group',
      author_email='oemof@rl-institut.de',
      description='The open energy modelling framework',
      package_dir={'oemof': 'oemof'},
      install_requires=['numpy >= 1.7.0',
                        'pandas >= 0.13.1',
                        'pyomo >= 4.0.0']
      )
