# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:13:54 2021

- This script downloads various weather data from the CEDA archive, then uses it to update the existing weather SQL database.

- weather data description: https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/WH_Table.html
- Irradiance data description: https://artefacts.ceda.ac.uk/badc_datadocs/ukmo-midas/RO_Table.html



@author: maxbi
"""
import ftplib
import os
from config import config

def downloadCedaData(start_year, end_year, dataNames=["insolation","weather","rainfall"]):
    
    username = config().username
    password = config().password
    
    fileInfoDict = {"weather": {"filepath": '/badc/ukmo-midas/data/WH/yearly_files/',
                                "filePrefix": 'midas_wxhrly_'},
                    "insolation": {"filepath": '/badc/ukmo-midas/data/RO/yearly_files/',
                                "filePrefix": 'midas_radtob_'},
                    "rainfall": {"filepath": '/badc/ukmo-midas/data/RH/yearly_files/',
                                "filePrefix": 'midas_rainhrly_'}
                    }
    
    # login to FTP with username and password
    f=ftplib.FTP("ftp.ceda.ac.uk", username, password)

    # If directory doesn't exist make it
    if not os.path.isdir('./raw_data/'):
        os.mkdir('./raw_data/')
    
    for dataName in dataNames: # iterate over each datatype

        # loop through years
        for year in range(start_year, end_year+1):
        
            # change the remote directory
            f.cwd(fileInfoDict[dataName]["filepath"])
            # define filename
            filename = fileInfoDict[dataName]["filePrefix"] + str(year) + '01-' + str(year) + '12.txt'
            # get the remote file to the local directory
            print('Downloading ' + dataName + ' for year ' + str(year))
            f.retrbinary("RETR %s" % filename, open("./raw_data/" + filename, "wb").write)
            
        
    # Close FTP connection
    f.close()
    
    return None

######################### USER INPUTS #######################################
## define start and end year you want to download data for
startYear = 2021 # got from 2000-2007 inclusive for weather
endYear = 2021


downloadCedaData(startYear, endYear, dataNames=["rainfall","insolation","weather"])

#############################################################################

