#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_check_country_info_of_compustat_data
# @Date: 2020/3/14
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SummarizeData.step01_check_country_info_of_compustat_data
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.STATA_DATA_PATH, '20200311_regression_data.dta'))
    country_list = reg_df[const.COUNTRY_ISO3].drop_duplicates()
    reg_df.loc[:, 'has_event'] = reg_df[['formal_Extend', 'formal_Shrink', 'real_Extend', 'real_Shrink']].sum(axis=1)
    reg_df.loc[:, 'has_event'] = (reg_df['has_event'] > 0).astype(int)
    used_event_year_df: DataFrame = reg_df[reg_df['has_event'] == 1].drop_duplicates(
        subset=[const.COUNTRY_ISO3, const.FISCAL_YEAR])
    country_year_group = reg_df.groupby([const.COUNTRY_ISO3, const.FISCAL_YEAR])
    country_year_event = country_year_group[
        ['has_event', 'formal_Extend', 'formal_Shrink', 'real_Extend', 'real_Shrink']].last()
    country_year_firm_count = country_year_group[const.GVKEY].count()
    country_year_firm_count.name = 'firm_number'
    country_year_summary: DataFrame = country_year_event.merge(country_year_firm_count, left_index=True,
                                                               right_index=True).reset_index(drop=False)
    country_info_df: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'countries_codes_and_coordinates.csv'),
                                             usecols=["Alpha-3 code", "Numeric code", "Country"]).rename(
        columns={"Alpha-3 code": const.COUNTRY_ISO3, "Numeric code": const.COUNTRY_ISO3N}).drop_duplicates(
        subset=[const.COUNTRY_ISO3])
    country_info_df.loc[:, const.COUNTRY_ISO3] = country_info_df[const.COUNTRY_ISO3].str.strip('" ').astype(str)
    country_info_df.loc[:, const.COUNTRY_ISO3N] = country_info_df[const.COUNTRY_ISO3N].str.strip('" ').astype(int)

    country_year_summary2: DataFrame = country_year_summary.merge(country_info_df, on=[const.COUNTRY_ISO3], how='left')

    country_year_summary2.to_excel(os.path.join(const.RESULT_PATH, '20190314_country_year_summary.xlsx'))
