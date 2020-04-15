#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step07_construct_country_level_regression_file
# @Date: 2020/4/15
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step07_construct_country_level_regression_file
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

COUNTRY_RENAME_DICT = {'NY.GDP.MKTP.KD': 'GDP', 'NY.GDP.PCAP.KD': 'GDP_PC', 'NY.GDS.TOTL.ZS': 'DOMESTIC_SAVING_PER',
                       'NY.GNS.ICTR.ZS': 'SAVING_PER', 'NY.GDP.MKTP.KD.ZG': 'GDP_GROWTH',
                       'NE.GDI.TOTL.KD.ZG': 'GDI_GROWTH', 'NE.GDI.TOTL.ZS': 'GDI_RATIO',
                       'NE.IMP.GNFS.ZS': 'IMPORT_RATIO', 'NV.AGR.TOTL.KD': 'AGR', 'NV.AGR.TOTL.KD.ZG': 'AGR_GROWTH',
                       'NV.AGR.TOTL.ZS': 'AGR_RATIO', 'NV.IND.MANF.KD': 'MANF', 'NV.IND.MANF.KD.ZG': 'MANF_GROWTH',
                       'NV.IND.MANF.ZS': 'MANF_RATIO', 'NV.IND.TOTL.KD': 'IND', 'NV.IND.TOTL.KD.ZG': 'IND_GROWTH',
                       'NV.IND.TOTL.ZS': 'IND_RATIO', 'GB.XPD.RSDV.GD.ZS': 'XRD_RATIO',
                       'GC.TAX.TOTL.GD.ZS': 'TAX_RATIO', 'SL.UEM.TOTL.ZS': 'UNEMP_RATE', 'SP.POP.TOTL': 'POPULATION',
                       'CM.MKT.LCAP.CD': 'MKT_CAP', 'CM.MKT.LCAP.GD.ZS': 'MKT_CAP_RATIO', 'BX.KLT.DINV.CD.WD': 'FDI',
                       'BX.KLT.DINV.WD.GD.ZS': 'FDI_RATIO', 'EG.USE.COMM.GD.PP.KD': 'ENERGY_EFFICIENCY',
                       'EN.ATM.CO2E.KT': 'CO2', 'EN.ATM.GHGT.KT.CE': 'GHG', 'FP.CPI.TOTL.ZG': 'CPI',
                       'FR.INR.LNDP': 'INR_SPR', 'FR.INR.RINR': 'REAL_INR', 'IC.BUS.DFRN.XQ': 'BUS_SCORE',
                       'NE.IMP.GNFS.CD': 'IMPORT', 'NE.IMP.GNFS.KD.ZG': 'IMPORT_GROWTH', 'NE.EXP.GNFS.CD': 'EXPORT',
                       'NE.EXP.GNFS.KD.ZG': 'EXPORT_GROWTH', 'NE.EXP.GNFS.ZS': 'EXPORT_RATIO'}

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200311_regression_data_with_count.pkl'))
    valid_keys = [const.COUNTRY_ISO3, const.FISCAL_YEAR]

    for pre in ['formal', 'real']:
        for suf in ['Extend', 'Shrink', 'ToUnlimit', 'ToLimit']:
            valid_keys.append('{}_{}'.format(pre, suf))

    event_df: DataFrame = reg_df.loc[:, valid_keys].drop_duplicates()
    country_year_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200320_country_year_data.pkl'))
    country_year_df_renamed: DataFrame = country_year_df.rename(
        columns=COUNTRY_RENAME_DICT).rename(columns=lambda x: x.replace('.', '_'))
    country_reg_df: DataFrame = event_df.merge(country_year_df_renamed.drop(['Country', 'Year'], axis=1),
                                               on=[const.COUNTRY_ISO3, const.FISCAL_YEAR], how='inner').sort_values(
        by=[const.FISCAL_YEAR], ascending=True)

    next_year_keys = list(COUNTRY_RENAME_DICT.values())
    next_year_keys.extend(['ln_GDP', 'ln_GDP_PC', 'ln_POPULATION', 'ln_CO2', 'ln_GHG'])
    for key in ['EXPORT', 'IMPORT', 'AGR', 'MANF', 'IND']:
        next_year_keys.append('ln_{}'.format(key))
        country_reg_df.loc[:, 'ln_{}'.format(key)] = country_reg_df[key].apply(np.log)

    shift_one_year = country_reg_df.groupby(const.COUNTRY_ISO3).shift(1)
    for key in next_year_keys:
        country_reg_df.loc[:, '{}_1'.format(key)] = shift_one_year[key]

    # Construct post3 and post5 dummy
    country_group = country_reg_df.groupby(const.COUNTRY_ISO3)
    for key in valid_keys[2:]:
        for i in range(1, 6):
            country_reg_df.loc[:, '{}_{}'.format(key, i)] = country_group[key].shift(i)

        country_reg_df.loc['{}_post3'] = country_reg_df[
            [key, '{}_1'.format(key), '{}_2'.format(key), '{}_3'.format(key)]].sum(axis=1)
        country_reg_df.loc['{}_post5'] = country_reg_df[
            [key, '{}_1'.format(key), '{}_2'.format(key), '{}_3'.format(key), '{}_4'.format(key),
             '{}_5'.format(key)]].sum(axis=1)

    country_reg_df.to_stata(os.path.join(const.STATA_DATA_PATH, '20200415_country_year_reg_data.dta'),
                            write_index=False)
