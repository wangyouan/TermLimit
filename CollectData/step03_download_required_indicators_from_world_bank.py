#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_download_required_indicators_from_world_bank
# @Date: 2020/3/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


"""
python -m CollectData.step01_download_world_bank_data
"""

import os
from urllib.parse import quote

from tqdm import tqdm
# import wbdata
import world_bank_data as wb
import pandas as pd
from pandas import DataFrame

if __name__ == '__main__':
    data_path = '/Users/markwang/Google Drive/Projects/TermLimitChange/data/worldbank'
    required_df: DataFrame = pd.read_excel(os.path.join(data_path, 'country_level_control.xlsx'))

    data_dfs = list()
    for i in tqdm(required_df.index):
        indicator_id = required_df.loc[i, 'IndicatorID']
        source_id = required_df.loc[i, 'SourceID']
        indicator_series: pd.Series = wb.get_series(quote(indicator_id), simplify_index=True).dropna()
        indicator_series.name = indicator_id
        data_dfs.append(indicator_series)

    result_df: DataFrame = pd.concat(data_dfs, axis=1)
    result_df.to_pickle(os.path.join(data_path, '20200311_worldbank_required_data.pkl'))
