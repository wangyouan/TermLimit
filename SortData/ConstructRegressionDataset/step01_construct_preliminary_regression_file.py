#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_construct_preliminary_regression_file
# @Date: 2020/3/9
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step01_construct_preliminary_regression_file
"""

import os

import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constants import Constants as const

if __name__ == '__main__':
    ctat_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20190309_regression_control_variables.pkl'))
    ann_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200309_annual_event_data.pkl')).rename(
        columns={'EventYear': 'fyear'})

    dep_vars = ['ln_at', 'CAPEX', 'EBITDA', 'PTBI', 'R_B', 'SGA', 'VOL_PTBI',
                'VOL_EBITDA', 'ROA', 'LEVERAGE', 'CASH_HOLDING', 'TANGIBILITY',
                'MV', 'TobinQ']

    for key in dep_vars:
        ctat_df.loc[ctat_df[key].notnull(), key] = winsorize(ctat_df[key].dropna(), (0.01, 0.01))

    ctat_df.loc[:, const.COUNTRY_ISO3] = ctat_df['loc']
    reg_df: DataFrame = ctat_df.merge(ann_df, on=['fyear', const.COUNTRY_ISO3], how='left')
    valid_keys = [const.GVKEY, 'fyear']
    valid_keys.extend(dep_vars)
    ctat_df_valid: DataFrame = ctat_df.loc[:, valid_keys].copy()
    ctat_df_valid.loc[:, 'fyear'] -= 1
    reg_df2: DataFrame = reg_df.merge(ctat_df_valid, on=[const.GVKEY, 'fyear'], how='left', suffixes=['', '_1'])
    for key in ['addzip', 'formal_last_term', 'real_last_term', 'formal_current_term', 'real_current_term']:
        reg_df2.loc[:, key] = reg_df2[key].astype(str)
    reg_df3: DataFrame = reg_df2.drop(['do'], axis=1).rename(columns={'Latitude (average)': 'loc_lat',
                                                                      'Longitude (average)': 'loc_lon'})

    for key in ['formal_Extend', 'real_Extend', 'formal_Shrink', 'real_Shrink']:
        reg_df3.loc[:, key] = reg_df3[key].fillna(0)
        country_year_df: DataFrame = reg_df3.loc[reg_df3[key] == 1, [const.COUNTRY_ISO3N, 'fyear']].drop_duplicates()
        for lag in range(1, 5):
            temp_df: DataFrame = country_year_df.copy()
            for j in range(lag):
                tmp_country_year = temp_df.copy()
                tmp_country_year.loc[:, 'fyear'] += 1
                temp_df: DataFrame = pd.concat([temp_df, tmp_country_year], ignore_index=True)

            temp_df.loc[:, '{}_{}'.format(key, lag + 1)] = 1
            reg_df3: DataFrame = reg_df3.merge(temp_df, on=[const.COUNTRY_ISO3N, 'fyear'], how='left')
            reg_df3.loc[:, '{}_{}'.format(key, lag + 1)] = reg_df3['{}_{}'.format(key, lag + 1)].fillna(0)

    reg_df3.to_stata(os.path.join(const.STATA_DATA_PATH, '20200309_regression_data.dta'), write_index=False,
                     version=117)
