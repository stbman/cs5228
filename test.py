#!/usr/bin/python
'''
Testing code, following a tutorial
'''

import warnings 
warnings.filterwarnings('ignore')

import os
import random
import numpy as np

from sklearn import linear_model, cross_validation, metrics, svm
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

import pandas as pd
import matplotlib.pyplot as plt

import pydoop.hdfs as hdfs

def read_csv_from_hdfs(path, col, col_types=None):
	files = hdfs.ls(path)
	pieces = []
	for f in files:
		fhandle = hdfs.open(f)
		pieces.append(pd.read_csv(fhandle, names=cols, dtype=col_types))
		fhandle.close()
	return pd.concat(pieces, ignore_index=True)
	
# Read the 2007 year file 
cols = ['year', 'month', 'day', 'dow', 'DepTime', 'CRSDepTime', 'ArrTime', 'CRSArrTime',
		'Carrier', 'FlightNum', 'TailNum', 'ActualElapsedTime', 'CRSElapsedTime', 'AirTime',
		'ArrDelay', 'DepDelay', 'Origin', 'Dest', 'Distance', 'TaxiIn', 'TaxiOut', 'Cancelled',
		'CancellationCode', 'Diverted', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 
		'SecurityDelay', 'LateAircraftDelay']
		
cwd = os.getcwd()
# Assume all the data files are stored in cwd/data
flt_2007 = read_csv_from_hdfs('/Users/lynnette/Documents/CS5228 Knowledge Discovery and Data Mining/cs5228/data/2007.csv', cols)
#print flt_2007.shape

df = flt_2007[flt_2007['Origin'] == 'ORD'].dropna(subset=['DepDelay'])
df['DepDelayed'] = df['DepDelay'].apply(lambda x: x>=15)
#print "total flights: " + str(df.shape[0])
#print "total delays: " + str(df['DepDelayed'].sum())

# Compute ave num of delayed flights per month
grouped = df[['DepDelayed', 'month']].groupby('month').mean()
grouped.plot(kind='bar')
# plt.show()

# Delayed flights per hour 
df['hour'] = df['CRSDepTime'].map(lambda x: int(str(int (x)).zfill(4)[:2]))
group_hour = df[['DepDelayed', 'hour']].groupby('hour').mean()
group_hour.plot(kind='bar')


# Ave number of delayed flights per carrier 
grouped1 = df[['DepDelayed', 'Carrier']].groupby('Carrier').filter(lambda x: len(x) > 10)
grouped2 = grouped1.groupby('Carrier').mean()
carrier = grouped2.sort(['DepDelayed'], ascending=False)
# Display top 15 destinations
carrier[:15].plot(kind='bar')

