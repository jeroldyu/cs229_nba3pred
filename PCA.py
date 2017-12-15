"""
PCA.py
--------------------------------------
This document contains the code to transform the raw data using 
Principal Component Analysis.
"""

# LIBRARIES
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn import decomposition
import numpy as np


'''
Parameters:
* filename: csv file to be loaded.

Function: read in data to be transformed.
'''
def load_dataset(filename):
	
	df = pd.read_csv(filepath_or_buffer=filename, sep=',')

	columns = ["name", "ncaa_fg3a", "ncaa_fg3_pct", "ncaa_ft_pct", "ncaa_sos","ncaa_team_fg3a_avg",
			"nba_avg_team_ortg", "nba_relative_team_fg3a", "nba_fg3_pct"]
	df.columns = columns

	df.dropna(how="all", inplace=True) # drops the empty line at file-end
	df.tail()

	X = df.ix[:,1:7].values
	X[:,1:3] *= 100.
	Y = df.ix[:,-1].values
	Y *= 100.

	return X, Y


def main():
	X, Y = load_dataset("train.csv")
	X_std = StandardScaler().fit_transform(X)
	
	pca = decomposition.PCA(n_components=4)
	pca.fit(X_std)
	print("Explained variance ratios:")
	print(pca.explained_variance_ratio_)

	transformed_X = pca.transform(X_std)
	transformed_samples = np.hstack((transformed_X, np.matrix(Y).T))
	np.savetxt("transformed_train.csv", transformed_samples, delimiter=',')

	
	X_test, Y_test = load_dataset("test.csv")
	X_test_std = StandardScaler().fit_transform(X_test)

	transformed_X_test = pca.transform(X_test_std)
	transformed_samples_test = np.hstack((transformed_X_test, np.matrix(Y_test).T))
	np.savetxt("transformed_test.csv", transformed_samples_test, delimiter=',')


if __name__ == '__main__':
	main()