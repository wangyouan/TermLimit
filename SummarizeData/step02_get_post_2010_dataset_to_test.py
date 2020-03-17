#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_get_post_2010_dataset_to_test
# @Date: 2020/3/15
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SummarizeData.step02_get_post_2010_dataset_to_test
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200315_full_regression_data.pkl'))
    reg_df_country_df: DataFrame = reg_df.drop_duplicates(subset=[const.FISCAL_YEAR, const.COUNTRY_ISO3])
    reg_df_country_df2: DataFrame = reg_df_country_df.loc[reg_df_country_df[const.FISCAL_YEAR] >= 2010,
                                                          [const.FISCAL_YEAR, const.COUNTRY_ISO3, 'has_event',
                                                           'formal_Extend', 'formal_Shrink', 'real_Extend',
                                                           'real_Shrink']].copy()

    country_info_df: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'countries_codes_and_coordinates.csv'),
                                             usecols=["Country", "Alpha-3 code", "Numeric code"]).rename(
        columns={"Alpha-3 code": const.COUNTRY_ISO3, "Numeric code": const.COUNTRY_ISO3N}).drop_duplicates(
        subset=[const.COUNTRY_ISO3])
    country_info_df.loc[:, const.COUNTRY_ISO3N] = country_info_df[const.COUNTRY_ISO3N].str.strip('" ').astype(int)
    country_info_df.loc[:, const.COUNTRY_ISO3] = country_info_df[const.COUNTRY_ISO3].str.strip('" ').astype(str)
    country_info_df.to_pickle(os.path.join(const.TEMP_PATH, '20200316_country_info_list.pkl'))

    country_year_summary2: DataFrame = reg_df_country_df2.merge(country_info_df, on=[const.COUNTRY_ISO3], how='left')
    country_year_summary2.to_excel(os.path.join(const.RESULT_PATH, '20200315_country_year_event_list.xlsx'),
                                   index=False)
