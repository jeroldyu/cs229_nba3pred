"""
linear_regression.py
--------------------------------------
This document contains the code to run linear regression and
weighted linear regression.
"""

# LIBRARIES
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn 

from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale
from collections import Counter
from sklearn.metrics import mean_squared_error, r2_score

import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.iolib.table import (SimpleTable, default_txt_fmt)


'''
Parameters:
* filename: csv file to be loaded.

Function: forms the train and test data from the given csv files.
'''
def read_file(filename):

    data = pd.read_csv(filepath_or_buffer=filename, sep=',',header=None)
    data.columns = ['feature1', 'feature2', 'feature3', 'feature4', 'y']
    data.dropna(how="all", inplace=True) # drops the empty line at file-end
    data.tail()

    X_data = data.ix[:,:4].values
    Y_data = data.ix[:,-1].values
    
    return X_data, Y_data


'''
Parameters:
* X_train: features for the training set.
* y_train: output for the training set.
* X_test: features for the test set.
* y_test: output for the test set.

Function: fits a linear regression model using the training data and measures its
          performance on the training and test set, respectively.
'''
def run_linear_regression(X_train, y_train, X_test, y_test):
    
    lm = LinearRegression()
    lm.fit(X_train,y_train)
    
    pred_train = lm.predict(X_train)
    pred_test = lm.predict(X_test)
    
    return lm, pred_train, pred_test


'''
Parameters:
* X_train: features for the training set.
* y_train: output for the training set.
* X_test: features for the test set.
* y_test: output for the test set.

Function: fits a weighted linear regression model using the training data and
          measures its performance on the training and test set, respectively.
'''
def run_weighted_regression(X_train, y_train, X_test, y_test):
    
    # Constants needed to ensure that WLR works.
    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)
    
    variance = np.diag(np.cov(X_train))

    mod_wls = sm.WLS(y_train, X_train, weights=1/variance)
    res_wls = mod_wls.fit()
    
    weighted_pred_test = res_wls.predict(X_test)
    weighted_pred_train = res_wls.predict(X_train)
    
    return res_wls, weighted_pred_train, weighted_pred_test
    

'''
Parameters:
* Y_train: output for the training set.
* Y_test: output for the test set.
* pred_train: predicted values for the training set.
* pred_test: predicted values for the test set. 

Function: This function plots the predicted actual Y values of the train and test
          set vs the predicted values of the regression. Train and test points are 
          designated by different colors.
'''
def plot_results(Y_train, Y_test, pred_train, pred_test):

    X = np.linspace(min(Y_test), max(Y_test))    

    plt.plot(Y_train, pred_train, 'b.', label='Train Player Data Points')
    plt.plot(Y_test, pred_test, 'r.', label = 'Test Player Data Points')
    plt.plot(X, X, 'k', label = 'Predicted Value = Actual Value')
    
    plt.xlabel('Actual Value')
    plt.ylabel('Predicted Value')
    plt.legend()
    plt.title('Weighted Linear Regression Results')
    plt.show()    
    

    
def main():
    X_train, Y_train = read_file("transformed_train.csv")
    X_test, Y_test = read_file("transformed_test.csv")

    lm, pred_train, pred_test = run_weighted_regression(X_train, Y_train, X_test, Y_test)

    print lm.summary()
    plot_results(Y_train, Y_test, pred_train, pred_test)

    
if __name__ == '__main__':
    main()
