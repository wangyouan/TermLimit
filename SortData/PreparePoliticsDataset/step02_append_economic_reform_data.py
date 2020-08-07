#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_append_economic_reform_data
# @Date: 2020/8/7
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.PreparePoliticsDataset.step02_append_economic_reform_data
"""

import os

import pandas as pd
from pandas import DataFrame

from SortData.PreparePoliticsDataset import PathInfo as const

if __name__ == '__main__':
    economic_reform_df: DataFrame = pd.read_stata(os.path.join(const.DATA_PATH, 'economic_reform.dta'))
    economic_reform_df.loc[:, 'year'] = economic_reform_df.year.dt.year
    economic_useful_variables = ['reform', 'country', 'reform_index', 'year']
    economic_reform_useful_df: DataFrame = economic_reform_df.loc[:, economic_useful_variables].copy()
    tmp_df = DataFrame(columns=['country', 'year'])

    reform_prefix_list = ['agri', 'Net', 'trade', 'cap', 'curr', 'dom']
    for reform in range(1, 7):
        prefix = reform_prefix_list[reform - 1]
        reform_df: DataFrame = economic_reform_useful_df.loc[
            economic_reform_useful_df['reform'] == reform, ['country', 'year', 'reform_index']].rename(
            columns={'reform_index': '{}_reform_index'.format(prefix)})
        tmp_df: DataFrame = tmp_df.merge(reform_df, on=['country', 'year'], how='outer')

    reform_index_df: DataFrame = tmp_df.rename(columns={'country': 'cname'})
    reform_index_df.loc[:, 'cname'] = reform_index_df['cname'].replace(
        {'US': 'United States', 'UK': 'United Kingdom', "Cote D'Ivoire": "Cote d'Ivoire",
         'CAR': 'Central African Republic', 'Cyprus': 'Cyprus (1975-)', 'Czech Rep': 'Czech Republic',
         'Ethiopia': 'Ethiopia (-1992)', 'France': 'France (1963-)', 'Korea': 'Korea, South',
         'Kyrgyz Rep': 'Kyrgyzstan', 'Lao': 'Laos', 'Macedonia': 'North Macedonia', 'Malaysia': 'Malaysia (1966-)',
         'Pakistan': 'Pakistan (1971-)', 'Papua New G.': 'Papua New Guinea', 'Slovak': 'Slovakia',
         'Solomon Is': 'Solomon Islands', 'St Kitts N': 'St Kitts and Nevis',
         'St Vincent Gr': 'St Vincent and the Grenadines', 'Trinidad Tob': 'Trinidad and Tobago',
         'Viet Nam': 'Vietnam', 'Yemen': 'Yemen, North', 'Zaire': 'Congo, Democratic Republic'})

    useful_df2: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200807_purge_qog_ucdp_merged.pkl'))
    useful_df3: DataFrame = useful_df2.merge(reform_index_df, on=['cname', 'year'], how='left')
    useful_df3.to_pickle(os.path.join(const.TEMP_PATH, '20200807_purge_qog_ucdp_reform_merged.pkl'))
    useful_df3.to_csv(os.path.join(const.OUTPUT_PATH, '20200807_purge_qog_ucdp_reform_merged.csv'), index=False)
