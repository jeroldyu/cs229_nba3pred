"""
select_test_train.py
--------------------------------------
November 20th, 2017
Roland Centeno, Hilary Sun, Jerold Yu
--------------------------------------
This document contains the code to split the data in 80%-20% training and test datasets.
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as tls
import numpy as np
import random
from sklearn.model_selection import train_test_split

def main():
	df = pd.read_csv(filepath_or_buffer="data.csv", sep=',')
	# features + class
	df.columns = ["name", "ncaa_fg3a", "ncaa_fg3_pct", "ncaa_ft_pct", "ncaa_sos", "ncaa_team_fg3a_avg", "nba_avg_team_ortg", "nba_relative_team_fg3a", "nba_fg3_pct"]
	df.dropna(how="all", inplace=True) # drops the empty line at file-end
	df.tail()

	train, test = train_test_split(df, test_size = 0.2)

	train.to_csv("train.csv", sep = ',', columns = train, index=False)
	test.to_csv("test.csv", sep = ',', columns = test, index=False)

if __name__ == '__main__':
	main()