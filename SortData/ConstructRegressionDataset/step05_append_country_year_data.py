#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step05_append_country_year_data
# @Date: 2020/3/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructRegressionDataset.step05_append_country_year_data
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    country_year_df: DataFrame = pd.read_pickle(
        os.path.join(const.DATA_PATH, 'worldbank', '20200311_worldbank_required_data.pkl')).reset_index(drop=False)
    country_info_df: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'countries_codes_and_coordinates.csv'))
    country_info_df.loc[:, const.COUNTRY_ISO3] = country_info_df['Alpha-3 code'].str.strip('" ')

    country_year_df_code: DataFrame = country_year_df.merge(country_info_df[['Country', const.COUNTRY_ISO3]],
                                                            how='left', on='Country')
    country_iso_dict = {'Yemen, Rep.': 'YEM', 'Virgin Islands (U.S.)': 'VIR', 'Venezuela, RB': 'VEN', 'Tanzania': 'TZA',
                        'St. Lucia': 'LCA', 'St. Kitts and Nevis': 'KNA', 'South Sudan': 'SSD',
                        'Slovak Republic': 'SVK', 'North Macedonia': 'MKD', 'Moldova': 'MDA',
                        'Micronesia, Fed. Sts.': 'FSM', 'Macao SAR, China': 'MAC', 'Lao PDR': 'LAO',
                        'Kyrgyz Republic': 'KGZ', 'Korea, Rep.': 'KOR', 'Korea, Dem. People’s Rep.': 'PRK',
                        'Iran, Islamic Rep.': 'IRN', 'Hong Kong SAR, China': 'HKG', 'Gambia, The': 'GMB',
                        'Eswatini': 'SWZ', 'Egypt, Arab Rep.': 'EGY', 'Curacao': 'CUW', "Cote d'Ivoire": 'CIV',
                        'Congo, Rep.': 'COG', 'Congo, Dem. Rep.': 'CDD', 'Cabo Verde': 'CPV',
                        'British Virgin Islands': 'VGB', 'Bahamas, The': 'BHS'}
    for key in country_iso_dict:
        iso_code = country_iso_dict[key]
        country_year_df_code.loc[country_year_df_code['Country'] == key, const.COUNTRY_ISO3] = iso_code

    valid_cy_df: DataFrame = country_year_df_code.loc[country_year_df_code[const.COUNTRY_ISO3].notnull()].copy()
    valid_cy_df.to_pickle(os.path.join(const.TEMP_PATH, '20200311_country_year_raw_data.pkl'))
    valid_cy_df.loc[:, 'ln_GDP'] = valid_cy_df['NY.GDP.MKTP.KD'].apply(np.log)
    valid_cy_df.loc[:, 'ln_GDP_PC'] = valid_cy_df['NY.GDP.PCAP.KD'].apply(np.log)
    valid_cy_df.loc[:, 'ln_POPULATION'] = valid_cy_df['SP.POP.TOTL'].apply(np.log)
    valid_cy_df.loc[:, 'ln_CO2'] = valid_cy_df['EN.ATM.CO2E.KT'].apply(np.log)
    valid_cy_df.loc[:, 'ln_GHG'] = valid_cy_df['EN.ATM.GHGT.KT.CE'].apply(np.log)
    valid_cy_df.loc[:, const.FISCAL_YEAR] = valid_cy_df['Year'].astype(int)

    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200311_regression_data_with_count.pkl'))
    reg_df_with_cy: DataFrame = reg_df.merge(valid_cy_df.drop(['Country', 'Year'], axis=1),
                                             on=[const.COUNTRY_ISO3, const.FISCAL_YEAR], how='left')
    reg_df_with_cy.to_stata(os.path.join(const.STATA_DATA_PATH, '20200311_regression_data.dta'),
                            write_index=False, version=117)
