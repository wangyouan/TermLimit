#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step09_pretend_analysis
# @Date: 2020/4/3
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

from Constants import Constants as const
from Utilities.generate_stata_code import generate_foreach_dep_code

COUNTRY_CTRL_LIST = [['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG'],
                     ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG'],
                     ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NY_GDP_MKTP_KD_ZG'],
                     ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NV_IND_TOTL_ZS'],
                     ['ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'SL_UEM_TOTL_ZS'],
                     ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'SL_UEM_TOTL_ZS']
                     ]
FIRM_CTRL_LIST = ['ln_at', 'LEVERAGE', 'LOSS', 'SGA', 'EBITDA']
DEP_VARS = 'CAPEX_1 R_B0_1 TANGIBILITY_1 ROA_1 SALE_RATIO_1 EMP_RATIO_1 ln_sale_1 ln_emp_1 TobinQ_1 MV_1'

if __name__ == '__main__':
    date_str = '20200407'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_preliminary_code_1.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_preliminary_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear',
                'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200331_term_limit_regression_data.dta')),
                ]

    ind_list = ['Extend', 'Shrink']

    for i, ctrl_info in enumerate(COUNTRY_CTRL_LIST):
        for pre in ['formal']:
            for suf in ind_list:
                output_file = os.path.join(output_path, 'ctrl_test_{}_{}_{}.xls'.format(i, pre, suf))
                ind_vars = '{}_{}'.format(pre, suf)
                for j in range(1, 4):
                    ind_vars = '{pre}_{suf}_tm{j} {previous} {pre}_{suf}_t{j}'.format(pre=pre, suf=suf, j=j,
                                                                                      previous=ind_vars)

                real_ctrl = FIRM_CTRL_LIST[:]
                real_ctrl.extend(ctrl_info)

                cmd_list.extend(
                    generate_foreach_dep_code(DEP_VARS, ind_vars, ' '.join(real_ctrl),
                                              fe_option='gvkey fyear',
                                              cluster_option='gvkey', output_path=output_file, condition='',
                                              text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                                              data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
