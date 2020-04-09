#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step11_try_to_remove_one_country_for_country_clusters
# @Date: 2020/4/9
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m ConstructRegressionFile.Stata.step11_try_to_remove_one_country_for_country_clusters
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const
from Utilities.generate_stata_code import generate_foreach2_dep_ind_code
from .step10_test_some_combination_of_control_variables import DEP_VARS

if __name__ == '__main__':
    # get valid country list
    data_path = os.path.join(const.STATA_DATA_PATH, '20200331_term_limit_regression_data.dta')
    f_ctrl_info = ['ln_at', 'LEVERAGE', 'ROA']
    c_ctrl_info = ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'FP_CPI_TOTL_ZG']
    real_ctrl = f_ctrl_info[:]
    real_ctrl.extend(c_ctrl_info)
    reg_df: DataFrame = pd.read_stata(data_path)
    valid_country_list = reg_df.dropna(subset=real_ctrl, how='any')[const.COUNTRY_ISO3].drop_duplicates()

    date_str = '20200409'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_remove_one_country_1.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_remove_one_country_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear',
                'use "{}"'.format(data_path),
                ]

    ind_list = ['Extend', 'ToUnlimit', 'Shrink', 'ToLimit']
    pre = 'formal'

    for country in valid_country_list:
        output_file = os.path.join(output_path, 'country_test_{}.xls'.format(country))
        ind_vars = ['{}_{}_3'.format(pre, suf) for suf in ind_list]

        cmd_list.extend(
            generate_foreach2_dep_ind_code(DEP_VARS, ' '.join(ind_vars), ' '.join(real_ctrl),
                                           fe_option='gvkey fyear',
                                           cluster_option='country_iso3n', output_path=output_file,
                                           condition='if indfmt != "FS" & country_iso3 != "{}"'.format(country),
                                           text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Country',
                                           data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
