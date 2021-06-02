## CEDA Weather database

This code allows you to:
- Download raw data files from the CEDA archive including; [weather](https://catalogue.ceda.ac.uk/uuid/916ac4bbc46f7685ae9a5e10451bae7c), [irradiance](https://catalogue.ceda.ac.uk/uuid/b4c028814a666a651f52f2b37a97c7c7) and [rainfall](https://catalogue.ceda.ac.uk/uuid/bbd6916225e7475514e17fdbf11141c1)
- Build an SQL database to store the raw data
- Query the weather data out in a clear and simple manner

# Prerequisites

- You have a CEDA account with access to the UK hourly weather dataset. You can apply for access [here](https://catalogue.ceda.ac.uk/uuid/916ac4bbc46f7685ae9a5e10451bae7c)

# Instructions for use

- Clone this repository into a local directory
- Setup a Python environment using the attached requirements.txt file
- Open Databases/config.py and fill in your CEDA account username and password
- Run Databases/download_midas_data.py for the chosen datatypes and time period
- Run Databases/get_midas_stations.py to create a table in your database detailing each weather station available
- Run Databases/update_database.py to load in all the raw weather data files into the database
- Use weather_query_frontend.py to query data from your local database
