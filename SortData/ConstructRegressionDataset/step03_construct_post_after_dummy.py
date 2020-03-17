#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_construct_post_after_dummy
# @Date: 2020/3/9
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step03_construct_post_after_dummy
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constants import Constants as const

if __name__ == '__main__':
    ann_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, '20200317_annual_event_data.xlsx'))
    # for key in ['real_last_term', 'real_current_term', 'real_Extend', 'real_ToUnlimit', 'real_ToLimit', 'real_Shrink']:
    #     ann_df.loc[14, key] = ann_df.loc[15, key]
    #
    # ann_df.drop(15, inplace=True)
    # ann_df.to_excel(os.path.join(const.RESULT_PATH, '20200310_annual_event_data.xlsx'), index=False)
    useful_keys = ['country_iso3', 'EventYear', 'formal_Extend', 'formal_ToUnlimit', 'formal_ToLimit', 'formal_Shrink',
                   'real_Extend', 'real_ToUnlimit', 'real_ToLimit', 'real_Shrink']
    ann_df_useful = ann_df.loc[:, useful_keys].copy()
    result_df: DataFrame = ann_df_useful.copy()

    # construct t + 1 dummy and n dummy
    for lag in range(5):
        real_lag = lag + 1
        t_keys_dict = {key: '{}_t{}'.format(key, real_lag) for key in useful_keys[2:]}
        n_keys_dict = {key: '{}_{}'.format(key, real_lag + 1) for key in useful_keys[2:]}
        tmp_df: DataFrame = ann_df_useful.copy()
        tmp_df.loc[:, 'EventYear'] += real_lag
        tmp_df_t: DataFrame = tmp_df.rename(columns=t_keys_dict)
        result_df: DataFrame = result_df.append(tmp_df_t, ignore_index=True, sort=False)

        n_dfs = list()
        for i in range(real_lag + 1):
            tmp_df2: DataFrame = ann_df_useful.rename(columns=n_keys_dict)
            tmp_df2.loc[:, 'EventYear'] += i
            n_dfs.append(tmp_df2)

        tmp_df_n: DataFrame = pd.concat(n_dfs, ignore_index=True, sort=False)
        result_df: DataFrame = result_df.append(tmp_df_n, ignore_index=True)

    # Construct t - n dummy
    for lag in range(1, 6):
        t_keys_dict = {key: '{}_tm{}'.format(key, lag) for key in useful_keys[2:]}
        tmp_df: DataFrame = ann_df_useful.copy()
        tmp_df.loc[:, 'EventYear'] -= lag
        tmp_df_t: DataFrame = tmp_df.rename(columns=t_keys_dict)
        result_df: DataFrame = result_df.append(tmp_df_t, ignore_index=True, sort=False)

    event_df: DataFrame = result_df.sort_values(['country_iso3', 'EventYear']).fillna(0).rename(
        columns={'EventYear': const.FISCAL_YEAR})
    real_event_df: DataFrame = event_df.groupby([const.COUNTRY_ISO3, const.FISCAL_YEAR]).sum()
    for key in real_event_df:
        real_event_df.loc[:, key] = (real_event_df[key] > 0).astype(int)

    event_df: DataFrame = real_event_df.reset_index(drop=False)
    event_df.to_pickle(os.path.join(const.TEMP_PATH, '20200320_term_limit_change_event2.pkl'))

    ctat_df: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20200310_regression_control_variables_winsorized.pkl'))
    dep_vars = ['ln_at', 'CAPEX', 'EBITDA', 'PTBI', 'ROA', 'R_B', 'SGA', 'LEVERAGE', 'CASH_HOLDING', 'TANGIBILITY',
                'TobinQ', 'ln_emp', 'ln_sale']

    ctat_df.loc[:, 'ln_sale'] = ctat_df['sale'].apply(np.log)
    ctat_df.loc[:, 'ln_emp'] = ctat_df['emp'].apply(np.log)
    ctat_df: DataFrame = ctat_df.replace([np.inf, -np.inf], np.nan)
    for key in ['ln_emp', 'ln_sale']:
        ctat_df.loc[ctat_df[key].notnull(), key] = winsorize(ctat_df[key].dropna(), (0.01, 0.01))

    ctat_df.loc[:, const.COUNTRY_ISO3] = ctat_df['loc']
    reg_df: DataFrame = ctat_df.merge(event_df, on=[const.COUNTRY_ISO3, const.FISCAL_YEAR], how='left')

    for key in dep_vars:
        reg_df.loc[:, '{}_1'.format(key)] = reg_df.groupby(const.GVKEY)[key].shift(1)

    for key in event_df.keys():
        if key in {const.COUNTRY_ISO3, const.FISCAL_YEAR}:
            continue
        reg_df.loc[:, key] = reg_df[key].fillna(0)

    # Remove invalid countries
    reg_df_drop: DataFrame = reg_df.loc[~reg_df['loc'].isin({'GNQ', 'TGO', 'TKM', 'SRB'})].copy()
    key_list = [('AZE', 2003), ('BRA', 1993), ('COM', 1991), ('PER', 2001)]
    for iso3, year in key_list:
        reg_df_drop: DataFrame = reg_df_drop.loc[(reg_df_drop['loc'] != iso3) | (reg_df_drop['fyear'] >= year)].copy()

    reg_df_drop2: DataFrame = reg_df_drop.loc[(reg_df_drop['loc'] != 'LBN') | (reg_df_drop['fyear'] <= 2004)].copy()
    reg_df_drop2.to_pickle(os.path.join(const.TEMP_PATH, '20200315_full_regression_data.pkl'))
    valid_reg_df: DataFrame = reg_df_drop2.loc[reg_df_drop2['fyear'] < 2011].drop(['do'], axis=1)
    for key in ['addzip']:
        valid_reg_df.loc[:, key] = valid_reg_df[key].astype(str)
    valid_reg_df.to_stata(os.path.join(const.STATA_DATA_PATH, '20200310_regression_data.dta'),
                          write_index=False, version=117)
