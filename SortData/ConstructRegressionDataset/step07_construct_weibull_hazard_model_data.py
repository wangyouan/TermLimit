#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step07_construct_weibull_hazard_model_data
# @Date: 2020/3/23
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step07_construct_weibull_hazard_model_data
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const
from ConstructRegressionFile.Stata.step04_rerun_preliminary_regression_for_presidential_countries import DEP_VARS

COUNTRY_CTRLS = ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'ln_POPULATION', 'NE_IMP_GNFS_ZS',
                 'NE_EXP_GNFS_ZS']

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.STATA_DATA_PATH, '20200320_term_limit_regression_data.dta'))
    reg_df.loc[:, 'R_B0_1'] = reg_df['R_B_1'].fillna(0)
    valid_reg_df: DataFrame = reg_df.loc[reg_df['is_presidential'] == 1].copy()
    valid_reg_df.to_stata(os.path.join(const.STATA_DATA_PATH, '20200324_term_limit_regression_data.dta'), version=117,
                          write_index=False)
    country_year_df: DataFrame = valid_reg_df.loc[:,
                                 [const.COUNTRY_ISO3, const.FISCAL_YEAR, 'has_event']].drop_duplicates()
    country_year_df.loc[:, 'post_event'] = country_year_df['has_event'].replace(0, np.nan)
    country_year_df.sort_values(by=[const.FISCAL_YEAR], ascending=True, inplace=True)
    country_year_df.loc[:, 'post_event'] = country_year_df.groupby(const.COUNTRY_ISO3).ffill().fillna(0)

    country_level_ctrl: DataFrame = valid_reg_df.groupby([const.COUNTRY_ISO3, const.FISCAL_YEAR])[COUNTRY_CTRLS].first()
    dep_average_df: DataFrame = valid_reg_df.groupby([const.COUNTRY_ISO3, const.FISCAL_YEAR])[DEP_VARS].mean()

    valid_country_year_df: DataFrame = country_year_df.loc[country_year_df['post_event'] != 0].copy()
    wh_reg_df: DataFrame = valid_country_year_df.merge(country_level_ctrl.reset_index(drop=False),
                                                       on=[const.COUNTRY_ISO3, const.FISCAL_YEAR], how='inner').merge(
        dep_average_df.reset_index(drop=False), on=[const.COUNTRY_ISO3, const.FISCAL_YEAR], how='inner')
    wh_reg_df.to_stata(os.path.join(const.STATA_DATA_PATH, '20200324_weibull_harzard_model_data.dta'),
                       write_index=False, version=117)
