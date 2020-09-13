#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_extract_useful_variables
# @Date: 2020/8/5
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.PreparePoliticsDataset.step01_extract_useful_variables
"""

import os

import pandas as pd
from pandas import DataFrame

from SortData.PreparePoliticsDataset import PathInfo as const

if __name__ == '__main__':
    # Quality of government data
    qog_df: DataFrame = pd.read_stata(os.path.join(const.DATA_PATH, 'qog_std_ts_jan20.dta'))
    qog_useful_list = ['cname', 'year', 'ccodealp', 'aii_q10', 'gcb_pb', 'gir_acrl', 'iiag_rol', 'ti_cpi',
                       'vdem_corr', 'bti_ci', 'ucdp_type3', 'lp_legor', 'aii_q01', 'aii_q15', 'aii_q16', 'bti_foe',
                       'bti_rol', 'aii_q07', 'aii_q06', 'fh_rol', 'p_polity2', 'chga_demo', 'fh_status', 'sgi_qdrlc',
                       'sgi_qdrl', 'van_comp', 'van_index', 'van_part', 'h_polcon3', 'vdem_exbribe', 'vdem_excrptps',
                       'vdem_execorr', 'vdem_exembez', 'vdem_exthftps', 'vdem_mecorrpt', 'vdem_pubcorr', 'vdem_jucorrdc',
                       'vdem_gcrrpt', 'ti_cpi_om']

    qog_useful_df: DataFrame = qog_df.loc[:, qog_useful_list].drop_duplicates(subset=['ccodealp', 'year'])
    qog_useful_df.to_pickle(os.path.join(const.TEMP_PATH, '20200913_qog_useful_dataset.pkl'))

    # Pruge data
    purge_df: DataFrame = pd.read_stata(
        os.path.join(const.DATA_PATH, 'Purge data (Sudduth CPS)', 'CPS_Elitepurge_Sudduth.dta')).rename(
        columns={'idacr': 'ccodealp'})
    purge_useful_list = ['year', 'ccodealp', 'Npurge', 'purge4', 'purge9']
    purge_useful_df: DataFrame = purge_df.loc[:, purge_useful_list].drop_duplicates(subset=['ccodealp', 'year'])
    purge_useful_df.loc[:, 'ccodealp'] = purge_useful_df['ccodealp'].replace(
        {'HAI': 'HTI', 'GUA': 'GTM', 'HON': 'HND', 'SAL': 'SLV', 'PAR': 'PRY', 'URU': 'URY', 'SPN': 'ESP', 'POR': 'PRT',
         'BUL': 'BGR', 'RUM': 'ROU', 'GRG': 'GEO', 'EQG': 'GNQ', 'GAM': 'GMB', 'MAA': 'MRT', 'NIR': 'NER', 'CDI': 'CIV',
         'GUI': 'GIN', 'BFO': 'BFA', 'SIE': 'SLE', 'TOG': 'TGO', 'CAO': 'CMR', 'NIG': 'NGA', 'CEN': 'CAF', 'CHA': 'TCD',
         'CON': 'COG', 'TAZ': 'TZA', 'BUI': 'BDI', 'ANG': 'AGO', 'MZM': 'MOZ', 'ZAM': 'ZMB', 'ZIM': 'ZWE', 'MAW': 'MWI',
         'SAF': 'ZAF', 'MAG': 'MDG', 'MOR': 'MAR', 'ALG': 'DZA', 'KUW': 'KWT', 'BAH': 'BHR', 'UAE': 'ARE', 'OMA': 'OMN',
         'TAJ': 'TJK', 'KZK': 'KAZ', 'BHU': 'BTN', 'BNG': 'BGD', 'MYA': 'MMR', 'SRI': 'LKA', 'NEP': 'NPL', 'THI': 'THA',
         'CAM': 'KHM', 'DRV': 'VNM', 'SIN': 'SGP', 'PHI': 'PHL', 'INS': 'IDN', 'DRC': 'COD', 'SWA': 'SWZ', 'SUD': 'SDN',
         'YPR': 'YEM', 'KYR': 'KGZ', 'ROK': 'KOR', 'MAL': 'MYS'})
    purge_useful_df.to_pickle(os.path.join(const.TEMP_PATH, '20200913_purge_useful_dataset.pkl'))

    useful_df: DataFrame = purge_useful_df.merge(qog_useful_df, on=['ccodealp', 'year'], how='outer')
    useful_df.to_pickle(os.path.join(const.TEMP_PATH, '20200913_purge_qog_merged.pkl'))

    # UCDP data
    ucdp_df: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'ucdp-nonstate-201.csv')).rename(
        columns={'location': 'cname'})
    ucdp_useful_list = ['year', 'best_fatality_estimate', 'low_fatality_estimate', 'high_fatality_estimate', 'cname',
                        'conflict_id']
    ucdp_group = ucdp_df.groupby(['year', 'cname'])
    event_number = ucdp_group['conflict_id'].count().reset_index(drop=False).rename(
        columns={'conflict_id': 'conflict_num'})
    fatality_sum = ucdp_group[
        'best_fatality_estimate', 'low_fatality_estimate', 'high_fatality_estimate'].sum().reset_index(
        drop=False).rename(columns={'conflict_id': 'conflict_num'})
    ucdp_useful_df: DataFrame = fatality_sum.merge(event_number, on=['year', 'cname'], how='outer')
    ucdp_result_df = DataFrame(columns=ucdp_useful_df.keys())
    for i in ucdp_useful_df.index:
        location = ucdp_useful_df.loc[i, 'cname']
        if ',' not in location:
            ucdp_result_df.loc[ucdp_result_df.shape[0]] = ucdp_useful_df.loc[i]
        else:
            location_list = location.split(',')
            for l in location_list:
                ucdp_useful_df.loc[i, 'cname'] = l.strip()
                ucdp_result_df.loc[ucdp_result_df.shape[0]] = ucdp_useful_df.loc[i]
            ucdp_useful_df.loc[i, 'cname'] = location

    ucdp_result_df2: DataFrame = ucdp_result_df.groupby(['cname', 'year']).sum().reset_index(drop=False)
    cname_list = ucdp_result_df2['cname'].drop_duplicates()

    result_dict = dict(ucdp_result_df2.iloc[0])
    for key in result_dict:
        result_dict[key] = 0

    for cname in cname_list:
        cname_df: DataFrame = ucdp_result_df2.loc[ucdp_result_df2['cname'] == cname]
        start_year = cname_df['year'].min()
        end_year = cname_df['year'].max()

        for year in range(start_year + 1, end_year):
            current_year_df: DataFrame = cname_df.loc[cname_df['year'] == year].copy()

            if current_year_df.empty:
                result_dict['year'] = year
                result_dict['cname'] = cname
                ucdp_result_df2: DataFrame = ucdp_result_df2.append(result_dict, ignore_index=True)

    ucdp_result_df2.loc[:, 'cname'] = ucdp_result_df2['cname'].replace(
        {'Russia (Soviet Union)': 'Russia', 'Serbia (Yugoslavia)': 'Serbia', 'Pakistan': 'Pakistan (1971-)',
         'Myanmar (Burma)': 'Myanmar', 'Madagascar (Malagasy)': 'Madagascar', 'Ethiopia': 'Ethiopia (-1992)',
         'Sudan': 'Sudan (2012-)', 'Yemen (North Yemen)': 'Yemen, North', 'Ivory Coast': "Cote d'Ivoire",
         'DR Congo (Zaire)': 'Congo, Democratic Republic'})
    ucdp_result_df2.to_pickle(os.path.join(const.TEMP_PATH, '20200806_ucdp_useful_data.pkl'))

    useful_df2: DataFrame = useful_df.merge(ucdp_result_df2, on=['cname', 'year'], how='outer')
    useful_df2.to_pickle(os.path.join(const.TEMP_PATH, '20200913_purge_qog_ucdp_merged.pkl'))
