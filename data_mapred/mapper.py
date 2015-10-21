#!/usr/bin/python

import pandas as pd 
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingRegressor

file_name = '2007_weather_preprocess.csv'
window = 50

iter_csv = pd.read_csv(file_name, iterator=True, chunksize=window)

gbr = GradientBoostingRegressor(n_estimators=20, learning_rate=0.1,
                      max_depth=1, random_state=0, loss='ls')
import numpy as np
for chunk in iter_csv:
    chunk = chunk.drop(['DateTime'], axis=1)
    attributes = chunk.columns.values
    training_chunk = chunk.iloc[:-1]
    predict_chunk = chunk.iloc[-1]
    actual = predict_chunk['TotalDelay']
    predict_chunk = predict_chunk.drop(['TotalDelay'])
    attributes = np.delete(attributes, attributes.tolist().index("TotalDelay"))
    gbr.fit(training_chunk[attributes], training_chunk['TotalDelay'])
    prediction = gbr.predict(predict_chunk)[0]
    print prediction, actual


