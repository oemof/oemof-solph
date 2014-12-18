#!/usr/bin/python
# -*- coding: utf-8

'''
Change 'path_to_your_pahesmf.py' to your personal path

If the path to your pahesmf.py file is:
'/home/user/pahesmf/pahesmf.py'
use:
'sys.path.append("/home/user/pahesmf/")'
'''

import sys
sys.path.append("path_to_your_pahesmf_py")
import src.pahesmf as pahesmf
pahesmf.init()