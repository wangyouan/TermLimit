#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_append_employment_related_variables
# @Date: 2020/3/9
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step02_append_employment_related_variables
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.STATA_DATA_PATH, '20200309_regression_data.dta'))
    reg_df.loc[:, 'ln_emp'] = reg_df['emp'].apply(np.log)

    reg_df.loc[:, 'ln_emp_1'] = reg_df.groupby(const.GVKEY)['ln_emp'].shift(1)
    reg_df.replace([np.inf, -np.inf], np.nan).to_stata(
        os.path.join(const.STATA_DATA_PATH, '20200309_regression_data.dta'), write_index=False, version=117)
