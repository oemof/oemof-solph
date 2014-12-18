#!/usr/bin/python
# -*- coding: utf-8


def pg_db():
    local_dict = {
        'ip': 'xxx.xxx.xx.xx',
        'port': '5432',
        'db': 'name_db',
        'user': 'username',
        'password': 'password'}
    return local_dict


def pahesmf():
    local_dict = pg_db()
    local_dict['dlrpath'] = '/home/uwe/rli-server/05_Temp'
    return local_dict
