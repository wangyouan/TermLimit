#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step09_append_unrest_variable
# @Date: 2020/3/31
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step09_append_unrest_variable
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.STATA_DATA_PATH, '20200326_term_limit_regression_data2.dta'))
    reg_df.loc[:, 'EMP_RATIO'] = reg_df['emp'] / reg_df['lag_at']
    da_reg_df: DataFrame = pd.read_stata(os.path.join(const.DATA_PATH, 'Acemolgu', 'DDCGdata_final.dta')).loc[:,
                           ['wbcode', const.YEAR, 'unrest', 'unrestn', 'unrestreg']].rename(
        columns={'wbcode': const.COUNTRY_ISO3, const.YEAR: const.FISCAL_YEAR})
    reg_df_rest: DataFrame = reg_df.merge(da_reg_df, on=[const.COUNTRY_ISO3, const.FISCAL_YEAR], how='left')
    reg_df_rest_valid: DataFrame = reg_df_rest.replace([np.inf, -np.inf], np.nan)
    reg_df_rest_valid.loc[reg_df_rest_valid['EMP_RATIO'].notnull(), 'EMP_RATIO'] = winsorize(
        reg_df_rest_valid['EMP_RATIO'].dropna(), (0.01, 0.01))
    reg_df_rest_valid.loc[:, 'EMP_RATIO_1'] = reg_df_rest_valid.groupby(const.GVKEY)['EMP_RATIO'].shift(1)
    reg_df_rest_valid.to_stata(os.path.join(const.STATA_DATA_PATH, '20200331_term_limit_regression_data.dta'),
                               write_index=False, version=117)
