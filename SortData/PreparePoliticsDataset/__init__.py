#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2020/8/5
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
This module is used in my Xiaoxin Air 14
"""

import os


class PathInfo(object):
    CODE_PATH = '/mnt/d/wyatc/PycharmProjects/TermLimit'
    ROOT_PATH = '/mnt/d/wyatc/Documents/Projects/TermLimit'
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'output')
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    DATA_PATH = os.path.join(ROOT_PATH, 'data')
