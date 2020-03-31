#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step08_test_regression_with_unrest_variable
# @Date: 2020/3/31
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m ConstructRegressionFile.Stata.step08_test_regression_with_unrest_variable
"""

import os

from Constants import Constants as const
from .step07_test_regression_result_of_different_control import generate_foreach2_dep_code

COUNTRY_CTRL_LIST = [['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'unrestn'],
                     ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'unrestn'],
                     ['ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NY_GDP_MKTP_KD_ZG', 'unrestn'],
                     ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NY_GDP_MKTP_KD_ZG', 'unrestn'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NV_IND_TOTL_ZS',
                      'unrestn'],
                     ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NV_IND_TOTL_ZS', 'unrestn'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'unrestn'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'unrestn'],
                     ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'unrestn'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'NV_IND_TOTL_ZS', 'unrestn'],
                     ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'SL_UEM_TOTL_ZS', 'NV_IND_TOTL_ZS', 'unrestn'],
                     ]
FIRM_CTRL_LIST = ['ln_at', 'LEVERAGE', 'LOSS', 'SGA', 'FOREIGN', 'EBITDA']
DEP_VARS = 'CAPEX_1 R_B0_1 TANGIBILITY_1 ROA_1 SALE_RATIO_1 EMP_RATIO_1 ln_sale_1 ln_emp_1 TobinQ_1 MV_1'

if __name__ == '__main__':
    date_str = '20200331'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_preliminary_code_1.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_preliminary_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear',
                'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200331_term_limit_regression_data.dta')),
                ]

    ind_list = ['Extend', 'ToUnlimit', 'Shrink', 'ToLimit']

    for i, ctrl_info in enumerate(COUNTRY_CTRL_LIST):
        for pre in ['formal', 'real']:
            output_file = os.path.join(output_path, 'ctrl_test_{}_{}.xls'.format(i, pre))
            ind_vars = ['{}_{}_3'.format(pre, suf) for suf in ind_list]
            real_ctrl = FIRM_CTRL_LIST[:]
            real_ctrl.extend(ctrl_info)

            cmd_list.extend(
                generate_foreach2_dep_code(DEP_VARS, ' '.join(ind_vars), ' '.join(real_ctrl), fe_option='gvkey fyear',
                                           cluster_option='gvkey', output_path=output_file, condition='',
                                           text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                                           data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
