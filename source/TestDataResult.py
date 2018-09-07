# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame

weather_report_data = pd.read_csv('../data/weather_report_result.csv', header=None,
                                  names=['date', 'temperature_h', 'temperature_l', 'temperature_average',
                                         'temperature_abs', 'wind_d_map', 'wind_n_map', 'wind_average', 'wind_abs',
                                         'weather_d_map', 'weather_n_map', 'weather_average', 'weather_abs'])
holiday = pd.read_csv('../data/date_holiday.txt', header=None, names=['date', 'isholiday'])

testdate = pd.date_range('2014-12-25', '2014-12-31')
datetimelist = []
for idate in testdate:
    datetime = pd.date_range(str(idate) + ' 6:00', str(idate) + ' 21:00', freq='H')
    datetimelist.append(DataFrame(datetime))

datetimeDf = pd.concat(datetimelist, ignore_index=True)
datetimeDf.columns = ['datetime']
datetimeDf['date'] = datetimeDf['datetime'].apply(lambda x: str(x).split(' ')[0])
datetimeDf['time'] = datetimeDf['datetime'].apply(lambda x: int(str(x).split(' ')[1].split(':')[0]))
datetimeDf_date_time = datetimeDf.drop('datetime', axis=1, inplace=False)
for i in ['6', '11']:
    lineX_passenger_hour_path = "../data/line%s_passenger_hour.csv" % i
    lineX_passenger_hour = pd.read_csv(lineX_passenger_hour_path)
    train_passenger_test = pd.concat([lineX_passenger_hour, datetimeDf_date_time], ignore_index=True)

    test_data_weather = pd.merge(train_passenger_test, weather_report_data, on='date', how='left')
    test_data_weather_holiday = pd.merge(test_data_weather, holiday, on='date', how='left')
    test_data_weather_holiday['dayofweek'] = test_data_weather_holiday['date'].apply(
        lambda x: pd.to_datetime(x).dayofweek)

    time_dum = pd.get_dummies(test_data_weather_holiday['time'], prefix='time')
    wind_d_map_dum = pd.get_dummies(test_data_weather_holiday['wind_d_map'], prefix='wind_d_map')
    wind_n_map_dum = pd.get_dummies(test_data_weather_holiday['wind_n_map'], prefix='wind_n_map')
    weather_d_map_dum = pd.get_dummies(test_data_weather_holiday['weather_d_map'], prefix='weather_d_map')
    weather_n_map_dum = pd.get_dummies(test_data_weather_holiday['weather_n_map'], prefix='weather_n_map')
    isholiday_dum = pd.get_dummies(test_data_weather_holiday['isholiday'], prefix='isholiday')
    dayofweek_dum = pd.get_dummies(test_data_weather_holiday['dayofweek'], prefix='dayofweek')

    test_data_dum = pd.concat(
        [test_data_weather_holiday, time_dum, wind_d_map_dum, wind_n_map_dum, weather_d_map_dum,
         weather_n_map_dum, isholiday_dum, dayofweek_dum], axis=1)
    test_data_dum.drop(
        ['time', 'wind_d_map', 'wind_n_map', 'weather_d_map', 'weather_n_map', 'isholiday', 'dayofweek'], axis=1,
        inplace=True)

    import sklearn.preprocessing as preprocessing

    scaler = preprocessing.StandardScaler()
    temperature_h_scale = scaler.fit(test_data_dum[
                                         ['temperature_h', 'temperature_l', 'temperature_average', 'temperature_abs',
                                          'weather_average', 'weather_abs']].values)
    scaleDf = DataFrame(temperature_h_scale.transform(test_data_dum[
                                                          ['temperature_h', 'temperature_l', 'temperature_average',
                                                           'temperature_abs', 'weather_average',
                                                           'weather_abs']].values),
                        columns=['temperature_h_scale', 'temperature_l_scale', 'temperature_average_scale',
                                 'temperature_abs_scale', 'weather_average_scale', 'weather_abs_scale'])
    test_data_dum_scale = pd.concat([test_data_dum, scaleDf], axis=1)
    test_data_dum_scale.drop(
        ['card_id', 'temperature_h', 'temperature_l', 'temperature_average', 'temperature_abs', 'weather_average',
         'weather_abs'],
        axis=1, inplace=True)

    result_no_dum_scale = test_data_weather_holiday[
        test_data_weather_holiday['date'] > '2014-12-24']
    result_no_dum_scale.drop('card_id', axis=1, inplace=True)
    result = test_data_dum_scale[test_data_dum_scale['date'] > '2014-12-24']

    test_data_no_dum_scale_path = '../data/test_%s_data_no_dum_scale.csv' % i
    result_no_dum_scale.to_csv(test_data_no_dum_scale_path, header=1, index=0, encoding='utf-8')

    test_data_dum_scale_path = '../data/test_%s_data_dum_scale.csv' % i
    result.to_csv(test_data_dum_scale_path, header=1, index=0, encoding='utf-8')
