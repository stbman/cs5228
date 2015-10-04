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

from sklearn import svm
from sklearn.neural_network import BernoulliRBM
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor

import preprocess

def svm_fit(df, query_data):
  svm_clf.fit(df_new[attributes], df_new['TotalDelay'])
  prediction = svm_clf.predict(query_data)[0] 
  return prediction

window_size = 20
window_start = 0
window_end = window_start + window_size
num_k_neighbours = window_size / 2

df = pd.read_csv('data/2007_weather_preprocess_shortened.csv')
attributes = list(df.columns.values)[1:]
attributes.remove('DateTime')
attributes.remove('PredDelay')

#df, attributes = preprocess.preprocess(df)

# Initialise Classifiers
svm_clf = svm.SVC()
bernolli_rbm_clf = BernoulliRBM(n_components=2)
decision_tree_clf = tree.DecisionTreeClassifier()

ada_boost_rgr = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4),
                          n_estimators=300, random_state=np.random.RandomState(1))

while window_end < len(df)-2:   # Because we can't predict the last one
  window_end = window_start + window_size
  window_start = window_start + 1
  
  query_index = window_end + 1
  
  df_new = df[window_start:window_end]
  df_new = df_new.drop(['DateTime', 'PredDelay'], axis=1)
  query_data = df.ix[query_index]
  query_data = query_data.drop(['DateTime', 'IsDelayed', 'PredDelay'])
  
  '''
  # SVM
  try:
    svm_clf.fit(df_new[attributes], df_new['IsDelayed'])
    prediction = svm_clf.predict(query_data)
  except:   # When all of them are the same class (i.e. not delayed)
    prediction = df_new['IsDelayed'].mode()

  # Bernolli RBF
  try: 
    bernolli_rbm_clf.fit(df_new[attributes], df_new['IsDelayed'])
    prediction = bernolli_rbm_clf.predict(query_data)
  except:
    prediction = df_new['IsDelayed'].mode()
  ''' 
 
  '''
  # Decision Trees
  try:
    decision_tree_clf.fit(df_new[attributes], df_new['IsDelayed'])
    prediction = decision_tree_clf.predict(query_data)
  except:
    prediction = df_new['IsDelayed'].mode()
  '''
  
  # Ada Boost Regressor
  try:
    ada_boost_rgr.fit(df_new[attributes], df_new['IsDelayed'])
    prediction = ada_boost_rgr.predict(query_data)
  except:
    prediction = df_new['IsDelayed'].mode()
 
  df = df.set_value(query_index, 'PredDelay', prediction)

# Computing Scores
prec_recall_score = precision_recall_fscore_support(df['IsDelayed'], df['PredDelay'])
print "Precision Recall Score: ", prec_recall_score