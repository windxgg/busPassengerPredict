# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame

train_data = pd.read_csv('../data/train_data.csv', header=None,
                         names=['use_city', 'line_name', 'terminal_id', 'card_id', 'create_city', 'deal_time',
                                'card_type'])
for i in ['线路6', '线路11']:
    train_data_lineX = train_data[train_data['line_name'] == i]
    # # 生成标准时间格式的交易数据
    # train_data_lineX = train_data_lineX.reset_index(drop=True)
    # train_data_lineX['deal_time'] = train_data_lineX['deal_time'].apply(lambda x: str(x)[:8] + ' ' + str(x)[8:])
    # train_data_lineX['deal_time'] = pd.to_datetime(train_data_lineX['deal_time'])
    if i == '线路6':
        train_data_lineX.to_csv('../data/train_data_line6.csv', header=0, index=0, encoding='utf-8')
    if i == '线路11':
        train_data_lineX.to_csv('../data/train_data_line11.csv', header=0, index=0, encoding='utf-8')
    # 把交易数据的日期和小时分成两个字段
    train_data_lineX['date'] = train_data_lineX['deal_time'].apply(lambda x: str(x).split(' ')[0])
    train_data_lineX['time'] = train_data_lineX['deal_time'].apply(lambda x: int(str(x).split(' ')[1].split(':')[0]))
    train_data_lineX_date_time = train_data_lineX.drop('deal_time', axis=1, inplace=False)
    if i == '线路6':
        train_data_lineX_date_time.to_csv('../data/train_data_6_date_time.csv', header=1, index=0, encoding='utf-8')
    if i == '线路11':
        train_data_lineX_date_time.to_csv('../data/train_data_11_date_time.csv', header=1, index=0, encoding='utf-8')
    train_data_lineX_date_time_06 = train_data_lineX_date_time[6 <= train_data_lineX_date_time['time']]
    train_data_lineX_date_time_06_21 = train_data_lineX_date_time_06[train_data_lineX_date_time_06['time'] <= 21]
    if i == '线路6':
        train_data_lineX_date_time_06_21.to_csv('../data/train_data_line6_date_time_06_21.csv', header=1, index=0,
                                                encoding='utf-8')
    if i == '线路11':
        train_data_lineX_date_time_06_21.to_csv('../data/train_data_line11_date_time_06_21.csv', header=1, index=0,
                                                encoding='utf-8')
    lineX_passenger_hour = DataFrame(
        train_data_lineX_date_time_06_21.groupby(['date', 'time']).count()['card_id']).reset_index()
    if i == '线路6':
        lineX_passenger_hour.to_csv('../data/line6_passenger_hour.csv', header=1, index=0, encoding='utf-8')
    if i == '线路11':
        lineX_passenger_hour.to_csv('../data/line11_passenger_hour.csv', header=1, index=0, encoding='utf-8')
