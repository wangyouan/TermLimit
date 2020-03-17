#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step06_construct_event_date_file
# @Date: 2020/3/17
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructVariable.step06_construct_event_date_file
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    country_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, '20200317_country_information.xlsx'),
                                          sheet_name=1)
    ann_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, '20200317_annual_event_data.xlsx')).rename(
        columns={'EventYear': const.YEAR})
    common_keys = [i for i in set(ann_df.keys()).intersection(country_df.keys()) if
                   i not in {const.COUNTRY_ISO3, const.YEAR}]
    country_df_event_df: DataFrame = country_df.merge(ann_df.drop(common_keys, axis=1),
                                                      on=[const.COUNTRY_ISO3, const.YEAR], how='left')
    country_df_event_df.to_excel(os.path.join(const.RESULT_PATH, '20200317_country_year_event_dataset.xlsx'),
                                 index=False)
