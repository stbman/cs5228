#!/usr/bin/python

import numpy as np
import pandas as pd 
from datetime import date

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support

from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor

# US Office of Personelle Management holidays
holidays = [
        date(2007, 1, 1), date(2007, 1, 15), date(2007, 2, 19), date(2007, 5, 28), date(2007, 6, 7), date(2007, 7, 4), \
        date(2007, 9, 3), date(2007, 10, 8), date(2007, 11, 11), date(2007, 11, 22), date(2007, 12, 25), \
        date(2008, 1, 1), date(2008, 1, 21), date(2008, 2, 18), date(2008, 5, 22), date(2008, 5, 26), date(2008, 7, 4), \
        date(2008, 9, 1), date(2008, 10, 13), date(2008, 11, 11), date(2008, 11, 27), date(2008, 12, 25) \
     ]

def days_from_nearest_holiday(year, month, day):
  d = date(year, month, day)
  x = [(abs(d-h)).days for h in holidays]
  return min(x)

window_size = 20
window_start = 0
window_end = window_start + window_size
query_index = window_end + 1
num_k_neighbours = window_size / 2

df = pd.read_csv('data/2007.csv')

#df['TestDate'] = pd.to_datetime(df.Year*10000 + df.Month*100 + df.DayofMonth + int(str(df['CRSDepTime'])[:2]) + int(str(df['CRSDepTime'])[2:]), format='%Y%m%d %H%m')

# TODO: Preprocess with hour/ minute 
# TODO: Include weather data

df['Date'] = pd.to_datetime(df.Year*10000 + df.Month*100 + df.DayofMonth, format='%Y%m%d')
df = df.drop(['Year', 'Month', 'DayofMonth'], axis=1)		# Because we combined them already
df = df.sort('Date')
df = df.reset_index()
df['PredDelay'] = np.NaN		# To fill up as predicted

# Convert nominal values to numeric ones 
# TODO: Better encoding to represent carriers/ tail numbers
print 'Converting Nominal values to numeric ones '
nominal_cols = ['UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'CancellationCode']
for col in nominal_cols:
	listOfItems = list(df[col].unique())
	df[col] = df[col].map(lambda x : listOfItems.index(x))

attributes = list(df.columns.values)[1:]
attributes.remove('Date')

# Combine all the delays into one 
# When flight is cancelled, Total Delay is NaN
df['TotalDelay'] = df.ArrDelay + df.DepDelay + df.CarrierDelay + df.WeatherDelay \
					+ df.NASDelay + df.SecurityDelay + df.LateAircraftDelay

df_new = df[window_start:window_end]
df_new = df_new.drop(['Date', 'PredDelay'], axis=1)
query_data = df.ix[query_index]
query_data = query_data.drop(['Date', 'TotalDelay', 'PredDelay'])

print "K Nearest Neighbours"
knn_clf = KNeighborsClassifier(n_neighbors=num_k_neighbours)
knn_clf.fit(df_new[attributes], df_new['TotalDelay'])
neighbours = knn_clf.kneighbors(query_data[attributes], return_distance=False).flatten()

df_new_neighbours = df_new.ix[neighbours]

print "Gradient Boosting Regressor"
gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, 
							max_depth=1, random_state=0, loss='ls')
gbr.fit(df_new[attributes], df_new['TotalDelay'])
prediction = gbr.predict(query_data)[0]
df = df.set_value(query_index, 'PredDelay', prediction)

print "Computing precision recall scores"
# TODO: Make a metric based on how close it is to actual delay time
'''
boolean_time = lambda x: time > 0
true_time = df['TotalDelay'].apply(boolean_time)
pred_delay_time = y_pred.apply(boolean_time)
prec_recall_score = precision_recall_fscore_support(true_time, pred_delay_time)
'''

print "Computing Root Mean Squared Error"
# Convert NaN to 999: force_all_finite
df['TotalDelay'].fillna(999)
df['PredDelay'].fillna(999)
rmse = np.sqrt(mean_squared_error(df['TotalDelay'], df['PredDelay'])
print rmse
