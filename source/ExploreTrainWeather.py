# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

weather_report_data = pd.read_csv('../data/weather_report_result.csv', header=None,
                                  names=['date', 'temperature_h', 'temperature_l', 'temperature_average',
                                         'temperature_abs', 'wind_d_map', 'wind_n_map', 'wind_average', 'wind_abs',
                                         'weather_d_map', 'weather_n_map', 'weather_average', 'weather_abs'])

for i in ['6', '11']:
    lineX_passenger_hour_path = "../data/line%s_passenger_hour.csv" % i
    lineX_passenger_hour = pd.read_csv(lineX_passenger_hour_path)
    lineX_passenger_day = DataFrame(lineX_passenger_hour.groupby('date').sum()['card_id']).reset_index()
    passenger_weather = pd.merge(lineX_passenger_day, weather_report_data, on='date', how='left')
    ss = ['temperature_h', 'temperature_l', 'temperature_average', 'temperature_abs', 'wind_d_map', 'wind_n_map',
          'wind_average', 'wind_abs', 'weather_d_map', 'weather_n_map', 'weather_average', 'weather_abs']
    for s in ss:
        feature_daycount = DataFrame(passenger_weather.groupby(s).count()['date']).reset_index()
        feature_person = DataFrame(passenger_weather.groupby(s).sum()['card_id']).reset_index()
        feature_daycount_person = pd.merge(feature_daycount, feature_person, on=s)
        feature_daycount_person['personOneday'] = feature_daycount_person['card_id'] / feature_daycount_person['date']
        feature_average_person = pd.DataFrame(feature_daycount_person, columns=[s, 'personOneday'])
        feature_daycount_person = feature_daycount_person.set_index(s)['personOneday']
        feature_daycount_person.plot(kind='bar', figsize=(8, 5))
        plt.show()
        print(feature_average_person.corr())
