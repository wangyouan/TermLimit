#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step05_rerun_preliminary_regression_with_single_variable
# @Date: 2020/3/20
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


"""
python -m ConstructRegressionFile.Stata.step04_rerun_preliminary_regression_for_presidential_countries
"""

import os

from Constants import Constants as const
from .step02_rerun_preliminary_regression import generate_regression_code
from .step04_rerun_preliminary_regression_for_presidential_countries import DEP_VARS

CTRL_VARS = 'ln_at TANGIBILITY CAPEX ROA ln_GDP ln_GDP_PC NY_GDP_MKTP_KD_ZG SL_UEM_TOTL_ZS ln_POPULATION NE_IMP_GNFS_ZS'

if __name__ == '__main__':
    date_str = '20200320'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_preliminary_code_5.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_preliminary_5'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear',
                'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200320_term_limit_regression_data.dta')),
                'replace R_B_1 = 0 if missing(R_B_1)']

    ind_vars = list()
    for suf in ['Extend', 'ToUnlimit', 'ToLimit', 'Shrink']:
        for pre in ['formal', 'real']:
            ind_vars.append('{}_{}'.format(pre, suf))

    for ind_key in ind_vars:
        for lag in range(5):
            real_key = '{}_{}'.format(ind_key, lag + 1) if lag != 0 else ind_key
            output_file = os.path.join(output_path, '{}.txt'.format(real_key))
            for dep_key in DEP_VARS:
                cmd_list.extend(
                    generate_regression_code(dep=dep_key, ind=real_key, ctrl=CTRL_VARS, fe_option='gvkey fyear',
                                             cluster_option='gvkey', output_path=output_file, condition='',
                                             text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                                             data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
