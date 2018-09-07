# -*- coding: utf-8 -*-
import re

import pandas as pd

weather_report = pd.read_csv('../data/gd_weather_report.txt', header=None,
                             names=['date', 'weather', 'temperature', 'wind_direction_force'])


def changeDate(date):
    dateList = date.split('/')
    if int(dateList[1]) < 10:
        month = '0' + dateList[1]
    else:
        month = dateList[1]
    if int(dateList[2]) < 10:
        day = '0' + dateList[2]
    else:
        day = dateList[2]
    return dateList[0] + month + day


weather_report['datestr'] = weather_report['date'].apply(lambda x: changeDate(x))
# 把相应字段分开
weather_report['weather_d'] = weather_report['weather'].apply(lambda x: x.split('/')[0])
weather_report['weather_n'] = weather_report['weather'].apply(lambda x: x.split('/')[1])
weather_report['temperature_h'] = weather_report['temperature'].apply(lambda x: int(re.sub(r'\D', '', x.split('/')[0])))
weather_report['temperature_l'] = weather_report['temperature'].apply(lambda x: int(re.sub(r'\D', '', x.split('/')[1])))
weather_report['wind_direction_force_d'] = weather_report['wind_direction_force'].apply(lambda x: x.split('/')[0])
weather_report['wind_direction_force_n'] = weather_report['wind_direction_force'].apply(lambda x: x.split('/')[1])

weather_report['temperature_average'] = (weather_report['temperature_h'] + weather_report['temperature_l']) / 2.0
weather_report['temperature_abs'] = abs(weather_report['temperature_h'] - weather_report['temperature_l'])
print(pd.concat([weather_report['wind_direction_force_d'], weather_report['wind_direction_force_n']],
                ignore_index=True).drop_duplicates())
windmap = {'无持续风向≤3级': 0, '无持续风向微风转3-4级': 1, '北风微风转3-4级': 1, '东北风3-4级': 2, '北风3-4级': 2, '东南风3-4级': 2, '东风4-5级': 3,
           '北风4-5级': 3}
weather_report['wind_direction_force_d_map'] = weather_report['wind_direction_force_d'].map(windmap)
weather_report['wind_direction_force_n_map'] = weather_report['wind_direction_force_n'].map(windmap)
weather_report['wind_average'] = (weather_report['wind_direction_force_d_map'] + weather_report[
    'wind_direction_force_n_map']) / 2.0
weather_report['wind_abs'] = abs(
    weather_report['wind_direction_force_d_map'] - weather_report['wind_direction_force_n_map'])
print(pd.concat([weather_report['weather_d'], weather_report['weather_n']], ignore_index=True).drop_duplicates())
weathermap = {'晴': 0, '多云': 1, '阴': 2, '小雨': 3, '小到中雨': 4, '中雨': 5, '中到大雨': 6, '大雨': 7, '大到暴雨': 8, '霾': 9, '阵雨': 10,
              '雷阵雨': 11}
weather_report['weather_d_map'] = weather_report['weather_d'].map(weathermap)
weather_report['weather_n_map'] = weather_report['weather_n'].map(weathermap)
weather_report['weather_average'] = (weather_report['weather_d_map'] + weather_report['weather_n_map']) / 2.0
weather_report['weather_abs'] = abs(weather_report['weather_d_map'] - weather_report['weather_n_map'])
weather_report_result = weather_report.drop(
    ['date', 'weather', 'temperature', 'wind_direction_force', 'weather_d', 'weather_n', 'wind_direction_force_d',
     'wind_direction_force_n'], axis=1, inplace=False)
# 生成标准时间格式的天气数据
weather_report_result = weather_report_result.reset_index(drop=True)
print(weather_report_result)
for i in range(len(weather_report_result)):
    weather_report_result.loc[i, 'datestr'] = pd.to_datetime(weather_report_result.loc[i, 'datestr'],
                                                             format='%Y%m%d').strftime('%Y-%m-%d')
weather_report_result.to_csv('../data/weather_report_result.csv', header=0, index=0, encoding='utf-8')
