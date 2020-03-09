#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step05_construct_makret_value_information
# @Date: 2020/3/9
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructVariable.step05_construct_makret_value_information
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    fiscal_end_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '198706_202003_global_compustat_all_fiscal_end.zip'))
    sec_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '19851231_20200308_ctat_global_price.zip'))
    sec_df.loc[:, 'datadate'] = pd.to_datetime(sec_df['datadate'], format='%Y%m%d')
    sec_df_monthly: DataFrame = sec_df.groupby([const.GVKEY, pd.Grouper(key='datadate', freq='M')]).last()
    sec_df_monthly = sec_df_monthly.reset_index(drop=False)
    sec_df_monthly.loc[:, const.YEAR] = sec_df_monthly['datadate'].dt.year
    sec_df_monthly.loc[:, const.MONTH] = sec_df_monthly['datadate'].dt.month

    fis_valid_df: DataFrame = fiscal_end_df.drop_duplicates(subset=[const.GVKEY, 'fyear'], keep='last')
    fis_valid_df.loc[:, 'datadate'] = pd.to_datetime(fis_valid_df['datadate'], format='%Y%m%d')
    fis_valid_df.loc[:, const.YEAR] = fis_valid_df['datadate'].dt.year
    fis_valid_df.loc[:, const.MONTH] = fis_valid_df['datadate'].dt.month

    fiscal_end_df_2: DataFrame = fis_valid_df.merge(
        sec_df_monthly.loc[:, [const.GVKEY, const.YEAR, const.MONTH, 'prccd']],
        on=[const.GVKEY, const.YEAR, const.MONTH])
    ctat_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200309_ctat_global_all_ctrl_vars.pkl'))
    ctat_df_prc: DataFrame = ctat_df.merge(fiscal_end_df_2.loc[:, ['fyear', const.GVKEY, 'prccd']],
                                           on=['fyear', const.GVKEY], how='left')
    ctat_df_prc.loc[:, 'mkvalt'] = ctat_df_prc['prccd'] * ctat_df_prc['cshoi']
    ctat_df_prc.loc[:, 'MV'] = ctat_df_prc['mkvalt'].apply(np.log)
    ctat_df_prc.loc[:, 'TobinQ'] = (ctat_df_prc['at'] + ctat_df_prc['mkvalt'] - ctat_df_prc['ceq']) / ctat_df_prc['at']

    ctat_df_prc_valid: DataFrame = ctat_df_prc.replace([np.inf, -np.inf], np.nan)
    ctat_df_prc_valid.to_pickle(os.path.join(const.TEMP_PATH, '20190309_regression_control_variables.pkl'))
