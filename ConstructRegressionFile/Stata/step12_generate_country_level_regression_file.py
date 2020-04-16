#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step12_generate_country_level_regression_file
# @Date: 2020/4/16
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m ConstructRegressionFile.Stata.step12_generate_country_level_regression_file
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const
from Utilities.generate_stata_code import generate_foreach2_dep_ind_code

if __name__ == '__main__':
    date_str = '20200416'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_country_reg_code_2.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_country_reg_code_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    data_path = os.path.join(const.STATA_DATA_PATH, '20200415_country_year_reg_data.dta')

    cmd_list = ['clear', 'use "{}"'.format(data_path)]

    ind_list = ['Extend', 'ToUnlimit', 'Shrink', 'ToLimit']
    c_ctrl_info = ['ln_GDP', 'ln_GDP_PC', 'UNEMP_RATE', 'GDP_GROWTH']

    data_df: DataFrame = pd.read_stata(data_path)
    dep_keys = [i for i in data_df.keys() if
                i.endswith("_1") and not i.startswith('formal') and not i.startswith('real') and i not in {
                    'BUS_SCORE_1'}]

    for pre in ['formal', 'real']:
        output_file = os.path.join(output_path, 'country_result_{}.xls'.format(pre))
        ind_vars = ['{}_{}_post2'.format(pre, suf) for suf in ind_list]
        real_ctrl = ' '.join(c_ctrl_info)

        cmd_list.extend(
            generate_foreach2_dep_ind_code(' '.join(dep_keys), ' '.join(ind_vars), real_ctrl,
                                           fe_option='{} fyear'.format(const.COUNTRY_ISO3),
                                           cluster_option=const.COUNTRY_ISO3, output_path=output_file, condition='',
                                           text_option='Country Dummy, Yes, Year Dummy, Yes, Cluster, Country',
                                           data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
