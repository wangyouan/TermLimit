#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_get_valid_presidential_country_list
# @Date: 2020/3/16
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SummarizeData.step03_get_valid_presidential_country_list
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200315_full_regression_data.pkl'))
    country_list = reg_df.loc[:, [const.COUNTRY_ISO3, const.FISCAL_YEAR]].drop_duplicates().rename(
        columns={const.FISCAL_YEAR: const.YEAR})

    pres_c_list: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, 'pres_limits_60_09_short.xlsx'))
    pres_c_valid: DataFrame = pres_c_list.loc[:, ['country', 'year', 'ISO3N']].rename(
        columns={'ISO3N': const.COUNTRY_ISO3N})

    country_info_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200316_country_info_list.pkl'))

    pres_c_info: DataFrame = pres_c_valid.replace({835: 834, 810: 643, 886: 887, 890: 688}).merge(
        country_info_df.drop(['Country'], axis=1).drop_duplicates(), on=[const.COUNTRY_ISO3N], how='left')
    pres_c_info.loc[:, 'is_presidential'] = 1
    pres_c_df: DataFrame = country_list.merge(pres_c_info, on=[const.COUNTRY_ISO3, const.YEAR], how='left')
    # pres_c_df.loc[:, 'is_presidential'] = pres_c_df.groupby(const.COUNTRY_ISO3)['is_presidential'].ffill()
    pres_c_df.loc[:, 'country'] = pres_c_df.groupby(const.COUNTRY_ISO3)['country'].ffill()
    pres_c_df.loc[:, const.COUNTRY_ISO3N] = pres_c_df.groupby(const.COUNTRY_ISO3)[const.COUNTRY_ISO3N].ffill()

    pres_c_df.to_excel(os.path.join(const.RESULT_PATH, '20200316_country_information.xlsx'), index=False)
