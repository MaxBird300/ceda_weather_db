# -*- coding: utf-8 -*-
"""
Created on Thu May 13 13:59:39 2021

- weather data description: https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/WH_Table.html
- Irradiance data description: https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/RO_Table.html
- Rainfall data description: https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/RH_Table.html

@author: maxbi
"""
import sqlite3
from datetime import datetime
import pandas as pd
import numpy as np

sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)    

databaseName = 'test.sqlite'

def timestamp2unix(val): # calcualtes unix time (number of seconds since 1970) from timestamp
    time_count = datetime.strptime('1970-01-01 00:00', '%Y-%m-%d %H:%M')
    try:
        time_id = int((datetime.strptime(val, '%Y-%m-%d %H:%M')-time_count).total_seconds())
    except ValueError: # sometime irradiance timestamps have an extra space
        time_id = int((datetime.strptime(val, ' %Y-%m-%d %H:%M')-time_count).total_seconds())
    return time_id


def weather2sql(startYear, endYear):
    
    conn = sqlite3.connect(databaseName)
    cur = conn.cursor()
    
    #Below code generates the table in the sqlite database
    cur.executescript('''                          
    CREATE TABLE IF NOT EXISTS Weather (
        unix_time INTEGER,
        station_id INTEGER,
        wind_direction_degrees  INTEGER,
        wind_speed_knots INTEGER, 
        cloud_cover_oktas INTEGER,
        visibility_decameters INTEGER,
        air_temp_C FLOAT,
        dewpoint_temp_C FLOAT,
        wetbulb_temp_C FLOAT,
        station_pressure_hpa FLOAT,
        relative_humidity_percent FLOAT,
        PRIMARY KEY (unix_time, station_id) 
    )
    
    ''')

    #==============================================================================
    for year in range(startYear, endYear+1): # range function goes up to but NOT including the last value
        print("Storing weather data for %s" % (year))
        location = './raw_data/midas_wxhrly_' + str(year) + '01-' + str(year) + '12.txt' # raw data path
        
        data = pd.read_csv(location, sep=",", header=None, usecols=[0,3,4,5,9,10,14,20,35,36,37,38,98], low_memory=False, na_values=" ") # imports the text file    
        
        # Below two lines remove all data points which have not been quallity checked by MIDAS
        mask = data.iloc[:,2] == 1
        data = data[mask]
        
        # select only SYNOP data - https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/met_domain.html
        mask = data.iloc[:,1] == " SYNOP"
        data = data[mask]
        
        # remove data quality variable now that bad quality data has been removed
        data.drop(columns=[3,4], inplace=True) 
        
        data[0] = data[0].apply(timestamp2unix) # convert string dates to unix timestamps
        
        data = data.reset_index(drop=True)
        
        data.columns = ["unix_time","station_id","wind_direction","wind_speed","cloud_cover","visibility","air_temp",
                        "dewpoint_temp","wetbulb_temp","station_pressure","relative_humidity"]
        
        for row in range(len(data)):
            
            # percent_complete = int((row/len(data))*100)
            # if percent_complete % 10 == 0:                
            #     print("Percent complete for %s weather: %i" % (year, percent_complete) + "%")
                
            
            cur.execute('''INSERT OR IGNORE INTO Weather (unix_time, station_id, wind_direction_degrees, wind_speed_knots, cloud_cover_oktas, visibility_decameters, 
                                                        air_temp_C, dewpoint_temp_C, wetbulb_temp_C, station_pressure_hpa, relative_humidity_percent)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (data.loc[row,"unix_time"], data.loc[row,"station_id"], data.loc[row,"wind_direction"], data.loc[row,"wind_speed"],
                                                data.loc[row,"cloud_cover"], data.loc[row,"visibility"], data.loc[row,"air_temp"], data.loc[row,"dewpoint_temp"],
                                                data.loc[row,"wetbulb_temp"], data.loc[row,"station_pressure"], data.loc[row,"relative_humidity"])) 
        
        conn.commit()  
        
    conn.close()
        
    return None


def insolation2sql(startYear, endYear):
    conn = sqlite3.connect(databaseName)
    cur = conn.cursor()
    
    #Below code generates the table in the sqlite database if one with the same name doesn't already exist
    cur.executescript('''                          
    CREATE TABLE IF NOT EXISTS Insolation (
        unix_time INTEGER,
        station_id INTEGER,
        insolation FLOAT,
        PRIMARY KEY (unix_time, station_id) 
    )
    
    ''')
    
    for year in range(startYear, endYear+1): # range function goes up to but NOT including the last value
        print("Storing insolation data for %s" % (year))
        location = './raw_data/midas_radtob_' + str(year) + '01-' + str(year) + '12.txt' # raw data path
        
        data = pd.read_csv(location, sep=",", header=None, usecols=[2,3,4,5,6,8], low_memory=False, na_values=" ") # imports the text file  

        # remove daily readings, leave only hourly
        mask = data.iloc[:,1] == 1
        data = data[mask]
        
        # Below two lines remove all data points which have not been quallity checked by MIDAS
        mask = data.iloc[:,2] == 1
        data = data[mask]
        
        # take data only from HCM - https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/met_domain.html
        mask = data.iloc[:,3] == " HCM"
        data = data[mask]
        
        
        # remove data quality variable now that bad quality data has been removed
        data.drop(columns=[3,4,5], inplace=True) 
        
        data[2] = data[2].apply(timestamp2unix) # convert string dates to unix timestamps
        
        data = data.reset_index(drop=True)
        data.columns = ["unix_time","station_id","insolation"]
        
        for row in range(len(data)):
            
            cur.execute('''INSERT OR IGNORE INTO Insolation (unix_time, station_id, insolation) 
            VALUES (?,?,?)''', (data.loc[row,"unix_time"], data.loc[row,"station_id"], data.loc[row,"insolation"])) 
        
        conn.commit()           
        
    conn.close()       
        
    return data
        

def rainfall2sql(startYear, endYear):
    conn = sqlite3.connect(databaseName)
    cur = conn.cursor()
    
    #Below code generates the table in the sqlite database
    cur.executescript('''                          
    CREATE TABLE IF NOT EXISTS Rainfall (
        unix_time INTEGER,
        station_id INTEGER,
        rainfall_mm FLOAT,
        PRIMARY KEY (unix_time, station_id) 
    )
    
    ''')
    
    for year in range(startYear, endYear+1): # range function goes up to but NOT including the last value
        print("Storing rainfall data for %s" % (year))
        location = './raw_data/midas_rainhrly_' + str(year) + '01-' + str(year) + '12.txt' # raw data path
        
        data = pd.read_csv(location, sep=",", header=None, usecols=[0,3,4,5,6,8], low_memory=False, na_values=" ") # imports the text file   

        # remove daily readings, leave only hourly
        mask = data.iloc[:,1] == 1
        data = data[mask]
        
        # Below two lines remove all data points which have not been quallity checked by MIDAS
        mask = data.iloc[:,2] == 1
        data = data[mask]
        
        # take data only from SREW - https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/met_domain.html
        mask = data.iloc[:,3] == " SREW"
        data = data[mask]
        
        
        # remove data quality variable now that bad quality data has been removed
        data.drop(columns=[3,4,5], inplace=True) 

        data[0] = data[0].apply(timestamp2unix) # convert string dates to unix timestamps
        
        data = data.reset_index(drop=True)
        
        data.columns = ["unix_time","station_id","rainfall_mm"]
        
        for row in range(len(data)):
            
            cur.execute('''INSERT OR IGNORE INTO Rainfall (unix_time, station_id, rainfall_mm) 
            VALUES (?,?,?)''', (data.loc[row,"unix_time"], data.loc[row,"station_id"], data.loc[row,"rainfall_mm"])) 
        
        conn.commit()  
        
    conn.close()       
        
    return data


########################### USER INPUTS ######################################

## define start and end year you want to download data for
startYear = 2021
endYear = 2021


_ = rainfall2sql(startYear, endYear)
_ = insolation2sql(startYear, endYear)
_ = weather2sql(startYear, endYear)


##############################################################################
