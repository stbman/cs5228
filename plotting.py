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
'''

grouped_by_delay = df[['ArrDelay', 'DepDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', \
             'CarrierDelay', 'LateAircraftDelay', 'Origin']].groupby('Origin').mean()
gdelay = pd.DataFrame(grouped_by_delay)
gdelay['TotalDelay'] = gdelay.ArrDelay + gdelay.DepDelay + gdelay.CarrierDelay + \
                        gdelay.WeatherDelay + gdelay.NASDelay + gdelay.SecurityDelay + \
                        gdelay.LateAircraftDelay
gdelay = gdelay.sort(['TotalDelay'], ascending=False)[:20]
gdelay = gdelay.drop(['TotalDelay'], axis=1)

py.image.save_as({
    'data': [Bar(
        x=gdelay.index, 
        y=gdelay[col],
        name=col
        ) for col in gdelay.columns],
    'layout': Layout(
        barmode='stack',
        xaxis={'title': 'Origin Airport Code'},
        yaxis={'title': 'Delay in Minutes'},
        title='Top 20 most delayed Airports'
    )
}, filename='delayedairports_2.png')

#gdf[:20].plot(kind='bar')
#plt.xticks(rotation=-30)
#plt.figure()


# Grouped by delay
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


# Group by day of month
grouped_by_month = df[['IsDelayed', 'DayofMonth']].groupby('DayofMonth').sum()
gmonth = pd.DataFrame(grouped_by_month)

py.image.save_as({
    'data': [Bar(
        x=gmonth.index, 
        y=gmonth['IsDelayed']
        )],
    'layout': Layout(
        xaxis={'title': 'Day of Month'},
        yaxis={'title': 'Number of Delays'},
        title='Number of Delays by Day of Month in 2007'
    )
}, filename='dayofmonth_delays.png')

# Group by month
grouped_by_month = df[['IsDelayed', 'Month']].groupby('Month').sum()
gmonth = pd.DataFrame(grouped_by_month)

py.image.save_as({
    'data': [Bar(
        x=gmonth.index, 
        y=gmonth['IsDelayed']
        )],
    'layout': Layout(
        xaxis={'title': 'Month'},
        yaxis={'title': 'Number of Delays'},
        title='Number of Delays by Month in 2007'
    )
}, filename='month_delays.png')

# Group by day of week
grouped_by_week = df[['IsDelayed', 'DayOfWeek']].groupby('DayOfWeek').sum()
gweek = pd.DataFrame(grouped_by_week)

py.image.save_as({
    'data': [Bar(
        x=gweek.index, 
        y=gweek['IsDelayed']
        )],
    'layout': Layout(
        xaxis={'title': 'Day of Week'},
        yaxis={'title': 'Number of Delays'},
        title='Number of Delays by Day of Week in 2007'
    )
}, filename='week_delays.png')

# Group by Unique Carrier 
grouped_by_carrier = df[['IsDelayed', 'UniqueCarrier']].groupby('UniqueCarrier').sum()
gcarrier = pd.DataFrame(grouped_by_carrier)
gcarrier = gcarrier.sort(['IsDelayed'], ascending=False)

py.image.save_as({
    'data': [Bar(
        x=gcarrier.index, 
        y=gcarrier['IsDelayed']
        )],
    'layout': Layout(
        xaxis={'title': 'Unique Carriers'},
        yaxis={'title': 'Number of Delays'},
        title='Top 20 most number of delays Carriers in 2007'
    )
}, filename='carrier_delays.png')
