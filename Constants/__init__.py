#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2020/3/6
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

from .path_info import PathInfo


class Constants(PathInfo):
    GVKEY = 'gvkey'
    COUNTRY = 'country'
    COUNTRY_ISO3 = 'country_iso3'
    COUNTRY_ISO3N = 'country_iso3n'
    YEAR = 'year'
    MONTH = 'month'
    CIK = 'cik'
    CURRENCY = 'ioscur'
    SIC = 'sic_code'
