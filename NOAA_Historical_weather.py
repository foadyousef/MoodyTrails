
# So this app will work on the NOAA API to extract weather data from the web.
# 
# The part that you need to pay attention to is whether you are working with a `location` or a `station`. Look under cell 4 for more details. 


import requests
import datetime
import numpy as np
import pandas as pd


# ### Process:
# 
# 1. If you want weather data for a specific place, first find the nearest station for it using this [link](https://www.ncdc.noaa.gov/cdo-web/datatools/findstation). Click on the tower icon ad write down the ID.
# 
# 2. Use the references [here](https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted) to generate a meaningful URL to be used by the NOAA API. Look inside the tabs on the top of the page to read about specific types of data in ways to call the data. 
# 
# 3. [This](https://gettecr.github.io/noaa-api.html#.XQJISiYpDCK) blogpost was very useful. 




#mytoken = 'JNYovzhikMxTKdSuBEYotIIoYaHzJPLd'

#begin_date = '2018-06-13'
#end_date = '2018-06-18'

#Location key for the region you are interested in (can be found on NOAA or requested as a different API as well)

#stationid = 'GHCND:USC00270690' #A station New Hampshire
#datasetid = 'GHCND' #datset id for "Daily Summaries"

#base_url_data = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
#base_url_stations = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'



# the weather function
def get_weather(stationid, datasetid, begin_date, end_date, mytoken):
    #mytoken = 'JNYovzhikMxTKdSuBEYotIIoYaHzJPLd'
    #stationid = 'GHCND:USC00270690' 
    #datasetid = 'GHCND' #datset id for "Daily Summaries"
    token = {'token': mytoken}
    #print(token)

    #passing as string instead of dict because NOAA API does not like percent encoding
    params = 'datasetid='+str(datasetid)+'&stationid='+str(stationid)+'&units=metric'+'&startdate='+str(begin_date)+'&enddate='+str(end_date)
                     
    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?'
    params
    #print(base_url)
    #print(params)
    r = requests.get(base_url, params, headers=token)
    print("Request status code: "+str(r.status_code))


    try:
        #results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_records(r.json()['results'])
        print("Successfully retrieved "+str(len(df['station'].unique()))+" stations")
        dates = pd.to_datetime(df['date'])
        print("Last date retrieved: "+str(dates.iloc[-1]))

        if df.count().max()==1000:
            print('WARNING: Maximum data limit was reached (limit = 1000)')
            print('Consider breaking your request into smaller pieces')
            
        return df

    #Catch all exceptions for a bad request or missing data
    except:
        print("Error converting weather data to dataframe. Missing data?")
 
get_weather


