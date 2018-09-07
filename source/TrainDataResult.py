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
for datei in testdate:
    datetime = pd.date_range(str(datei) + ' 6:00', str(datei) + ' 21:00', freq='H')
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

    train_data_weather_passenger = pd.merge(train_passenger_test, weather_report_data, on='date', how='left')
    train_data_weather_passenger_holiday = pd.merge(train_data_weather_passenger, holiday, on='date', how='left')
    train_data_weather_passenger_holiday['dayofweek'] = train_data_weather_passenger_holiday['date'].apply(
        lambda x: pd.to_datetime(x).dayofweek)

    time_dum = pd.get_dummies(train_data_weather_passenger_holiday['time'], prefix='time')
    wind_d_map_dum = pd.get_dummies(train_data_weather_passenger_holiday['wind_d_map'], prefix='wind_d_map')
    wind_n_map_dum = pd.get_dummies(train_data_weather_passenger_holiday['wind_n_map'], prefix='wind_n_map')
    weather_d_map_dum = pd.get_dummies(train_data_weather_passenger_holiday['weather_d_map'], prefix='weather_d_map')
    weather_n_map_dum = pd.get_dummies(train_data_weather_passenger_holiday['weather_n_map'], prefix='weather_n_map')
    isholiday_dum = pd.get_dummies(train_data_weather_passenger_holiday['isholiday'], prefix='isholiday')
    dayofweek_dum = pd.get_dummies(train_data_weather_passenger_holiday['dayofweek'], prefix='dayofweek')

    train_data_dum = pd.concat(
        [train_data_weather_passenger_holiday, time_dum, wind_d_map_dum, wind_n_map_dum, weather_d_map_dum,
         weather_n_map_dum, isholiday_dum, dayofweek_dum], axis=1)
    train_data_dum.drop(
        ['time', 'wind_d_map', 'wind_n_map', 'weather_d_map', 'weather_n_map', 'isholiday', 'dayofweek'], axis=1,
        inplace=True)

    import sklearn.preprocessing as preprocessing

    scaler = preprocessing.StandardScaler()
    temperature_h_scale = scaler.fit(train_data_dum[
                                         ['temperature_h', 'temperature_l', 'temperature_average', 'temperature_abs',
                                          'weather_average', 'weather_abs']].values)
    scaleDf = DataFrame(temperature_h_scale.transform(train_data_dum[
                                                          ['temperature_h', 'temperature_l', 'temperature_average',
                                                           'temperature_abs', 'weather_average',
                                                           'weather_abs']].values),
                        columns=['temperature_h_scale', 'temperature_l_scale', 'temperature_average_scale',
                                 'temperature_abs_scale', 'weather_average_scale', 'weather_abs_scale'])
    train_data_dum_scale = pd.concat([train_data_dum, scaleDf], axis=1)
    train_data_dum_scale.drop(
        ['temperature_h', 'temperature_l', 'temperature_average', 'temperature_abs', 'weather_average', 'weather_abs'],
        axis=1, inplace=True)
    result_no_dum_scale1 = train_data_weather_passenger_holiday[
        train_data_weather_passenger_holiday['date'] < '2014-12-25']
    result_no_dum_scale2 = result_no_dum_scale1[result_no_dum_scale1['date'] < '2014-08-11']
    result_no_dum_scale3 = result_no_dum_scale1[result_no_dum_scale1['date'] > '2014-08-17']
    result_no_dum_scale = pd.concat([result_no_dum_scale2, result_no_dum_scale3])

    train_data_dum_scale1 = train_data_dum_scale[train_data_dum_scale['date'] < '2014-12-25']
    train_data_dum_scale2 = train_data_dum_scale1[train_data_dum_scale1['date'] < '2014-08-11']
    train_data_dum_scale3 = train_data_dum_scale1[train_data_dum_scale1['date'] > '2014-08-17']
    result_dum_scale = pd.concat([train_data_dum_scale2, train_data_dum_scale3])

    train_data_no_dum_scale_path = '../data/line%s_train_data_no_dum_scale.csv' % i
    result_no_dum_scale.to_csv(train_data_no_dum_scale_path, header=1, index=0, encoding='utf-8')
    train_data_dum_scale_path = '../data/line%s_train_data_dum_scale.csv' % i
    result_dum_scale.to_csv(train_data_dum_scale_path, header=1, index=0, encoding='utf-8')
    print(result_no_dum_scale)
