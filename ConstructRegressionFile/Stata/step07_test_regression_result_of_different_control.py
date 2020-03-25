#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step07_test_regression_result_of_different_control
# @Date: 2020/3/25
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m ConstructRegressionFile.Stata.step07_test_regression_result_of_different_control
"""

import os

from Constants import Constants as const

CTRL_LIST = [['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT', 'NV_IND_TOTL_ZS'],
             ['ln_GDP', 'ln_GDP_PC', 'NE_EXP_GNFS_KD_ZG', 'NE_IMP_GNFS_KD_ZG'],
             ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG'],
             ['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT', 'NV_IND_MANF_ZS', 'NY_GDP_MKTP_KD_ZG'],
             ['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT', 'NV_IND_MANF_ZS', 'SL_UEM_TOTL_ZS'],
             ['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT', 'NV_IND_MANF_ZS'],
             ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG', 'ln_IMPORT', 'ln_EXPORT', 'NV_IND_TOTL_ZS'],
             ['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT', 'NV_IND_TOTL_ZS', 'SL_UEM_TOTL_ZS'],
             ]
DEP_VARS = 'TobinQ_1 TANGIBILITY_1 ROA_1 R_B0_1 CASH_HOLDING_1 CAPEX_1 ln_sale_1 ln_emp_1'


def generate_foreach2_dep_code(dep, ind, ctrl, fe_option, cluster_option, output_path, text_option,
                               data_description, condition=''):
    return ['foreach dep_var in {}{{'.format(dep),
            'foreach ind_var in {}{{'.format(ind),
            "capture qui reghdfe `dep_var' `ind_var' {ctrl} {condition}, absorb({fe}) cl({cl})".format(
                dep=dep, ctrl=ctrl, fe=fe_option, cl=cluster_option, condition=condition),
            'outreg2 using "{output_file}", addtext({output_text}) {dataconfig} nolabel append'.format(
                output_file=output_path, output_text=text_option,
                dataconfig=data_description),
            '}\n}\n']


if __name__ == '__main__':
    date_str = '20200325'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_preliminary_code_1.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_preliminary_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear',
                'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200324_term_limit_regression_data.dta')),
                ]

    ind_vars = list()
    for suf in ['Extend', 'ToUnlimit', 'ToLimit', 'Shrink']:
        for pre in ['formal', 'real']:
            ind_vars.append('{}_{}'.format(pre, suf))

    for i, ctrl_info in enumerate(CTRL_LIST):
        output_file = os.path.join(output_path, 'ctrl_test_{}.xls'.format(i))

        cmd_list.extend(generate_foreach2_dep_code(DEP_VARS, DEP_VARS, ' '.join(ctrl_info), fe_option='gvkey fyear',
                                                   cluster_option='gvkey', output_path=output_file, condition='',
                                                   text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                                                   data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
