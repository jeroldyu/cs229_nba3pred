"""
forest.py
--------------------------------------
This document runs a basic random forest decision tree model with some base parameters
on PCA-transformed data.
"""

# LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn.grid_search import GridSearchCV


'''
Parameters:
* filename: csv file to be loaded.

Function: read in data to use in gradient boosting regression code.
'''
def load_dataset(filename, columns = None):
    df = pd.read_csv(filepath_or_buffer=filename, sep=',')

    if columns:
        df.columns = columns

    df.dropna(how="all", inplace=True) # drops the empty line at file-end
    df.tail()
    X = df.ix[:,0:4].values
    Y = df.ix[:,4].values

    return X, Y    


'''
Parameters:
* train_X: parameters of the training data (e.g. ncaa_fg3)
* train_y: label for the training data (i.e. nba_fg3_pct)
* test_X: parameters of the test data
* test_y: label for the test data (i.e. nba_fg3_pct)
* params: parameters used for the random forest regressor.

Function: builds a random forest regressor using the data and specified parameters.
'''
def fit_model(train_X, train_y, test_X, test_y, params):
    clf = ensemble.RandomForestRegressor(**params)

    clf.fit(train_X, train_y)
    # mse = mean_squared_error(test_y, clf.predict(test_X))
    # print("MSE: %.4f" % mse)

    return clf.predict(train_X), clf.predict(test_X)



def main():
    columns = ['X1', 'X2', 'X3', 'X4', 'Y']
    train_X, train_y = load_dataset('transformed_train.csv')
    test_X, test_y = load_dataset('transformed_test.csv')

    params = {}
    params['n_estimators'] = 3000
    params['max_depth'] = 4
    
    clf = fit_model(train_X, train_y, test_X, test_y, params)



if __name__ == '__main__':
    main()