#! /usr/bin/env python

from distutils.core import setup

setup( name='oemof'
     , version='0.0.1'
     , description='The open energy modelling framework'
     , package_dir = {'oemof': 'src'}
     , packages=[ "oemof"
                , "oemof.network"
                , "oemof.network.entities"
                , "oemof.network.entities.components"
                ]
     )

