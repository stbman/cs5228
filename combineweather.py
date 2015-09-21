#!/usr/bin/python

'''
Combining weather data with flight data 
For Year 2007 
'''

import os
import datetime
from datetime import date 
import linecache

import numpy as np
import pandas as pd

import pydoop.hdfs as hdfs

def read_csv_from_hdfs(path, col, col_types=None):
	files = hdfs.ls(path)
	pieces = []
	for f in files:
		fhandle = hdfs.open(f)
		pieces.append(pd.read_csv(fhandle, names=col, dtype=col_types))
		fhandle.close()
	return pd.concat(pieces, ignore_index=True)
	
def mean_weather_data():
	time_frame = pd.date_range(datetime.date(2007,01,01), datetime.date(2008,12,31))
	time_frame_mapped = map(lambda x: int(float(x.strftime("%Y%m%d"))), time_frame)
	cols = ['STATION', 'STATION_NAME', 'DATE', 'PRCP', 'TMAX', 'TMIN', 'AWND', 'NUM_PRCP', 'NUM_TMAX', 'NUM_TMIN', 'NUM_AWND']
	
	df = pd.DataFrame(index=range(len(time_frame)), columns=cols)

	# Variables for num station points
	df['NUM_AWND'] = 0
	df['NUM_TMAX'] = 0
	df['NUM_TMIN'] = 0
	df['NUM_AWND'] = 0
	df['NUM_PRCP'] = 0

	df['DATE'] = time_frame_mapped
	df['STATION'] = 'USA'
	df['STATION_NAME'] = 'USA'
	
	df['TMAX'] = 0 
	df['TMIN'] = 0
	df['AWND'] = 0
	df['PRCP'] = 0
	
	for file in os.listdir('data/weather'):
		df_file = pd.read_csv('data/weather/'+file)
		
		try: 
			df['TMAX'] = df['TMAX'] + df_file['TMAX']
			df['NUM_TMAX'] = df['NUM_TMAX'] + 1
		except:
			pass
		try: 
			df['TMIN'] = df['TMIN'] + df_file['TMIN']
			df['NUM_TMIN'] = df['NUM_TMIN'] + 1
		except: 
			pass
		try:
			df['AWND'] = df['AWND'] + df_file['AWND']
			df['NUM_AWND'] = df['NUM_AWND'] + 1
		except: 
			pass

		try: 
			df['PRCP'] = df['PRCP'] + df_file['PRCP']
			df['NUM_PRCP'] = df['NUM_PRCP'] + 1
		except:
			pass

	# Average out 
	df['TMAX'] = int(df['TMAX']/df['NUM_TMAX'])
	df['TMIN'] = int(df['TMIN']/df['NUM_TMIN'])
	df['AWND'] = int(df['AWND']/df['NUM_AWND'])
	df['PRCP'] = int(qdf['PRCP']/df['NUM_PRCP'])
				
	df.to_csv('USA.csv', index=None)

	return df
	
def combine_weather():
	cols = ['Year', 'Month', 'Day', 'DayOfWeek', 'DepTime', 'CRSDepTime', 'ArrTime', 'CRSArrTime',
			'Carrier', 'FlightNum', 'TailNum', 'ActualElapsedTime', 'CRSElapsedTime', 'AirTime',
			'ArrDelay', 'DepDelay', 'Origin', 'Dest', 'Distance', 'TaxiIn', 'TaxiOut', 'Cancelled',
			'CancellationCode', 'Diverted', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 
			'SecurityDelay', 'LateAircraftDelay']
			
	# Read the 2007 year file, stored in data/2007.csv 
	
	cwd = os.getcwd()
	
	flt_2007 = read_csv_from_hdfs(cwd + '/data/2007.csv', cols)
	flt_2007 = flt_2007.ix[1:]
	
	print 'Got Year 2007 Flight Data'
	
	start_date = date(2007, 01, 01)
	
	flt_2007['tmax'] = np.nan
	flt_2007['tmin'] = np.nan
	flt_2007['wind'] = np.nan
	flt_2007['precipitation'] = np.nan
	
	print 'Combining Weather'
	for index, row in flt_2007.iterrows():
		print index
	
		flight_date = date(int(float(row.Year)), int(float(row.Month)), int(float(row.Day)))
		diff = (flight_date-start_date).days
		
		filename = row.Origin + '.csv'
		
		line = linecache.getline('data/weather/' + filename, diff+2) # 2 because file count starts on line 1 and first line is header
		if line is '':
			line = linecache.getline('USA.csv', diff+2) # 2 because file count starts on line 1 and first line is header
			
		line_array = line.split(',')
		
		print line_array
		
		precipitation = int(float(line_array[3]))
		tmax = int(float(line_array[5]))
		tmin = int(float(line_array[6]))
		wind = int(float(line_array[7]))	

	flt_2007.to_csv('2007_weather.csv')
	
if __name__ == "__main__":
	#pass
	combine_weather()