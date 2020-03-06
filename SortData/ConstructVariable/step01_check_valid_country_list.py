#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_check_valid_country_list
# @Date: 2020/3/6
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructVariable.step01_check_valid_country_list
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    ctat_df: DataFrame = pd.read_csv(os.path.join(const.DATABASE_PATH, 'Compustat',
                                                  '198706_202003_global_compustat_all_firms.zip')).sort_values(
        by='datadate', ascending=True).rename(columns={'fyear': const.YEAR}).drop_duplicates(
        subset=[const.GVKEY, const.YEAR], keep='last')
    country_list: DataFrame = ctat_df.loc[:, ['loc', const.YEAR]].drop_duplicates()
    country_year_min: DataFrame = country_list.groupby('loc')[const.YEAR].min().rename(
        columns={const.YEAR: 'start_year'})

    country_year_max: DataFrame = country_list.groupby('loc')[const.YEAR].max().rename(
        columns={const.YEAR: 'end_year'})
    country_year_data: DataFrame = country_year_min.merge(country_year_max, left_index=True, right_index=True)
    country_year_data.to_csv(os.path.join(const.RESULT_PATH, '20200306_ctat_global_country_list.csv'))
