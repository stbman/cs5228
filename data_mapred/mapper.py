#!/usr/bin/python

import sys

import pandas as pd 
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingRegressor

file_name = '2007_weather_short.csv'
window = int(sys.argv[1])   
#window = 50
k = window/2    # Thought windows should be of a ratio

iter_csv = pd.read_csv(file_name, iterator=True, chunksize=window)

knn = KNeighborsClassifier(n_neighbors=k)

# To change classifiers 
gbr = GradientBoostingRegressor(n_estimators=20, learning_rate=0.1,
                      max_depth=1, random_state=0, loss='ls')

for chunk in iter_csv:
    chunk = chunk.drop(['DateTime'], axis=1)
    
    attributes = chunk.columns.values
    attributes = np.delete(attributes, attributes.tolist().index('TotalDelay'))    
    
    training_chunk = chunk.iloc[:-1]
    predict_chunk = chunk.iloc[-1]
    actual = predict_chunk['TotalDelay']
    predict_chunk = predict_chunk.drop(['TotalDelay'])
        
    # KNN
    knn.fit(training_chunk[attributes], training_chunk['TotalDelay'])
    neighbours = knn.kneighbors(predict_chunk[attributes], return_distance=False).flatten()
    
    # Other classifiers
    new_training_chunk = training_chunk.ix[neighbours]

    try:
        gbr.fit(new_training_chunk[attributes], new_training_chunk['TotalDelay'])
        prediction = gbr.predict(predict_chunk)[0]
    except:
        prediction = new_training_chunk['TotalDelay'].mean()
    
    print prediction, actual
   



