__author__ = 'stfn'

print("/iolib/postgis.py imported")

import oemof.iolib.config as cfg


def raw_query(query_string):
    return query_string + " loaded."