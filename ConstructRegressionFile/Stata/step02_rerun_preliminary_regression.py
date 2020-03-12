#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_rerun_preliminary_regression
# @Date: 2020/3/10
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructVariable.step02_rerun_preliminary_regression
"""

import os

from Constants import Constants as const

IND_VARS = [' '.join(
    ['formal_Extend_tm3', 'formal_Extend_tm2', 'formal_Extend_tm1', 'formal_Extend', 'formal_Extend_t1',
     'formal_Extend_t2', 'formal_Extend_t3', 'formal_Extend_t4', 'formal_Extend_t5']),
    ' '.join(
        ['formal_Shrink_tm3', 'formal_Shrink_tm2', 'formal_Shrink_tm1', 'formal_Shrink', 'formal_Shrink_t1',
         'formal_Shrink_t2', 'formal_Shrink_t3', 'formal_Shrink_t4', 'formal_Shrink_t5']),
    ' '.join(
        ['real_Shrink_tm3', 'real_Shrink_tm2', 'real_Shrink_tm1', 'real_Shrink', 'real_Shrink_t1',
         'real_Shrink_t2', 'real_Shrink_t3', 'real_Shrink_t4', 'real_Shrink_t5']),
    ' '.join(
        ['real_Extend_tm3', 'real_Extend_tm2', 'real_Extend_tm1', 'real_Extend', 'real_Extend_t1',
         'real_Extend_t2', 'real_Extend_t3', 'real_Extend_t4', 'real_Extend_t5']),
    ' '.join(
        ['formal_ToLimit_tm3', 'formal_ToLimit_tm2', 'formal_ToLimit_tm1', 'formal_ToLimit', 'formal_ToLimit_t1',
         'formal_ToLimit_t2', 'formal_ToLimit_t3', 'formal_ToLimit_t4', 'formal_ToLimit_t5']),
    ' '.join(
        ['formal_ToUnlimit_tm3', 'formal_ToUnlimit_tm2', 'formal_ToUnlimit_tm1', 'formal_ToUnlimit',
         'formal_ToUnlimit_t1',
         'formal_ToUnlimit_t2', 'formal_ToUnlimit_t3', 'formal_ToUnlimit_t4', 'formal_ToUnlimit_t5']),
    ' '.join(
        ['real_ToUnlimit_tm3', 'real_ToUnlimit_tm2', 'real_ToUnlimit_tm1', 'real_ToUnlimit', 'real_ToUnlimit_t1',
         'real_ToUnlimit_t2', 'real_ToUnlimit_t3', 'real_ToUnlimit_t4', 'real_ToUnlimit_t5']),
    ' '.join(
        ['real_ToLimit_tm3', 'real_ToLimit_tm2', 'real_ToLimit_tm1', 'real_ToLimit', 'real_ToLimit_t1',
         'real_ToLimit_t2', 'real_ToLimit_t3', 'real_ToLimit_t4', 'real_ToLimit_t5']),
]
DEP_VARS = ['{}_1'.format(i) for i in ['CAPEX', 'EBITDA', 'PTBI', 'ROA', 'R_B', 'LEVERAGE', 'CASH_HOLDING',
                                       'TANGIBILITY', 'TobinQ', 'ln_emp', 'ln_sale']]
CTRL_VARS = 'ln_at SGA TANGIBILITY CAPEX FOREIGN PTBI VOL_PTBI'


def generate_regression_code(dep, ind, ctrl, fe_option, cluster_option, output_path, text_option, data_description,
                             condition=''):
    return ['capture qui reghdfe {dep} {ind} {ctrl} {condition}, absorb({fe}) cl({cl})'.format(
        dep=dep, ind=ind, ctrl=ctrl, fe=fe_option, cl=cluster_option, condition=condition),
        'outreg2 using {output_file}, addtext({output_text}) {dataconfig} nolabel append'.format(
            output_file=output_path, output_text=text_option,
            dataconfig=data_description), '']


if __name__ == '__main__':
    date_str = '20200310'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_preliminary_code_1.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_preliminary_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear', 'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200310_regression_data.dta'))]

    for ind_key in IND_VARS:
        output_file = os.path.join(output_path, '{}.txt'.format(ind_key.split(' ')[3]))
        for dep_key in DEP_VARS:
            cmd_list.extend(generate_regression_code(dep=dep_key, ind=ind_key, ctrl=CTRL_VARS, fe_option='gvkey fyear',
                                                     cluster_option='gvkey', output_path=output_file,
                                                     text_option='Firm Dummy, Yes, Year Dummy, Yes, Cluster, Firm',
                                                     data_description='tstat bdec(4) tdec(4) rdec(4)'))

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
