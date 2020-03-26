#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step04_construct_required_variables
# @Date: 2020/3/8
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructVariable.step04_construct_required_variables
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    ctat_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '198706_202003_global_compustat_all_fina_data.zip'))
    ctat_df: DataFrame = ctat_df.sort_values(by=['datadate'], ascending=True).drop_duplicates(
        subset=[const.GVKEY, 'fyear'], keep='last')
    ctat_df.loc[:, 'lag_at'] = ctat_df.groupby(['gvkey'])['at'].shift(1)
    ctat_df.loc[:, 'ln_at'] = ctat_df['at'].apply(np.log)
    ctat_df.loc[:, 'CAPEX'] = ctat_df['capx'] / ctat_df['lag_at']
    ctat_df.loc[:, 'EBITDA'] = ctat_df['ebitda'] / ctat_df['lag_at']
    ctat_df.loc[:, 'PTBI'] = ctat_df['pi'] / ctat_df['lag_at']
    ctat_df.loc[:, 'R_B'] = ctat_df['xrd'] / ctat_df['lag_at']
    ctat_df.loc[:, 'sale_diff'] = ctat_df.groupby(const.GVKEY)['sale'].diff()
    ctat_df.loc[:, 'SGA'] = ctat_df['sale_diff'] / ctat_df['lag_at']
    ctat_df.loc[:, 'SHARES_OUT'] = ctat_df['cshoi'].apply(np.log)
    ctat_df.loc[:, 'ipodate'] = ctat_df.groupby(const.GVKEY)['ipodate'].bfill()
    ctat_df.loc[:, 'ipodate'] = ctat_df.groupby(const.GVKEY)['ipodate'].ffill()

    ctat_df.loc[:, 'std_pi'] = ctat_df.groupby(const.GVKEY)['pi'].rolling(5).std().values
    ctat_df.loc[:, 'std_ebitda'] = ctat_df.groupby(const.GVKEY)['ebitda'].rolling(5).std().values
    ctat_df.loc[:, 'VOL_PTBI'] = ctat_df['std_pi'] / ctat_df['lag_at']
    ctat_df.loc[:, 'VOL_EBITDA'] = ctat_df['std_ebitda'] / ctat_df['lag_at']
    ctat_df.loc[:, 'ROA'] = ctat_df['nicon'] / ctat_df['lag_at']
    ctat_df.loc[:, 'LOSS'] = (ctat_df['ib'] < 0).astype(int)
    ctat_df.loc[:, 'LEVERAGE'] = (ctat_df['dltt'] + ctat_df['dlc']) / ctat_df['lag_at']
    ctat_df.loc[:, 'FOREIGN_EXPO'] = ctat_df['fca'].notnull().astype(int)
    ctat_df.loc[:, 'FOREIGN'] = (ctat_df['fca'] > 0).astype(int).fillna(0)
    ctat_df.loc[:, 'CASH_HOLDING'] = ctat_df['che'] / ctat_df['lag_at']
    ctat_df.loc[:, 'TANGIBILITY'] = ctat_df['ppent'] / ctat_df['lag_at']
    ctat_df.loc[:, 'CASH_RATIO'] = ctat_df['ch'] / ctat_df['lag_at']
    ctat_df.loc[:, 'SALE_RATIO'] = ctat_df['sale'] / ctat_df['lag_at']

    ctat_df.to_pickle(os.path.join(const.TEMP_PATH, '20200309_ctat_global_all_ctrl_vars.pkl'))
