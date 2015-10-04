#!/usr/bin/python

'''
For regressions
'''

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support

from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor

import preprocess

def gradient_boosted_regressor_fit(df, query_data):
  gbr.fit(df[attributes], df['TotalDelay'])
  prediction = gbr.predict(query_data)[0] 
  return prediction

df_metrics = pd.DataFrame(columns=['WindowSize', 'PrecisionNotDelayed', 'PrecisionDelayed' \
                                      'RecallNotDelayed', 'RecallDelayed', 'FNotDelayed', 'FDelayed', \
                                      'NumCorrDelayed', 'NumCorrNotDelayed', 'RMSE'])

df = pd.read_csv('data/2007_shortened_weather.csv')
df, attributes = preprocess.preprocess(df)

# Initialise Regressors
gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, 
              max_depth=1, random_state=0, loss='ls')

test = []

iteration_num = 0
for i in xrange(10, 100, 10):
  window_size = i
  window_start = 0
  window_end = window_start + window_size   
  
  while window_end < len(df)-2:   # Because we can't predict the last one
    window_end = window_start + window_size
    window_start = window_start + 1
    
    query_index = window_end + 1
    
    df_new = df[window_start:window_end]
    df_new = df_new.drop(['DateTime', 'PredDelay'], axis=1)
    query_data = df.ix[query_index]
    query_data = query_data.drop(['DateTime', 'TotalDelay', 'PredDelay'])
  
    # Gradient Boosting Regressor
    prediction = gradient_boosted_regressor_fit(df_new, query_data)
    df = df.set_value(query_index, 'PredDelay', prediction)
  
  # Computing Scores
  pred_delay_time = df['PredDelay'].apply(lambda x: 1 if x > 0 else 0)
  prec_recall_score = precision_recall_fscore_support(df['IsDelayed'], pred_delay_time)
  precision = prec_recall_score[0]
  recall = prec_recall_score[1]
  fscore = prec_recall_score[2]
  num_corr = prec_recall_score[3]
  print "Precision Recall Score: ", precision, recall, fscore, num_corr
  
  test.append(prec_recall_score)
  
  df['TotalDelay'] = df['TotalDelay'].fillna(999)   # Force All Finite
  df['PredDelay'] = df['PredDelay'].fillna(999)
  rmse = np.sqrt(mean_squared_error(df['TotalDelay'], df['PredDelay']))
  print "Window Size: " , window_size, " Root Mean Square Error: ", rmse
  
  df_metrics = df_metrics.set_value(iteration_num, 'WindowSize', window_size)
  df_metrics = df_metrics.set_value(iteration_num, 'RMSE', rmse)
  df_metrics = df_metrics.set_value(iteration_num, 'PrecisionDelayed', precision[0])
  df_metrics = df_metrics.set_value(iteration_num, 'PrecisionNotDelayed', precision[1])  
  df_metrics = df_metrics.set_value(iteration_num, 'RecallDelayed', recall[0])
  df_metrics = df_metrics.set_value(iteration_num, 'RecallNotDelayed', recall[1])   
  df_metrics = df_metrics.set_value(iteration_num, 'FDelayed', fscore[0])
  df_metrics = df_metrics.set_value(iteration_num, 'FNotDelayed', fscore[1])   
  df_metrics = df_metrics.set_value(iteration_num, 'NumCorrDelayed', num_corr[0])
  df_metrics = df_metrics.set_value(iteration_num, 'NumCorrNotDelayed', num_corr[1])       
  
  iteration_num = iteration_num + 1
  
# Plot the data
fig = plt.figure()
plt.plot(df_metrics['WindowSize'], df_metrics['RMSE'])
plt.xlabel('Window Size')
plt.ylabel('Root Mean Square Error')
plt.title('RMSE vs Window Size')
plt.savefig('RMSE.png')

fig = plt.figure()
plt.plot(df_metrics['WindowSize'], df_metrics['PrecisionDelayed'])
plt.plot(df_metrics['WindowSize'], df_metrics['RecallDelayed'])
plt.legend(['Precision Delayed', 'Recall Delayed'], loc='upper left')
plt.xlabel('Window Size')
plt.savefig('PrecisionRecall.png')

#plt.show()
