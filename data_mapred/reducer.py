#!/usr/bin/python

import sys
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report

df = pd.DataFrame(columns=['actual', 'predicted'])

for line in sys.stdin:
    predicted, actual = line.strip().split(" ")
    df = df.append({'actual': float(actual), 'predicted': float(predicted)}, ignore_index=True)

rmse = np.sqrt(mean_squared_error(df['actual'], df['predicted']))

df['actualBoolean']    = df['actual'].map(lambda x: 1 if x > 15 else 0)    
df['predictedBoolean'] = df['predicted'].map(lambda x: 1 if x > 15 else 0)    

prec_recall_score   = precision_recall_fscore_support(df['actualBoolean'], df['predictedBoolean'])
num_corr_0          = prec_recall_score[3][0]
num_corr_1          = prec_recall_score[3][1]
num_corr_total      = num_corr_0 + num_corr_1
prec                = (prec_recall_score[0][0] * num_corr_0 + prec_recall_score[0][1] * num_corr_1) / num_corr_total
recall              = (prec_recall_score[1][0] * num_corr_0 + prec_recall_score[1][1] * num_corr_1) / num_corr_total
fscore              = (prec_recall_score[2][0] * num_corr_0 + prec_recall_score[2][1] * num_corr_1) / num_corr_total

#print classification_report(df['actualBoolean'], df['predictedBoolean'])
print rmse, prec, recall, fscore

