#
# Python UDFs for our PIG script
#
from datetime import date

# get hour-of-day from HHMM field
@outputSchema("value: int")
def get_hour(val):
  return int(val.zfill(4)[:2])

# this array defines the dates of holiday in 2007 and 2008
holidays = [
        date(2007, 1, 1), date(2007, 1, 15), date(2007, 2, 19), date(2007, 5, 28), date(2007, 6, 7), date(2007, 7, 4), \
        date(2007, 9, 3), date(2007, 10, 8), date(2007, 11, 11), date(2007, 11, 22), date(2007, 12, 25), \
        date(2008, 1, 1), date(2008, 1, 21), date(2008, 2, 18), date(2008, 5, 22), date(2008, 5, 26), date(2008, 7, 4), \
        date(2008, 9, 1), date(2008, 10, 13), date(2008, 11, 11), date(2008, 11, 27), date(2008, 12, 25) \
     ]
# get number of days from nearest holiday
@outputSchema("days: int")
def days_from_nearest_holiday(year, month, day):
  d = date(year, month, day)
  x = [(abs(d-h)).days for h in holidays]
  return min(x)