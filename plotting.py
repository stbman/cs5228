#!/usr/bin/python

'''
Trying to plot some data
'''

import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py 
from plotly.graph_objs import *

df = pd.read_csv('data/2007_weather.csv')

# Simple Preprocessing
df['TotalDelay'] = df.ArrDelay + df.DepDelay + df.CarrierDelay + df.WeatherDelay \
					+ df.NASDelay + df.SecurityDelay + df.LateAircraftDelay	
					
df['IsDelayed'] = df['TotalDelay'].apply(lambda x: 1 if x > 0 else 0)					

# Group by Origin
'''
grouped_by_origin = df[['IsDelayed', 'Origin']].groupby('Origin').sum()
grouped_by_origin = grouped_by_origin.sort(['IsDelayed'], ascending=False)
grouped_by_origin.plot(kind='bar')
plt.title('Number of Delayed Flights against Origin Airport')
plt.ylabel('Number of Delayed Flights')
plt.xlabel('Origin Airport')
plt.xticks(rotation=-30)
plt.show()


grouped_by_origin = df[['IsDelayed', 'Origin']].groupby('Origin').sum()
gdf = pd.DataFrame(grouped_by_origin)
gdf = gdf.sort(['IsDelayed'], ascending=False)
gdf[:20].plot(kind='bar')
plt.xticks(rotation=-30)

plt.figure()
'''

grouped_by_delay = df[['TotalDelay', 'ArrDelay', 'DepDelay', 'WeatherDelay', \
					  'NASDelay', 'SecurityDelay', 'LateAircraftDelay', 'Origin']].groupby('Origin').mean()
gdelay = pd.DataFrame(grouped_by_delay)
gdelay = gdelay.sort(['TotalDelay'], ascending=False)
df2 = pd.DataFrame(gdelay)
df2 = df2.drop(['TotalDelay'], axis=1)[:20]

py.image.save_as({
	'data': [Bar(
		x=df2.index, 
		y=df2[col],
		name=col
		) for col in df2.columns],
	'layout': Layout(
		xaxis={'title': 'Origin Airport Code'},
		yaxis={'title': 'Delay in Minutes'},
		title='Top 20 most delayed Airports'
	)
}, filename='delayedairports_2.png')
