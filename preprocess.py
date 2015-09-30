#!/usr/bin/python

'''
This class preprocesses the dataframe
1. Combine Year, Month, DayofMonth, CRSDepTime (The scheduled departure time)
into a datetime object
2. Add all the delays together to get Total Delay 
3. Drop data columns used in (1) and (2) to avoid duplicates
4. Get days from nearest holidays_2007 (from US Office)
5. Create IsDelayed to convert Total Delay to Boolean
6. Create a PredDelay column for predicted number of minutes of delay
7. Convert nominal columns to numeric ones 
8. Cancellation Code if does not exist, force it to be 999 
Cannot have NaN for the Machine Learning
9. Sort dataframe by date
'''

import pandas as pd
import numpy as np
from datetime import datetime

# US Office of Personelle Management holidays
holidays_2007 = [
        datetime(2007, 1, 1), datetime(2007, 1, 15), datetime(2007, 2, 19), datetime(2007, 5, 28), datetime(2007, 6, 7), datetime(2007, 7, 4), \
        datetime(2007, 9, 3), datetime(2007, 10, 8), datetime(2007, 11, 11), datetime(2007, 11, 22), datetime(2007, 12, 25), \
        datetime(2008, 1, 1), datetime(2008, 1, 21), datetime(2008, 2, 18), datetime(2008, 5, 22), datetime(2008, 5, 26), datetime(2008, 7, 4), \
        datetime(2008, 9, 1), datetime(2008, 10, 13), datetime(2008, 11, 11), datetime(2008, 11, 27), datetime(2008, 12, 25) \
     ]

nominal_cols = ['UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'CancellationCode']

def days_from_nearest_holiday(d):
  d = np.datetime64(d).astype(datetime)
  x = [(abs(d-h)).days for h in holidays_2007]
  return min(x)

def preprocess(df): 
	# (1) 
	df['DepHour'] = df['CRSDepTime'].apply(lambda x: int(str(x).zfill(4)[:2]))
	df['DepMin'] = df['CRSDepTime'].apply(lambda x: int(str(x).zfill(4)[2:]))
	df['DateTime'] = df[['Year', 'Month', 'DayofMonth', 'DepHour', 'DepMin']].apply(lambda s : datetime(*s), axis = 1)
	
	# (2)
	# Note: We could consider using each delay separately to see results? 
	df['TotalDelay'] = df.ArrDelay + df.DepDelay + df.CarrierDelay + df.WeatherDelay \
						+ df.NASDelay + df.SecurityDelay + df.LateAircraftDelay		
	
	# (3)
	df = df.drop(['Year', 'Month', 'DayofMonth', 'DepHour', 'DepMin', \
					'ArrDelay', 'DepDelay', 'CarrierDelay', 'WeatherDelay', \
					'NASDelay', 'SecurityDelay', 'LateAircraftDelay'], axis=1)
	
	# (4)
	df['DaysFromHoliday'] = df['DateTime'].apply(days_from_nearest_holiday)
	
	# (5)
	df['IsDelayed'] = df['TotalDelay'].apply(lambda x: 1 if x > 0 else 0)
	
	# (6)
	df['PredDelay'] = np.NaN
	
	# (7)
	for col in nominal_cols:
		listOfItems = list(df[col].unique())
		df[col] = df[col].map(lambda x : listOfItems.index(x))
	
	# (8)
	df['CanellationCode'] = df['CancellationCode'].fillna(999)
	df = df.fillna(0)		# Just in case any NaNs appear in frame
	
	# (9)
	df = df.sort('DateTime')
	df = df.reset_index()	# To fill up as being predicted
	
	return df