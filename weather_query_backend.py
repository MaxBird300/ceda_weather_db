# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 12:50:03 2020

@author: maxbi
"""
import pandas as pd
import sqlite3
import numpy as np
import datetime
from math import cos, sin, atan2, sqrt, radians


def timestamp2unix(strTime): # calcualtes unix time (number of seconds since 1970) from string time
    time_count = datetime.datetime.strptime('1970-01-01 00:00', '%Y-%m-%d %H:%M')
    unix_time = int((datetime.datetime.strptime(strTime, '%d/%m/%Y')-time_count).total_seconds())

    return unix_time


# used for calculating distances between lon/lat points
def haversine(coord1: object, coord2: object):

    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = radians(lat1)
    phi_2 = radians(lat2)

    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)

    a = sin(delta_phi / 2.0) ** 2 + cos(phi_1) * \
        cos(phi_2) * sin(delta_lambda / 2.0) ** 2

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers

    km = round(km, 3)
    return km


class weatherDatabase():
    
    def __init__(self, lat_q, lon_q, radius):
        self.dbPath = './Databases/Weather_DB.sqlite'
        self.latQ = lat_q
        self.lonQ = lon_q
        self.radius = radius
        self.midasStations = self.midasStationInfo()
        
        

    def midasStationInfo(self): # output dataframe of midas station information
    
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM MIDAS_stations''')
        MIDAS_station_data = pd.DataFrame(cur.fetchall(), 
                                          columns = ["station_id","name","start_date","end_date","latitude","longitude","postcode","weather_collected","insolation_collected","rainfall_collected"])
    
        distances = []
        coords_query = [self.latQ, self.lonQ]
        for entry in range(len(MIDAS_station_data)):
    
            coords_station = [MIDAS_station_data['latitude'][entry], MIDAS_station_data['longitude'][entry]]
            # calls haversine function to calculate distance
            dist = haversine(coords_query, coords_station)
            distances.append(dist)
            
        MIDAS_station_data['Distance from query (km)'] = distances # create column to store distance from query of all midas stations
    
        # sorts df into ascending order based on distance from query
        MIDAS_ascending = MIDAS_station_data.sort_values(by=['Distance from query (km)'], ignore_index = True)
        
        ## below loop removes any stations which are outside of the radius specified by the user
        for entry in range(len(MIDAS_ascending)):
            if  MIDAS_ascending['Distance from query (km)'][entry] <= self.radius:
                pass
            else:
                drop_indexes = range(entry, len(MIDAS_ascending))
                MIDAS_in_radius = MIDAS_ascending.drop(labels = drop_indexes)
                break   
    
        return MIDAS_in_radius 


    def getRainfallData(self, strStart, strEnd, station):
        
        unixStart = timestamp2unix(strStart)
        unixEnd = timestamp2unix(strEnd)
        
        # filter out stations which dont have rainfall data
        mask = self.midasStations["rainfall_collected"] == True
        rainStations = self.midasStations[mask]
        rainStations.reset_index(inplace=True, drop=True)
        
        # return rainStations
        print("Pulling data from station %i" % int(rainStations.loc[station,"station_id"]))
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Rainfall WHERE station_id = ? AND unix_time > ? AND unix_time <= ?''', (int(rainStations.loc[station,"station_id"]), unixStart, unixEnd))
        stationData = pd.DataFrame(cur.fetchall(), columns = ["unix_time","station_id","rainfall_mm"])
        
        stationData.insert(loc=0, column="Timestamp", value = pd.to_datetime(stationData["unix_time"], unit="s"))
        stationData.drop(columns="unix_time", inplace=True)
        
        return stationData, rainStations
    
    def getWeatherData(self, strStart, strEnd, station):
        
        unixStart = timestamp2unix(strStart)
        unixEnd = timestamp2unix(strEnd)
        
        # filter out stations which dont have rainfall data
        mask = self.midasStations["weather_collected"] == True
        weatherStations = self.midasStations[mask]
        weatherStations.reset_index(inplace=True, drop=True)
        
        # return rainStations
        print("Pulling data from station %i" % int(weatherStations.loc[station,"station_id"]))
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Weather WHERE station_id = ? AND unix_time > ? AND unix_time <= ?''', (int(weatherStations.loc[station,"station_id"]), unixStart, unixEnd))
        stationData = pd.DataFrame(cur.fetchall(), columns = ["unix_time","station_id","wind_direction","wind_speed","cloud_cover","visibility",
                                                              "air_temp", "dewpoint_temp","wetbulb_temp","station_pressure","relative_humidity"])
        
        stationData.insert(loc=0, column="Timestamp", value = pd.to_datetime(stationData["unix_time"], unit="s"))
        stationData.drop(columns="unix_time", inplace=True)
        
        return stationData, weatherStations       
    
    def getInsolationData(self, strStart, strEnd, station):
        
        unixStart = timestamp2unix(strStart)
        unixEnd = timestamp2unix(strEnd)
        
        # filter out stations which dont have rainfall data
        mask = self.midasStations["insolation_collected"] == True
        insolationStations = self.midasStations[mask]
        insolationStations.reset_index(inplace=True, drop=True)
    
        
        # return rainStations
        print("Pulling data from station %i" % int(insolationStations.loc[station,"station_id"]))
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Insolation WHERE station_id = ? AND unix_time > ? AND unix_time <= ?''', (int(insolationStations.loc[station,"station_id"]), unixStart, unixEnd))
        stationData = pd.DataFrame(cur.fetchall(), columns = ["unix_time","station_id","insolation"])
        
        stationData.insert(loc=0, column="Timestamp", value = pd.to_datetime(stationData["unix_time"], unit="s"))
        stationData.drop(columns="unix_time", inplace=True)
        
        return stationData, insolationStations      
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


