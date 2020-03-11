#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step04_add_firm_year_count
# @Date: 2020/3/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


"""
python -m SortData.ConstructRegressionDataset.step04_add_firm_year_count
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.STATA_DATA_PATH, '20200310_regression_data.dta'))
    country_year_count = reg_df.groupby([const.COUNTRY_ISO3, const.FISCAL_YEAR])[const.GVKEY].count().reset_index(
        drop=False).rename(columns={const.GVKEY: 'firm_num'})
    reg_df_with_fc: DataFrame = reg_df.merge(country_year_count, on=[const.COUNTRY_ISO3, const.FISCAL_YEAR])
    reg_df_with_fc.to_pickle(os.path.join(const.TEMP_PATH, '20200311_regression_data_with_count.pkl'))
