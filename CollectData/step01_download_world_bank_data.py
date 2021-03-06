#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_download_world_bank_data
# @Date: 2020/3/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m CollectData.step01_download_world_bank_data
"""

import os
import time
import random
from urllib.parse import quote

from tqdm import tqdm
import wbdata
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    # reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200311_regression_data_with_count.pkl'))
    # country_year_df: DataFrame = reg_df.loc[:, [const.COUNTRY_ISO3, const.FISCAL_YEAR]].drop_duplicates()

    source_list = wbdata.get_source(display=False)
    output_path = os.path.join(const.DATABASE_PATH, 'WorldBank')
    indicator_index_df = DataFrame(columns=['SourceID', 'SourceName', 'IndicatorID', 'IndicatorName',
                                            'sourceOrganization', 'sourceNote'])
    error_indicator_list = list()
    for source_info in source_list:
        source_id = source_info['id']
        save_path = os.path.join(output_path, source_id)
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        info_dict = {'SourceID': source_id, 'SourceName': source_info['name']}

        indicator_list = wbdata.get_indicator(source=source_id, display=False)
        source_indicator_dfs = list()
        for indicator_info in tqdm(indicator_list):
            indicator_info_dict = info_dict.copy()
            indicator_id = indicator_info['id']
            indicator_info_dict['IndicatorID'] = indicator_id
            indicator_info_dict['IndicatorName'] = indicator_info['name']

            for key in ['sourceOrganization', 'sourceNote']:
                if key in indicator_info:
                    indicator_info_dict[key] = indicator_info[key]

            tmp_df: DataFrame = indicator_index_df.loc[indicator_index_df['IndicatorID'] == indicator_id]
            if not tmp_df.empty:
                tmp_source_id = tmp_df.iloc[0]['SourceID']
                tmp_save_path = os.path.join(output_path, tmp_source_id)
                for key in ['SourceName', 'SourceID']:
                    indicator_info_dict[key] = tmp_df.iloc[0][key]
                indicator_index_df: DataFrame = indicator_index_df.append(indicator_info_dict, ignore_index=True)
                continue

            save_file_path = os.path.join(save_path, '{}.pkl'.format(indicator_id))
            if os.path.isfile(save_file_path):
                indicator_df = pd.read_pickle(save_file_path)
            else:
                try:
                    indicator_df: DataFrame = wbdata.get_data(quote(indicator_id), country='all', pandas=True,
                                                              column_name=indicator_id).dropna()
                    indicator_df.to_pickle(os.path.join(save_path, '{}.pkl'.format(indicator_id)))
                    time.sleep(random.randint(1, 10))
                except Exception as e:
                    error_indicator_list.append(indicator_id)
                    continue

            source_indicator_dfs.append(indicator_df)
            indicator_index_df: DataFrame = indicator_index_df.append(indicator_info_dict, ignore_index=True)
        source_df: DataFrame = pd.concat(source_indicator_dfs, axis=1)
        source_df.to_pickle(os.path.join(output_path, '{}.pkl'.format(source_id)))

    indicator_index_df.to_pickle(os.path.join(output_path, '20200324_indicator_index.pkl'))
    indicator_index_df.to_excel(os.path.join(output_path, '20200324_indicator_index.xlsx'), index=False)
    pd.to_pickle(error_indicator_list, os.path.join(const.TEMP_PATH, '20200324_error_loading_indicator_list.pkl'))
