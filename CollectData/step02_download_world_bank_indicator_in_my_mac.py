#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_download_world_bank_indicator_in_my_mac
# @Date: 2020/3/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m CollectData.step02_download_world_bank_indicator_in_my_mac
"""

import os
import time
import random

from tqdm import tqdm
import wbdata
from pandas import DataFrame

if __name__ == '__main__':
    source_list = wbdata.get_source(display=False)
    indicator_index_df = DataFrame(columns=['SourceID', 'SourceName', 'IndicatorID', 'IndicatorName',
                                            'sourceOrganization', 'sourceNote'])
    save_path = '/Users/markwang/Google Drive/Projects/DatabaseInformation/WorldBank'
    for source_info in tqdm(source_list):
        source_id = source_info['id']
        info_dict = {'SourceID': source_id, 'SourceName': source_info['name']}

        indicator_list = wbdata.get_indicator(source=source_id, display=False)
        source_indicator_dfs = list()
        for indicator_info in indicator_list:
            indicator_id = indicator_info['id']
            indicator_info_dict = info_dict.copy()
            indicator_info_dict['IndicatorID'] = indicator_id
            indicator_info_dict['IndicatorName'] = indicator_info['name']
            for key in ['sourceOrganization', 'sourceNote']:
                if key in indicator_info:
                    indicator_info_dict[key] = indicator_info[key]

            indicator_index_df: DataFrame = indicator_index_df.append(indicator_info_dict, ignore_index=True)
        time.sleep(random.randint(1, 10))

    indicator_index_df.to_excel(os.path.join(save_path, '20200311_indicator_information.xlsx'), index=False)
