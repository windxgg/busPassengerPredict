# -*- coding: utf-8 -*-
from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd

train_data_6 = pd.read_csv('../data/train_data_line6.csv', header=None,
                           names=['use_city', 'line_name', 'terminal_id', 'card_id', 'create_city', 'deal_time',
                                  'card_type'])
train_data_6_sort_time = train_data_6.sort_values('deal_time').set_index('deal_time')
train_data_6_sort_time_groupbytime = train_data_6_sort_time.groupby('deal_time').count()['card_id']
fig = plt.figure()
train_data_6_sort_time.groupby('deal_time').count()['card_id'].plot(figsize=(200, 10))
plt.show()


# 把start和end这一段时间切分成每段frequstr时长的切片
def timeFrequent(start, end, freqstr):
    timelist = pd.date_range(start, end, freq=freqstr)
    timeparts = []
    for index in range(len(timelist) - 1):
        timepart = list(timelist[index:index + 2])
        timeparts.append(timepart)
    return timeparts


def everyDayDraw(df):
    day = pd.date_range('2014-08-01 00:00:00', '2014-09-01 00:00:00', freq='D')
    fig, axes = plt.subplots(nrows=31, ncols=1, figsize=(18, 130))
    subplot_counter = 0
    for daystart, dayend in timeFrequent('2014-08-01 00:00:00', '2014-09-01 00:00:00', 'D'):
        if len(df[str(daystart):str(dayend)]) != 0:
            df[str(daystart):str(dayend - timedelta(minutes=1))].plot(style='o-', ax=axes[subplot_counter])
            axes[subplot_counter].set_title(str(day[subplot_counter]))
            subplot_counter += 1
    plt.show()


everyDayDraw(train_data_6_sort_time_groupbytime)


def everyWeekDraw(df):
    week = pd.date_range('2014-08-01 00:00:00', '2014-12-25 00:00:00', freq='W-MON')
    fig, axes = plt.subplots(nrows=25, ncols=1, figsize=(20, 50))
    subplot_counter = 0
    for weekstart, weekend in timeFrequent('2014-08-01 00:00:00', '2014-12-25 00:00:00', 'W-MON'):
        if len(df[str(weekstart):str(weekend)]) != 0:
            df[str(weekstart):str(weekend - timedelta(minutes=1))].plot(style='o-', ax=axes[subplot_counter])
            axes[subplot_counter].set_title(str(week[subplot_counter]))
            subplot_counter += 1
    plt.show()


everyWeekDraw(train_data_6_sort_time_groupbytime)


