# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from error import error

for i in ['6', '11']:
    test_data_path = "../data/test_%s_data_dum_scale.csv" % i
    test_data = pd.read_csv(test_data_path)

    no_dum_test_data_path = "../data/test_%s_data_no_dum_scale.csv" % i
    no_dum_test_data = pd.read_csv(no_dum_test_data_path)

    lineX_passenger_hour_test_path = "../data/line%s_passenger_hour_test.csv" % i
    line_passenger_hour_test = pd.read_csv(lineX_passenger_hour_test_path)
    test_labels = line_passenger_hour_test['card_id']

    # 线性回归预测
    model_path = "../model/linreg_%s.model" % i
    model = joblib.load(model_path)
    features = test_data.drop('date', axis=1)
    predict_labels = model.predict(features)
    err = error(predict_labels, test_labels)
    # print(err)

    # 2次lasso回归预测
    quadratic_featurizer = PolynomialFeatures(degree=2)
    X_train_quadratic = quadratic_featurizer.fit_transform(features)
    lassoreg_model_path = "../model/lassoreg_%s.model" % i
    quadratic_model = joblib.load(lassoreg_model_path)
    quadratic_predict_labels = quadratic_model.predict(X_train_quadratic)
    quadratic_err = error(quadratic_predict_labels, test_labels)
    print(quadratic_err)

    # CART树预测
    tree_model_path = "../model/treereg_%s.model" % i
    tree_model = joblib.load(tree_model_path)
    no_dum_features = no_dum_test_data.drop('date', axis=1)
    tree_predict_labels = tree_model.predict(no_dum_features)
    err = error(tree_predict_labels, test_labels)
    print(err)

    # GBDT预测
    gbdt_model_path = "../model/gbdt_%s.model" % i
    gbdt_model = joblib.load(gbdt_model_path)
    no_dum_features = no_dum_test_data.drop('date', axis=1)
    gbdt_predict_labels = gbdt_model.predict(no_dum_features)
    err = error(gbdt_predict_labels, test_labels)
    print(err)
