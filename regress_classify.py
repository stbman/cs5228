#!/usr/bin/python

'''
For regressions and classifications to be used together in one pass
'''

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.neural_network import BernoulliRBM
from sklearn import tree

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor

from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_recall_fscore_support

import preprocess

df_regOutput = pd.DataFrame()
df_booleanOutput = pd.DataFrame()

df = pd.read_csv('data/2007_weather_preprocess.csv')
#df, attributes = preprocess.preprocess(df)
attributes = list(df.columns.values)[1:]
attributes.remove('DateTime')
attributes.remove('PredDelay')

# Initialise Regressors
regressors = {'gbr_reg': GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, 
                max_depth=1, random_state=0, loss='ls'),
              'ada_reg': AdaBoostRegressor(DecisionTreeRegressor(max_depth=4),
                n_estimators=300, random_state=np.random.RandomState(1))
              }

# Initialise Classifiers 
classifiers = {'svm_clf': svm.SVC(),
                'bernolli_rbm_clf': BernoulliRBM(n_components=2),
                'decision_tree_clf': tree.DecisionTreeClassifier()
               }
              
window_size = 20
window_start = 0
window_end = window_start + window_size
print "Window Size: ", window_size

while window_end < len(df)-2:   # Because we can't predict the last one
  window_end = window_start + window_size
  window_start = window_start + 1
  
  query_index = window_end + 1
  
  df_new = df[window_start:window_end]
  df_new = df_new.drop(['DateTime', 'PredDelay'], axis=1)
  query_data = df.ix[query_index]
  query_data = query_data.drop(['DateTime', 'TotalDelay', 'PredDelay'])

  for name, reg in regressors.items():
    reg.fit(df_new[attributes], df_new['TotalDelay'])
    prediction = reg.predict(query_data)[0]
    df_regOutput = df_regOutput.set_value(query_index, name + 'PredDelay', prediction)
    
  for name, clf in classifiers.items():
    try:
      clf.fit(df_new[attributes], df_new['IsDelayed'])
      prediction = clf.predict(query_data)
    except:   # In case all the classes are the same 
      prediction = df_new['IsDelayed'].mode()
    df_booleanOutput = df_booleanOutput.set_value(query_index, name + 'PredDelay', prediction)
  
# Computing Scores
df_booleanOutput = pd.concat([df_booleanOutput,
                    df_regOutput.applymap(lambda x: 1 if x > 0 else 0)])

df_booleanOutput = df_booleanOutput.fillna(999)
df_regOutput = df_regOutput.fillna(999)

for col_name, col in df_regOutput.iteritems():
  rmse = np.sqrt(mean_squared_error(df['TotalDelay'][window_size+1:], col))
  print col_name, " RMSE: " , rmse
  
for col_name, col in df_booleanOutput.iteritems():
  prec_recall_score = precision_recall_fscore_support(df['IsDelayed'][window_size+1:], col)
  precision = prec_recall_score[0]
  recall = prec_recall_score[1]
  fscore = prec_recall_score[2]
  num_corr = prec_recall_score[3]
  print col_name, " Precision Recall Score: ", precision, recall, fscore, num_corr