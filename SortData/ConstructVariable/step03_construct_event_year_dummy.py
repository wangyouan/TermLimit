#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_construct_event_year_dummy
# @Date: 2020/3/8
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructVariable.step03_construct_event_year_dummy
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const


def construct_event_row_information(event_tmp_df):
    row_dict = dict()
    event_type = None
    for i in event_tmp_df.index:
        event_type = event_tmp_df.loc[i, 'change_type']
        for key in ['last_term', 'current_term', 'Extend', 'ToUnlimit', 'ToLimit']:
            row_dict['{}_{}'.format(event_type, key)] = event_tmp_df.loc[i, key]

        row_dict['{}_Shrink'.format(event_type)] = 1 - row_dict['{}_Extend'.format(event_type)]
        if event_type == 'formal':
            row_dict['RealConsist'] = event_tmp_df.loc[i, 'Consistent With Real']

    if event_tmp_df.shape[0] != 1:
        return pd.Series(row_dict)

    if event_type == 'formal':
        other_type = 'real'
        row_dict['RealConsist'] = 0

    else:
        other_type = 'formal'

    for key in ['last_term', 'current_term', 'Extend', 'ToUnlimit', 'ToLimit', 'Shrink']:
        row_dict['{}_{}'.format(other_type, key)] = 0

    return pd.Series(row_dict)


if __name__ == '__main__':
    event_df: DataFrame = pd.read_excel(os.path.join(const.RESULT_PATH, '20200307_term_limit_change_event_list.xlsx'))
    event_df.loc[:, 'EventYear'] = event_df['EventYear'].fillna(event_df['year'])

    annual_event_df: DataFrame = event_df.groupby(['ISO3N', 'EventYear']).apply(
        construct_event_row_information).reset_index(drop=False).drop(['level_2'], axis=1).fillna(0).rename(
        columns={'ISO3N': const.COUNTRY_ISO3N})
    country_code: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'countries_codes_and_coordinates.csv')).rename(
        columns={'Alpha-2 code': 'country_iso2', 'Alpha-3 code': const.COUNTRY_ISO3,
                 'Numeric code': const.COUNTRY_ISO3N})
    for key in 'country_iso2	country_iso3	country_iso3n	Latitude (average)	Longitude (average)'.split('\t'):
        country_code.loc[:, key] = country_code[key].str.strip(' "')
    country_code.loc[:, const.COUNTRY_ISO3N] = country_code[const.COUNTRY_ISO3N].astype(int)
    country_code.drop_duplicates(subset=['country_iso3n'], inplace=True)
    annual_event_df.loc[:, const.COUNTRY_ISO3N] = annual_event_df[const.COUNTRY_ISO3N].replace(
        {835: 834, 810: 643, 886: 887, 890: 688})

    ann_df: DataFrame = annual_event_df.merge(country_code, on=[const.COUNTRY_ISO3N])
    ann_df.to_pickle(os.path.join(const.TEMP_PATH, '20200309_annual_event_data.pkl'))
