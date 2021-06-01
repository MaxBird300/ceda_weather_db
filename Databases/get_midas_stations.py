# -*- coding: utf-8 -*-
"""
Created on Mon May 17 11:09:03 2021

1). Pull all weather stations ID's out of the weather database
2). Search the weather station details here - https://archive.ceda.ac.uk/midas_stations/
3). Insert all these new details into a new table in the weather database to facilitate weather querying


- weather data description: https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/WH_Table.html
- Irradiance data description: https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/RO_Table.html
- Rainfall data description: https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/RH_Table.html



@author: maxbi
"""
import pandas as pd
import sqlite3
import numpy as np


startYear = 2021
endYear = 2021
# databaseName = 'Weather_DB.sqlite'
databaseName = 'test.sqlite'

rainfallStations = []
weatherStations = []
insolationStations = []
masterStations = []

# get ids for rainfall stations
# for year in range(startYear, endYear+1): # range function goes up to but NOT including the last value
#     print("Finding rainfall stations for %s" % (year))
#     location = './raw_data/midas_rainhrly_' + str(year) + '01-' + str(year) + '12.txt' # raw data path
    
    
#     data = pd.read_csv(location, sep=",", header=None, usecols=[0,3,4,5,6,8]) # imports the text file  

#     # remove daily readings, leave only hourly
#     mask = data.iloc[:,1] == 1
#     data = data[mask]
    
#     # Below two lines remove all data points which have not been quallity checked by MIDAS
#     mask = data.iloc[:,2] == 1
#     data = data[mask]
    
#     # take data only from SREW - https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/met_domain.html
#     mask = data.iloc[:,3] == " SREW"
#     data = data[mask]
    
#     for station in data.iloc[:,4]:
#         if station not in rainfallStations:
#             rainfallStations.append(station)        
        
# # get ids for insolation stations       
# for year in range(startYear, endYear+1): # range function goes up to but NOT including the last value
#     print("Finding insolation stations for %s" % (year))
#     location = './raw_data/midas_radtob_' + str(year) + '01-' + str(year) + '12.txt' # raw data path
    
#     data = pd.read_csv(location, sep=",", header=None, usecols=[2,3,4,5,6,8]) # imports the text file  

#     # remove daily readings, leave only hourly
#     mask = data.iloc[:,1] == 1
#     data = data[mask]
    
#     # Below two lines remove all data points which have not been quallity checked by MIDAS
#     mask = data.iloc[:,2] == 1
#     data = data[mask]
    
#     # take data only from HCM - https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/met_domain.html
#     mask = data.iloc[:,3] == " HCM"
#     data = data[mask]  

#     for station in data.iloc[:,4]:
#         if station not in insolationStations:
#             insolationStations.append(station)
      
        
# # get ids for weather stations        
# for year in range(startYear, endYear+1): # range function goes up to but NOT including the last value
#     print("Finding weather stations for %s" % (year))
#     location = './raw_data/midas_wxhrly_' + str(year) + '01-' + str(year) + '12.txt' # raw data path
    
#     data = pd.read_csv(location, sep=",", header=None, usecols=[0,3,4,5,9]) # imports the text file    
    
#     # Below two lines remove all data points which have not been quallity checked by MIDAS
#     mask = data.iloc[:,2] == 1
#     data = data[mask]
    
#     # select only SYNOP data - https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/met_domain.html
#     mask = data.iloc[:,1] == " SYNOP"
#     data = data[mask]
    
#     for station in data.iloc[:,3]:
#         if station not in weatherStations:
#             weatherStations.append(station) 
 
        
# # get master list of all available stations for all weather types      
# for x in [rainfallStations,weatherStations,insolationStations]:
#     for station in x:
#         if station not in masterStations:
#             masterStations.append(station)
            
            
# ######## Extract data from excel download from midas website (step 2) #########

# stationDetails = pd.read_excel("./raw_data/excel_list_station_details.xlsx", skiprows=1)

# stationDetails['weather collected (?)'] = False
# stationDetails['insolation collected (?)'] = False
# stationDetails['rainfall collected (?)'] = False

# for row in range(len(stationDetails)):
    
#     stationId = stationDetails.loc[row, "src_id"]
    
#     if stationId in weatherStations:
#         stationDetails.loc[row, 'weather collected (?)'] = True
#     if stationId in insolationStations:
#         stationDetails.loc[row, 'insolation collected (?)'] = True
#     if stationId in rainfallStations:
#         stationDetails.loc[row, 'rainfall collected (?)'] = True


# stationDetails.drop(columns=["Area type"], inplace=True)
# stationDetails.to_excel("./raw_data/processed_midas_station_details_May2021.xlsx")


######## STEP 3 ###################################

sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)    


conn = sqlite3.connect(databaseName)     
cur = conn.cursor()

#Below code generates the table in the sqlite database
cur.executescript('''
DROP TABLE IF EXISTS MIDAS_stations;                  

CREATE TABLE MIDAS_stations (
    station_id INTEGER,
    name  STRING,
    start_date STRING,
    end_date STRING,
    latitude FLOAT,
    longitude FLOAT,
    postcode STRING,
    weather_collected BOOL,
    insolation_collected BOOL,
    rainfall_collected BOOL,
    PRIMARY KEY (station_id)    
);

''')

stationDetails = pd.read_excel("./raw_data/processed_midas_station_details_May2021.xlsx", usecols=[1,2,4,5,6,7,8,9,10,11])
stationDetails.columns = ["station_id","name","start_date","end_date","latitude","longitude","postcode","weather_collected","insolation_collected","rainfall_collected"]


stationDetails.to_sql("MIDAS_stations", con=conn, if_exists='append', index=False)
conn.close()
print("Table successfully added to database")






