# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 16:19:29 2020

The below code will, given a set or query coordinates, a time range and an acceptable search radius, return 
all weather data within the query radius. 

@author: maxbird
"""
from weather_query_backend import weatherDatabase
import pandas as pd

################## USER INPUTS ###############################################

lat = 51.5042 # latitude coordinate of query location
lon = -0.12948 # longitude coordinate of query location
radius = 30 # maximum radius (km) you want your weather station to be within
start = '01/01/2020' ## dd/mm/yyyy format 
end = '01/05/2021' ## dd/mm/yyyy format 
station = 1 # 0 indexed number you want to pull data from within the specified radius. E.g. 0 uses closest station, 1 uses next closest etc.

################## USER INPUTS ###############################################

'''
Below function returns:
    
    1). rainfallData: a dataframe containing the time-series data for the rainfall
    
    2). stationMetaData: a dataframe containing meta data about all weather stations which fall within the specified search radius.
                                          
Errors:
    - If the code returns 'IndexError: list index out of range' it usually means there is not a weather station within the radius you have specified

'''
weatherQuery = weatherDatabase(lat, lon, radius)
rainfallData, stationMetaData = weatherQuery.getRainfallData(start, end, 0)
weatherData, stationMetaData = weatherQuery.getWeatherData(start, end, 0)
# insolationData, stationMetaData = weatherQuery.getInsolationData(start, end, 1)



'''
Manipulating the data you have just queried. Here are some useful links:
    - https://stackoverflow.com/questions/16967165/getting-the-average-of-a-certain-hour-on-weekdays-over-several-years-in-a-pandas
    - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
    - https://realpython.com/pandas-groupby/
    
I also recommend playing around with the below code examples to understand how the groupby function really works
    
''' 

# The below line will return the mean for each hourly variable over the entire query period
# test = weather.groupby([weather['Timestamp'].dt.hour]).mean()

# The below line will return the mean of each day over the entire query period
# test = weather.groupby([weather['Timestamp'].dt.day]).mean()

# The below line will return the mean of each month over the entire query period
# test = weather.groupby([weather['Timestamp'].dt.month]).mean()

# The below line will return the mean of each day for each individual year in the entire query period
# test = weather.groupby([weather['Timestamp'].dt.year, weather['Timestamp'].dt.day]).mean()

# # The below line will return the mean of each month in a year for each individual year in the entire query period
# test = weather.groupby([weather['Timestamp'].dt.year, weather['Timestamp'].dt.month]).mean()

# # The below line will return the mean of each day in a month for each individual year in the entire query period
# test = weather.groupby([weather['Timestamp'].dt.year, weather['Timestamp'].dt.day]).mean()

## you can also change the .mean() at the end to a different operation if you need to


# test = rainfallData.groupby([rainfallData['Timestamp'].dt.day]).mean()




