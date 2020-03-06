#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_construct_term_change_dummy
# @Date: 2020/3/6
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructVariable.step02_construct_term_change_dummy
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const


def check_if_continue_year(df):
    min_year = df[const.YEAR].min()
    max_year = df[const.YEAR].max()
    return int((max_year - min_year) + 1 == df.shape[0])


def check_get_term_change(df):
    term_change_list = DataFrame()
    country_name = df.iloc[0]['country']

    for i in range(df.shape[0] - 1):
        last_row = df.iloc[i]
        current_row = df.iloc[i + 1]
        current_real_term = current_row['terms_effect']
        current_formal_term = current_row['formal_terms']
        last_real_term = last_row['terms_effect']
        last_formal_term = last_row['formal_terms']
        if last_formal_term != current_formal_term:
            term_change_list: DataFrame = term_change_list.append(
                {const.YEAR: current_row[const.YEAR], const.COUNTRY: country_name, 'last_term': last_formal_term,
                 'current_term': current_formal_term, 'change_type': 'formal'},
                ignore_index=True)

        if last_real_term != current_real_term:
            term_change_list: DataFrame = term_change_list.append(
                {const.YEAR: current_row[const.YEAR], const.COUNTRY: country_name, 'last_term': last_real_term,
                 'current_term': current_real_term, 'change_type': 'real'},
                ignore_index=True)
    return term_change_list


def construct_term_change_dummy(row):
    result_dict = {'longer_term': 0, 'shorter_term': 0, 'less_term': 0, 'more_term': 0, 'unlimited_terms': 0,
                   'limited_terms': 0}

    last_n_term, last_term_year = row['last_term'].split('x')
    current_n_term, current_term_year = row['current_term'].split('x')
    if current_term_year == 'N':
        if last_term_year != 'N':
            result_dict['longer_term'] = 1
            result_dict['unlimited_terms'] = 1
    elif last_term_year == 'N':
        result_dict['shorter_term'] = 1
        result_dict['limited_terms'] = 1
    elif last_term_year > current_term_year:
        result_dict['shorter_term'] = 1
    elif current_term_year > last_term_year:
        result_dict['longer_term'] = 1

    if current_n_term == 'N':
        if last_term_year != 'N':
            result_dict['more_term'] = 1
            result_dict['unlimited_terms'] = 1
    elif last_n_term == 'N':
        result_dict['less_term'] = 1
        result_dict['limited_terms'] = 1
    elif last_n_term > current_n_term:
        result_dict['less_term'] = 1
    elif current_n_term > last_n_term:
        result_dict['more_term'] = 1

    return pd.Series(result_dict)


if __name__ == '__main__':
    term_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, 'pres_limits_60_09_short.xlsx'))
    valid_term_df: DataFrame = term_df.loc[term_df[const.YEAR] >= 1981].copy()
    country_term_group = valid_term_df.groupby('ISO3N')

    country_term_change: DataFrame = country_term_group.apply(check_get_term_change).reset_index(drop=False).drop(
        ['level_0'], axis=1)
    country_term_change.to_excel(os.path.join(const.RESULT_PATH, '20200306_term_limit_change_event_list.xlsx'),
                                 index=False)

    # check if continue (not need to consider)
    continue_country = country_term_group.apply(check_if_continue_year)
