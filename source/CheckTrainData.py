# -*- coding: utf-8 -*-
'''
查看原始数据各个字段包含的值
'''
import pandas as pd

train_data = pd.read_csv('../data/gd_train_data.txt', header=None,
                         names=['use_city', 'line_name', 'terminal_id', 'card_id', 'create_city', 'deal_time',
                                'card_type'])
train_data.info()
print(train_data['use_city'].drop_duplicates())
print(train_data['line_name'].drop_duplicates())
print(train_data['create_city'].drop_duplicates())
print(train_data['card_type'].drop_duplicates())
