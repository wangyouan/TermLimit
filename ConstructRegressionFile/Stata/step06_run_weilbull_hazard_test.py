#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step06_run_weilbull_hazard_test
# @Date: 2020/3/25
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m ConstructRegressionFile.Stata.step06_run_weilbull_hazard_test
"""

import os

from Constants import Constants as const

if __name__ == '__main__':
    date_str = '20200325'
    save_file = os.path.join(const.STATA_CODE_PATH, '{}_wh_code_1.do'.format(date_str))
    output_path = os.path.join(const.STATA_RESULT_PATH, '{}_wh_1'.format(date_str))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    cmd_list = ['clear',
                'use "{}"'.format(os.path.join(const.STATA_DATA_PATH, '20200324_weibull_harzard_model_data.dta')),
                'stset fyear, f(post_event) id(country_iso3)']

    ctrl_list = [['ln_GDP', 'ln_GDP_PC'],
                 ['ln_GDP', 'ln_GDP_PC', 'NY_GDP_MKTP_KD_ZG'],
                 ['ln_GDP', 'ln_GDP_PC', 'NE_EXP_GNFS_KD_ZG', 'NE_IMP_GNFS_KD_ZG'],
                 ['ln_GDP', 'ln_GDP_PC', 'NE_EXP_GNFS_KD_ZG', 'NE_IMP_GNFS_KD_ZG', 'SL_UEM_TOTL_ZS'],
                 ['ln_GDP', 'ln_GDP_PC', 'NE_EXP_GNFS_KD_ZG', 'NE_IMP_GNFS_KD_ZG', 'FP_CPI_TOTL_ZG', 'SL_UEM_TOTL_ZS'],
                 ['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT'],
                 ['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT', 'NV_IND_TOTL_ZS'],
                 ['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT', 'SL_UEM_TOTL_ZS'],
                 ['ln_GDP', 'ln_GDP_PC', 'ln_IMPORT', 'ln_EXPORT', 'SL_UEM_TOTL_ZS', 'FP_CPI_TOTL_ZG'],
                 ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'NE_EXP_GNFS_KD_ZG', 'NE_IMP_GNFS_KD_ZG'],
                 ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS'],
                 ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'SL_UEM_TOTL_ZS'],
                 ['ln_GDP', 'ln_GDP_PC', 'NE_IMP_GNFS_ZS', 'NE_EXP_GNFS_ZS', 'SL_UEM_TOTL_ZS', 'FP_CPI_TOTL_ZG']]
    dep_vars = 'TobinQ_1 TANGIBILITY_1 ROA_1 R_B0_1 CASH_HOLDING_1 CAPEX_1 ln_sale_1 ln_emp_1'
    output_option = 'addtext(Cluster, Country) pvalue bdec(4) pdec(4) rdec(4) addstat(chi-square test, e(chi2)) ' \
                    'nolabel append'
    for i, ctrl in enumerate(ctrl_list):
        output_file = os.path.join(output_path, 'control_combination_{}.xls'.format(i))
        cmd_list.append('foreach dep_var in {}{'.format(dep_vars))
        cmd_list.append("	capture qui streg `dep_var' {}, vce(cluster country_iso3) d(w)".format(' '.join(ctrl)))
        cmd_list.append('	outreg2 using "{}", {}'.format(output_file, output_option))
        cmd_list.append('}\n')

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(save_file))
