#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step06_construct_regression_data_with_extended_event_data
# @Date: 2020/3/20
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step06_construct_regression_data_with_extended_event_data
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const


def construct_n_dummy_variables(tmp_df: DataFrame):
    if tmp_df.loc[~tmp_df['event_month'].isnull()].empty:
        return tmp_df

    sorted_tmp_df: DataFrame = tmp_df.sort_values(by=[const.YEAR], ascending=True)

    for suffix in ['Extend', 'ToUnlimit', 'ToLimit', 'Shrink']:
        for prefix in ['formal', 'real']:
            origin_key = '{}_{}'.format(prefix, suffix)
            data_series = sorted_tmp_df[origin_key]
            if data_series.sum() == 0:
                continue
            for n in range(1, 6):
                new_key_a = '{}_a{}'.format(origin_key, n)
                new_key_b = '{}_b{}'.format(origin_key, n)
                new_key_n = '{}_{}'.format(origin_key, n + 1)
                data_series = sorted_tmp_df[origin_key]
                sorted_tmp_df.loc[:, new_key_a] = data_series.shift(n).fillna(0)
                sorted_tmp_df.loc[:, new_key_b] = data_series.shift(-n).fillna(0)
                key_list = [origin_key]
                key_list.extend(['{}_a{}'.format(origin_key, j) for j in range(1, n + 1)])
                sorted_tmp_df.loc[:, new_key_n] = sorted_tmp_df[key_list].sum(axis=1)

    return sorted_tmp_df


if __name__ == '__main__':
    event_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, '20200320_country_year_event_dataset.xlsx'))
    event_df_group = event_df.groupby(const.COUNTRY_ISO3)
    event_df_2: DataFrame = pd.concat([construct_n_dummy_variables(df) for _, df in event_df_group], ignore_index=True,
                                      sort=False)
    data_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200315_full_regression_data.pkl'))

    common_keys = set(event_df_2.keys()).intersection(data_df.keys())
    reg_df: DataFrame = data_df.drop([i for i in common_keys if i != const.COUNTRY_ISO3], axis=1).merge(
        event_df_2.rename(
            columns={const.YEAR: const.FISCAL_YEAR}), on=[const.COUNTRY_ISO3, const.FISCAL_YEAR])
    for suf in ['Extend', 'ToUnlimit', 'ToLimit', 'Shrink']:
        for pre in ['formal', 'real']:
            real_key = '{}_{}'.format(pre, suf)
            reg_df.loc[:, real_key] = reg_df[real_key].fillna(0)

    reg_df.loc[:, 'RealConsist'] = reg_df['RealConsist'].fillna(reg_df['event_month'].isnull().astype(int)).fillna(0)
    reg_df.loc[:, 'has_event'] = reg_df['has_event'].fillna(0)

    cy_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200320_country_year_data.pkl'))
    reg_df_with_cy: DataFrame = reg_df.merge(cy_df.drop(['Country', 'Year'], axis=1),
                                             on=[const.COUNTRY_ISO3, const.FISCAL_YEAR], how='left').rename(

        columns=lambda x: x.replace('.', '_'))
    reg_df_with_cy2: DataFrame = reg_df_with_cy.drop(['do', 'addzip', 'county'], axis=1)
    real_formal_keys = [i for i in reg_df_with_cy2.keys() if i.startswith('formal') or i.startswith('real')]
    for key in real_formal_keys:
        if 'term' in key:
            continue
        reg_df_with_cy2.loc[:, key] = reg_df_with_cy2[key].fillna(0)
    reg_df_with_cy2.to_pickle(os.path.join(const.TEMP_PATH, '20200320_term_limit_regression_data.pkl'))
    reg_df_with_cy2.to_stata(os.path.join(const.STATA_DATA_PATH, '20200320_term_limit_regression_data.dta'),
                             write_index=False)
