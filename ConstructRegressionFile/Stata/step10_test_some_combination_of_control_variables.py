#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step10_test_some_combination_of_control_variables
# @Date: 2020/4/7
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m ConstructRegressionFile.Stata.step08_test_regression_with_unrest_variable
"""

import os

from Constants import Constants as const
from Utilities.generate_stata_code import generate_foreach2_dep_ind_code

COUNTRY_CTRL_LIST = [['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG'],
                     ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG'],
                     ['ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NY_GDP_MKTP_KD_ZG'],
                     ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NY_GDP_MKTP_KD_ZG'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NV_IND_TOTL_ZS'],
                     ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NV_IND_TOTL_ZS'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'FP_CPI_TOTL_ZG'],
                     ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'FP_CPI_TOTL_ZG'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'NV_IND_TOTL_ZS', 'FP_CPI_TOTL_ZG'],
                     ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'NV_IND_TOTL_ZS', 'FP_CPI_TOTL_ZG'],
                     ]
FIRM_CTRL_LIST = [['ln_at', 'LEVERAGE', 'LOSS', 'SGA', 'FOREIGN', 'EBITDA'],
                  ['ln_at', 'LEVERAGE', 'ROA'],
                  ['ln_at', 'LEVERAGE', 'TobinQ'],
                  ['ln_at', 'LEVERAGE', 'ln_emp', 'ROA', 'LOSS'],
                  ['ln_at', 'LEVERAGE', 'SALE_RATIO', 'TobinQ', 'TANGIBILITY'],
                  ['ln_at', 'LEVERAGE', 'SALE_RATIO', 'TobinQ', 'TANGIBILITY', 'LOSS', 'FOREIGN'],
                  ['ln_at', 'LEVERAGE', 'SALE_RATIO', 'TobinQ', 'TANGIBILITY', 'LOSS', 'FOREIGN_EXPO'],
                  ['ln_at', 'LEVERAGE', 'LOSS', 'SGA', 'FOREIGN_EXPO', 'EBITDA'],
                  ['ln_at', 'LEVERAGE', 'LOSS', 'SGA', 'FOREIGN_EXPO', 'ROA'],
                  ['ln_at', 'LEVERAGE', 'LOSS', 'SGA', 'FOREIGN', 'ROA'],
                  ['ln_at', 'LEVERAGE', 'LOSS', 'ln_sale', 'FOREIGN', 'ROA'],
                  ['ln_at', 'LEVERAGE', 'LOSS', 'ln_sale', 'FOREIGN', 'PTBI'],
                  ['ln_at', 'LEVERAGE', 'LOSS', 'ln_sale', 'FOREIGN', 'PTBI', 'CASH_HOLDING'],
                  ['ln_at', 'LEVERAGE', 'LOSS', 'ln_sale', 'FOREIGN', 'ROA', 'CASH_HOLDING'],
                  ['ln_at', 'LEVERAGE', 'LOSS', 'FOREIGN', 'ROA', 'CASH_RATIO'],
                  ]
DEP_VARS = 'CAPEX_1 R_B0_1 TANGIBILITY_1 ROA_1 SALE_RATIO_1 EMP_RATIO_1 ln_sale_1 ln_emp_1 TobinQ_1 MV_1'

if __name__ == '__main__':
    date_str = '20200407'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_preliminary_code_3.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_preliminary_3'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear',
                'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200331_term_limit_regression_data.dta')),
                ]

    ind_list = ['Extend', 'ToUnlimit', 'Shrink', 'ToLimit']

    i = 0
    for c_ctrl_info in COUNTRY_CTRL_LIST:
        for f_ctrl_info in FIRM_CTRL_LIST:
            for pre in ['formal', 'real']:
                output_file = os.path.join(output_path, 'ctrl_test_{}_{}.xls'.format(i, pre))
                ind_vars = ['{}_{}_3'.format(pre, suf) for suf in ind_list]
                real_ctrl = f_ctrl_info[:]
                real_ctrl.extend(c_ctrl_info)

                cmd_list.extend(
                    generate_foreach2_dep_ind_code(DEP_VARS, ' '.join(ind_vars), ' '.join(real_ctrl),
                                                   fe_option='gvkey fyear',
                                                   cluster_option='gvkey', output_path=output_file, condition='',
                                                   text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                                                   data_description='tstat bdec(4) tdec(4) rdec(4)'))
            i += 1

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
