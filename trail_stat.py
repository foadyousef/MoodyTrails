import requests
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import date, timedelta
import NOAA_Historical_weather as noaa
from sklearn.externals import joblib


def trail_stat(trailname, userdate):
    
    
    # NOAA model parameters
    mytoken = 'JNYovzhikMxTKdSuBEYotIIoYaHzJPLd'
    stationid = 'GHCND:USC00270690'
    datasetid = 'GHCND'
    
    # Julain Date
    d = dt.today().date()
    jday = d.timetuple()
    jday = jday.tm_yday
    
    # Date for NOAA
    print('##################################')
    print(userdate)
    date = dt.strptime(userdate, '%Y-%m-%d')
    date = date - timedelta(days=3)
    date = str(date.date())
    #print(date)

    
    # Make a call to NOAA
    wd = noaa.get_weather(stationid, datasetid, date, date, mytoken)
    
    
    # Make a dataframe from observations:
    try: 
        PREC = 0
        TMAX = 0
        TMIN = 0
        SNOW = 0
        PREC = wd['value'][wd['datatype']=='PRCP'].values[0]
        SNOW = wd['value'][wd['datatype']=='SNOW'].values[0]
        TMAX = wd['value'][wd['datatype']=='TMAX'].values[0]
        TMIN = wd['value'][wd['datatype']=='TMIN'].values[0]
        
        # Populate the Numbers (check this one)
        data = [jday,PREC,TMAX,TMIN,SNOW]
        X = np.asarray(data)
        # Reshape the data
        X = X.reshape(1, -1)
        # Load the RF model:
        ADM = joblib.load('adams_RF.sav')
        WSH = joblib.load('adams_RF.sav')
        # Feed the numbers into the model
        
        if trailname =='ADM':
            print('fitting the model for ADM')
            p = ADM.predict(X)
        if trailname == 'WSH':
            print('fitting the model for WSH')
            p = WSH.predict(X)
        # Publish the model prediction
        print(p[0])
        if p[0] == 0:
            stat = 'Trail is not in ideal condition!'
            return stat
        else:
            stat = 'Trail condition is ideal for hiking!'
            return stat
    
    except:
        print('Weather data might not be available!')
    
    
