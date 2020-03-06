#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2020/3/6
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os


class PathInfo(object):
    ROOT_PATH = '/home/zigan/Documents/wangyouan/research/TermLimit'

    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    RESULT_PATH = os.path.join(ROOT_PATH, 'output')
    STATA_PATH = os.path.join(ROOT_PATH, 'stata')
    STATA_CODE_PATH = os.path.join(STATA_PATH, 'code')
    STATA_DATA_PATH = os.path.join(STATA_PATH, 'data')
    STATA_RESULT_PATH = os.path.join(STATA_PATH, 'result')

    DATABASE_PATH = '/home/zigan/Documents/wangyouan/database'

    WRDS_PATH = '/home/zigan/Documents/wangyouan/database/wrds'
    TFN_PATH = os.path.join(WRDS_PATH, 'tfn')
    TFN_OWNER_PATH = os.path.join(TFN_PATH, 'ownership')
    TFN_S34_PATH = os.path.join(TFN_PATH, 's34')

    REGRESSION_PATH = '/home/zigan/Documents/wangyouan/research/DataMining/OLS'
    REG_CONFIG_PATH = os.path.join(REGRESSION_PATH, 'config', 'TermLimits')
    REG_RESULT_PATH = os.path.join(REGRESSION_PATH, 'result', 'TermLimits')
    REG_DATA_PATH = os.path.join(REGRESSION_PATH, 'data', 'TermLimits')
