#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step08_append_epu_index
# @Date: 2020/3/26
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step08_append_epu_index
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.STATA_DATA_PATH, '20200326_term_limit_regression_data.dta'))
    epu_index: DataFrame = pd.read_pickle(
        os.path.join(const.DATABASE_PATH, 'PolicyUncertainty', 'epu_index.pkl')).rename(
        columns={'country': const.COUNTRY_ISO3, const.YEAR: const.FISCAL_YEAR})
    reg_df_epu: DataFrame = reg_df.merge(epu_index, on=[const.COUNTRY_ISO3, const.FISCAL_YEAR], how='left')
    reg_df_epu.loc[:, 'MV_1'] = reg_df.groupby(const.GVKEY)['MV'].shift(1)
    reg_df_epu.to_stata(os.path.join(const.STATA_DATA_PATH, '20200326_term_limit_regression_data2.dta'),
                        write_index=False, version=117)
