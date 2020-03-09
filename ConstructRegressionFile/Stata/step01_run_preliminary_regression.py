#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_run_preliminary_regression
# @Date: 2020/3/9
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructVariable.step01_check_valid_country_list
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    save_file = os.path.join(const.STATA_CODE_PATH, '20200309_preliminary_code_3.do')
    output_path = os.path.join(const.STATA_RESULT_PATH, '20200309_preliminary_3')
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear', 'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200309_regression_data.dta'))]
    ctrl_vars = 'ln_at SGA TANGIBILITY CAPEX FOREIGN'

    for ind_key in ['formal_Extend', 'real_Extend', 'formal_Shrink', 'real_Shrink']:
        for lag in range(5):
            real_ind = '{}_{}'.format(ind_key, lag + 1) if lag != 0 else ind_key
            output_file = os.path.join(output_path, '{}.txt'.format(real_ind))
            for dep in ['CAPEX', 'R_B', 'ROA', 'LEVERAGE', 'CASH_HOLDING', 'TANGIBILITY', 'TobinQ', 'ln_emp']:
                real_dep = "{}_1".format(dep)

                cmd_list.append('capture qui reghdfe {dep} {ind} {ctrl}, absorb(gvkey fyear) cl(gvkey)'.format(
                    dep=real_dep, ind=real_ind, ctrl=ctrl_vars))
                cmd_list.append(
                    'outreg2 using {output_file}, addtext({output_text}) {dataconfig} nolabel append'.format(
                        output_file=output_file, output_text='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                        dataconfig='tstat bdec(4) tdec(4) rdec(4)'))
                cmd_list.append('')

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
