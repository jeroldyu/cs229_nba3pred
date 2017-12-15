"""
tuning_boosting.py
--------------------------------------
December 9th, 2017
Roland Centeno, Hilary Sun, Jerold Yu
--------------------------------------
This document contains code that uses grid search GridSearchCV
to hypertune the parameters to look for the best gradient boosted model.
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
    X = df.ix[:,0:3].values
    Y = df.ix[:,4].values

    return X, Y    


'''
Parameters:
* train_X: parameters of the training data (e.g. ncaa_fg3)
* train_y: label for the training data (i.e. nba_fg3_pct)
* test_X: parameters of the test data
* test_y: label for the test data (i.e. nba_fg3_pct)
* params: parameters used for the gradient boosting regressor.

Function: builds a gradient boosting regressor using the data and specified 
          parameters. Calculates the mean squared error of the fitted model.
'''
def fit_model(train_X, train_y, test_X, test_y, params):
    clf = ensemble.GradientBoostingRegressor(**params)

    clf.fit(train_X, train_y)
    mse = mean_squared_error(test_y, clf.predict(test_X))
    print("MSE: %.4f" % mse)

    return clf


'''
Parameters:
* test_X: parameters of the test data
* test_y: label for the test data (i.e. nba_fg3_pct)
* clf: the fitted gradient boosting model
* params: parameters used for the gradient boosting regressor
* columns: the header names of the data

Function: generates two plots: one for the deviance of the training and test data
          over the number of boosting iterations, and one that ranks the relative
          importance of the variables used.
'''
def generate_plots(test_X, test_y, clf, params, columns):
    
    # Compute test set deviance.
    test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

    for i, pred_y in enumerate(clf.staged_predict(test_X)):
        test_score[i] = clf.loss_(test_y, pred_y)

    plt.figure(figsize=(12,6))
    plt.subplot(1,2,1)
    plt.title('Deviance')
    plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-', label='Training Set Deviance')
    plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-', label='Test Set Deviance')
    plt.legend(loc='upper right')
    plt.xlabel('Boosting Iterations')
    plt.ylabel('Deviance')

    # Plot feature importance relative to the other variables.
    feature_importance = clf.feature_importances_
    feature_importance = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)

    col = []
    for i in sorted_idx:
        col.append(columns[i])

    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.subplot(1,2,2)
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, col)
    plt.tight_layout()
    plt.xlabel('Relative Importance')
    plt.title('Variable Importance')
    plt.show()



def main():
    columns = ['X1', 'X2', 'X3', 'X4', 'Y']
    train_X, train_y = load_dataset('transformed_train.csv')
    test_X, test_y = load_dataset('transformed_test.csv')

    param_grid = {'learning_rate': [1, .1, .001, .0001, .00001, .000001],
                  'max_depth': [4, 5, 6]
    }

    est = ensemble.GradientBoostingRegressor(n_estimators = 3000)
    gs_cv = GridSearchCV(est, param_grid, n_jobs=4).fit(train_X, train_y)
    params = gs_cv.best_params_
    print(params)
    params['n_estimators'] = 3000
    clf = fit_model(train_X, train_y, test_X, test_y, params)
    generate_plots(test_X, test_y, clf, params, columns)



if __name__ == '__main__':
	main()