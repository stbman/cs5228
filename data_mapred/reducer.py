#!/usr/bin/python

import sys
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_recall_fscore_support

df = pd.DataFrame(columns=['actual', 'predicted'])

for line in sys.stdin:
    predicted, actual = line.strip().split(" ")
    df = df.append({'actual': actual, 'predicted': predicted}, ignore_index=True)

rmse = np.sqrt(mean_squared_error(df['actual'], df['predicted']))

df['actualBoolean']    = df['actual'].map(lambda x: 1 if x > 15 else 0)    
df['predictedBoolean'] = df['predicted'].map(lambda x: 1 if x > 15 else 0)    

#print df


prec_recall_score   = precision_recall_fscore_support(df['actualBoolean'], df['predictedBoolean'])
prec_delayed        = prec_recall_score[0][1]
recall_delayed      = prec_recall_score[1][1]
fscore_delayed      = prec_recall_score[2][1]
num_corr            = prec_recall_score[3][1]
    
print rmse, prec_delayed, recall_delayed, fscore_delayed, num_corr

