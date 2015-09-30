#!/usr/bin/python

import numpy as np
import pandas as pd 

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support

from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor

import preprocess

window_size = 20
window_start = 0
window_end = window_start + window_size
num_k_neighbours = window_size / 2

df = pd.read_csv('data/2007_shortened_weather.csv')
df = preprocess.preprocess(df)

attributes = list(df.columns.values)[1:]
attributes.remove('DateTime')
attributes.remove('PredDelay')

# Initialise Regressors
gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, 
              max_depth=1, random_state=0, loss='ls')
knn_clf = KNeighborsClassifier(n_neighbors=num_k_neighbours)

while window_end < len(df)-2:   # Because we can't predict the last one
  window_end = window_start + window_size
  window_start = window_start + 1
  
  query_index = window_end + 1
  
  df_new = df[window_start:window_end]
  df_new = df_new.drop(['DateTime', 'PredDelay'], axis=1)
  query_data = df.ix[query_index]
  query_data = query_data.drop(['DateTime', 'TotalDelay', 'PredDelay'])
  
  ''' Not sure why KNN Doesn't work :( 
  # KNN
  knn_clf.fit(df_new[attributes], df_new['TotalDelay'])
  neighbours = knn_clf.kneighbors(query_data[attributes], return_distance=False).flatten()
  df_new_neighbours = df_new.ix[neighbours]
  '''

  # Gradient Boosting Regressor
  gbr.fit(df_new[attributes], df_new['TotalDelay'])
  prediction = gbr.predict(query_data)[0]
  df = df.set_value(query_index, 'PredDelay', prediction)

# Computing Scores
print "Computing precision recall scores"
# TODO: Make a boolean set (Perceptron etc)
'''
boolean_time = lambda x: time > 0
true_time = df['TotalDelay'].apply(boolean_time)
pred_delay_time = y_pred.apply(boolean_time)
prec_recall_score = precision_recall_fscore_support(true_time, pred_delay_time)
'''

print "Computing Root Mean Squared Error"
# Convert NaN to 999: force_all_finite
df['TotalDelay'] = df['TotalDelay'].fillna(999)
df['PredDelay'] = df['PredDelay'].fillna(999)
rmse = np.sqrt(mean_squared_error(df['TotalDelay'], df['PredDelay']))
print rmse
