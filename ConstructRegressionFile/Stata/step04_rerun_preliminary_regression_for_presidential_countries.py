#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step04_rerun_preliminary_regression_for_presidential_countries
# @Date: 2020/3/20
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m ConstructRegressionFile.Stata.step04_rerun_preliminary_regression_for_presidential_countries
"""

import os

from Constants import Constants as const
from .step02_rerun_preliminary_regression import generate_regression_code

DEP_VARS = ['{}_1'.format(i) for i in
            ['CAPEX', 'ROA', 'R_B', 'CASH_HOLDING', 'TANGIBILITY', 'TobinQ', 'ln_emp', 'ln_sale']]

CTRL_VARS = 'ln_at SGA TANGIBILITY CAPEX ROA ln_GDP ln_GDP_PC NY_GDP_MKTP_KD_ZG'

if __name__ == '__main__':
    ind_vars = list()
    for suf in ['Extend', 'ToUnlimit', 'ToLimit', 'Shrink']:
        for pre in ['formal', 'real']:
            real_key = '{}_{}'.format(pre, suf)
            ind_list = [real_key]
            for n in range(1, 6):
                if n < 4:
                    ind_list.insert(0, '{}_b{}'.format(real_key, n))
                ind_list.append('{}_a{}'.format(real_key, n))
            ind_vars.append(' '.join(ind_list))

    date_str = '20200320'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_preliminary_code_1.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_preliminary_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear', 'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200320_term_limit_regression_data.dta'))]

    for ind_key in ind_vars:
        key_info = ind_key.split(' ')[0][:-3]
        output_file = os.path.join(output_path, '{}.txt'.format(key_info))
        for dep_key in DEP_VARS:
            cmd_list.extend(generate_regression_code(dep=dep_key, ind=ind_key, ctrl=CTRL_VARS, fe_option='gvkey fyear',
                                                     cluster_option='gvkey', output_path=output_file, condition='',
                                                     text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                                                     data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
