"""
kfold.py
--------------------------------------
This document contains the code for k-fold cross validation. Specifically,
we are running the processed training data through linear regression, 
weighted linear regression, gradient boosting, and random forest. The model 
that produces the lowest test mean squared error on the dev set will be used
as the working model for the entire data set.
"""

# LIBRARIES
import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

# local files in directory
import linear_regression as lr
import boosting as gb
import forest as rf



'''
Parameters:
* filename: csv file to be loaded.

Function: read in data to use in gradient boosting regression code.
'''
def load_dataset(filename):
    df = pd.read_csv(filepath_or_buffer=filename, sep=',')

    # df.columns = ["name", "ncaa_fg3a", "ncaa_fg3_pct", "ncaa_ft_pct", "ncaa_sos", "ncaa_team_fg3a_avg",
    # 			"nba_avg_team_ortg", "nba_relative_team_fg3a", "nba_fg3_pct"]

    df.dropna(how="all", inplace=True) # drops the empty line at file-end
    df.tail()

    return df.values


'''
Parameters:
* df: the processed training data.

Function: Runs k-fold cross validation on the processed training data.
		  In this program, k = 10.
'''
def kfold_cv(df, k):
	kf = KFold(n_splits=k, random_state=0, shuffle=True)

	# Contains the averaged mean squared error for each model over the k folds.
	train_scores = np.repeat(0., 4)
	test_scores = np.repeat(0., 4)

	for train_index, test_index in kf.split(df):
		X_train, y_train = df[train_index][:,:4], df[train_index][:,-1]
		X_test, y_test = df[test_index][:,:4], df[test_index][:,-1]

		# Train using linear regression
		lm, pred_train, pred_test = lr.run_linear_regression(X_train, y_train, X_test, y_test)
		train_scores[0] += mean_squared_error(y_train, pred_train)
		test_scores[0] += mean_squared_error(y_test, pred_test)

		# Train using weighted linear regression
		lm, pred_train, pred_test = lr.run_weighted_regression(X_train, y_train, X_test, y_test)
		train_scores[1] += mean_squared_error(y_train, pred_train)
		test_scores[1] += mean_squared_error(y_test, pred_test)

		# Train using gradient boosting
		params = {}
		params['n_estimators'] = 3000
		params['learning_rate'] = .0001
		params['max_depth'] = 5

		pred_train, pred_test = gb.fit_model(X_train, y_train, X_test, y_test, params)
		train_scores[2] += mean_squared_error(y_train, pred_train)
		test_scores[2] += mean_squared_error(y_test, pred_test)

		# Train using random forest
		params.pop('learning_rate', None)
		params['max_depth'] = 4
		
		pred_train, pred_test = rf.fit_model(X_train, y_train, X_test, y_test, params)
		train_scores[3] += mean_squared_error(y_train, pred_train)
		test_scores[3] += mean_squared_error(y_test, pred_test)		


	train_scores /= k
	test_scores /= k

	print train_scores
	print test_scores



def main():
	train = load_dataset('transformed_train.csv')
	kfold_cv(train, 10)


if __name__ == '__main__':
	main()