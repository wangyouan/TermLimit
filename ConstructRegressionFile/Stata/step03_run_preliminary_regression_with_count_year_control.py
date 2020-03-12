#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_run_preliminary_regression_with_count_year_control
# @Date: 2020/3/12
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m ConstructRegressionFile.Stata.step03_run_preliminary_regression_with_count_year_control
"""

import os

from Constants import Constants as const
from .step02_rerun_preliminary_regression import generate_regression_code, DEP_VARS

CTRL_VARS = 'ln_at SGA TANGIBILITY CAPEX PTBI VOL_PTBI ln_GDP ln_GDP_PC GC_TAX_TOTL_GD_ZS FP_CPI_TOTL_ZG FR_INR_RINR'
IND_VARS = ['formal_Extend_3', 'real_Extend_3', 'formal_Shrink_3', 'real_Shrink_3']
CONDITION = 'if firm_num >= 100'

if __name__ == '__main__':
    date_str = '20200312'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_preliminary_code_1.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_preliminary_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear', 'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200311_regression_data.dta'))]

    for ind_key in IND_VARS:
        output_file = os.path.join(output_path, '{}.txt'.format(ind_key.split(' ')[3]))
        for dep_key in DEP_VARS:
            cmd_list.extend(generate_regression_code(dep=dep_key, ind=ind_key, ctrl=CTRL_VARS, fe_option='gvkey fyear',
                                                     cluster_option='gvkey', output_path=output_file,
                                                     condition=CONDITION,
                                                     text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                                                     data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
