# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn import ensemble
from error import error


def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Error")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, scoring=score)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training error")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation error")

    plt.legend(loc="best")
    return plt


for i in ['6', '11']:
    train_data_X_path = '../data/line%s_train_data_dum_scale.csv' % i
    train_data_X = pd.read_csv(train_data_X_path)
    lables = train_data_X['card_id']
    features = train_data_X.drop(['date', 'card_id'], axis=1)
    # 每天06点到21点共16个预测小时，预测天数为7天
    # X_train, X_test, y_train, y_test = train_test_split(features, lables, test_size=7 * 16)

    quadratic_featurizer = PolynomialFeatures(degree=2)
    X_train_quadratic = quadratic_featurizer.fit_transform(features)

    # linreg = linear_model.LinearRegression()
    # linreg.fit(features, lables)
    # model_path = "../model/linreg_%s.model" % i
    # joblib.dump(linreg, model_path)
    # model = joblib.load(model_path)
    # predict_labels = model.predict(X_test)
    # err = error(predict_labels, y_test)
    # print("err: %f" % err)
    score = make_scorer(error, greater_is_better=True)
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=5, test_size=7 * 16, random_state=1)

    # print(cross_val_score(linreg, features, lables, scoring=score, cv=cv))
    # Lineartitle = "Learning Curves (Linear Regression)"
    # plot_learning_curve(linreg, Lineartitle, features, lables, ylim=(0.0, 1.01), cv=cv)

    # print(cross_val_score(linreg, X_train_quadratic, lables, scoring=score, cv=cv))
    # Quadratictitle = "Learning Curves (Quadratic Linear Regression)"
    # plot_learning_curve(linreg, Quadratictitle, X_train_quadratic, lables, ylim=(0.0, 1.01), cv=cv)

    # lassoreg = linear_model.Lasso()
    # parameters = {'alpha': [1 * (i + 1) for i in range(10)]}
    # clf = GridSearchCV(lassoreg, parameters)
    # clf.fit(features, lables)
    # best_parameters = clf.best_params_
    # print(best_parameters['alpha'])
    # lassoreg.set_params(alpha=best_parameters['alpha'])
    # print(cross_val_score(lassoreg, features, lables, scoring=score, cv=cv))
    # Lassotitle = "Learning Curves (Lasso Regression)"
    # plot_learning_curve(lassoreg, Lassotitle, X_train_quadratic, lables, ylim=(0.0, 1.01), cv=cv)

    # lassoreg.fit(X_train_quadratic, lables)
    # lassoreg_model_path = "../model/lassoreg_%s.model" % i
    # joblib.dump(lassoreg, lassoreg_model_path)

    # for a, score in enumerate(cross_val_score(linreg, features, lables, scoring=score, cv=cv)):
    #     if score >= 6:
    #         train_index, test_index = list(cv.split(features))[a]
    #         print("TRAIN:", train_index, "TEST:", test_index)
    #         print("TRAIN:", train_data_X.loc[train_index], "TEST:", train_data_X.loc[test_index])

    train_data_no_dum_scale_X_path = '../data/line%s_train_data_no_dum_scale.csv' % i
    train_data_no_dum_scale_X = pd.read_csv(train_data_no_dum_scale_X_path)
    no_dum_lables = train_data_no_dum_scale_X['card_id']
    no_dum_features = train_data_no_dum_scale_X.drop(['date', 'card_id'], axis=1)

    treereg = DecisionTreeRegressor()
    print(cross_val_score(treereg, no_dum_features, no_dum_lables, scoring=score, cv=cv))
    Decisiontitle = "Learning Curves (Decision tree)"
    plot_learning_curve(treereg, Decisiontitle, no_dum_features, no_dum_lables, (0.0, 1.01), cv=cv)
    treereg.fit(no_dum_features, no_dum_lables)
    treereg_model_path = "../model/treereg_%s.model" % i
    joblib.dump(treereg, treereg_model_path)

    gbdt = ensemble.GradientBoostingRegressor()
    print(cross_val_score(gbdt, no_dum_features, no_dum_lables, scoring=score, cv=cv))
    title = "Learning Curves (GBDT)"
    plot_learning_curve(gbdt, title, no_dum_features, no_dum_lables, (0.0, 1.01), cv=cv)
    gbdt.fit(no_dum_features, no_dum_lables)
    gbdt_model_path = "../model/gbdt_%s.model" % i
    joblib.dump(gbdt, gbdt_model_path)

    plt.show()
