#!/usr/bin/python

'''
For Classifications
- SVM
- Bernolli Neural Networks 
- Decision Trees
'''

import numpy as np
import pandas as pd 

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support

from sklearn.metrics import mean_squared_error
from sklearn import svm

import preprocess

def svm_fit(df, query_data):
  svm_clf.fit(df_new[attributes], df_new['TotalDelay'])
  prediction = svm_clf.predict(query_data)[0] 
  return prediction

window_size = 20
window_start = 0
window_end = window_start + window_size
num_k_neighbours = window_size / 2

df = pd.read_csv('data/2007_weather.csv')
df, attributes = preprocess.preprocess(df)

# Initialise Classifiers
svm_clf = svm.SVC()

while window_end < len(df)-2:   # Because we can't predict the last one
  window_end = window_start + window_size
  window_start = window_start + 1
  
  query_index = window_end + 1
  
  df_new = df[window_start:window_end]
  df_new = df_new.drop(['DateTime', 'PredDelay'], axis=1)
  query_data = df.ix[query_index]
  query_data = query_data.drop(['DateTime', 'TotalDelay', 'PredDelay'])
  
  prediction = svm_fit(df_new, query_data)
  df = df.set_value(query_index, 'PredDelay', prediction)

# Computing Scores
prec_recall_score = precision_recall_fscore_support(df['IsDelayed'], df['PredDelay'])
print "Precision Recall Score: ", prec_recall_score