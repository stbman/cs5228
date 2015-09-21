Register 'util.py' USING jython as util;
DEFINE preprocess(year_str, airport_code) returns data
{
        -- load airline data from specified year (need to specify fields since it's not in HCat)
        airline = load '$year_str.csv' using PigStorage(',') 
            as (Year: int, Month: int, DayOfMonth: int, DayOfWeek: int, DepTime: chararray, 
                CRSDepTime: chararray, ArrTime, CRSArrTime, Carrier: chararray, FlightNum, TailNum, ActualElapsedTime, 
                CRSElapsedTime, AirTime, ArrDelay, DepDelay: int, Origin: chararray, Dest: chararray, Distance: int, 
                TaxiIn, TaxiOut, Cancelled: int, CancellationCode, Diverted, CarrierDelay, WeatherDelay, 
                NASDelay, SecurityDelay, LateAircraftDelay);

        -- keep only instances where flight was not cancelled and originate at ORD
        airline_flt = filter airline by Cancelled == 0 and Origin == '$airport_code';

        -- Keep only fields I need
        $data = foreach airline_flt generate DepDelay as delay, Month, DayOfMonth, DayOfWeek, 
                                             util.get_hour(CRSDepTime) as hour, Distance, Carrier, Dest,
                                             util.days_from_nearest_holiday(Year, Month, DayOfMonth) as hdays;
};

ORD_2007 = preprocess('/Users/lynnette/Documents/CS5228 Knowledge Discovery and Data Mining/cs5228/data/2007', 'ORD');
store ORD_2007 into '/Users/lynnette/Documents/CS5228 Knowledge Discovery and Data Mining/cs5228/data/2007_processed' using PigStorage(',');
