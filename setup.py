#! /usr/bin/env python

from setuptools import find_packages, setup

setup(name='oemof_base',
      version='0.0.3dev',
      author='oemof developing group',
      author_email='oemof@rl-institut.de',
      description='The open energy modelling framework',
      packages=find_packages(),
      package_dir={'oemof': 'oemof'},
      install_requires=['numpy >= 1.7.0',
                        'pandas >= 0.17.0',
                        'pyomo >= 4.0.0']
      )
