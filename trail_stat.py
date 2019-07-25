import requests
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import date, timedelta
import NOAA_Historical_weather as noaa
from sklearn.externals import joblib


def trail_stat(trailname, userdate):
    
    
    # NOAA model parameters
    #mytoken = 'JNYovzhikMxTKdSuBEYotIIoYaHzJPLd' #foad.yousef
    mytoken = 'yGsCbTQIJINcnYiOacAffeqDJupZIlWH' #foad1359
    stationid = 'GHCND:USC00270690'
    datasetid = 'GHCND'
    
    # Julain Date
    d = dt.today().date()
    jday = d.timetuple()
    jday = jday.tm_yday
    
    # Date for NOAA
    print('##################################')
    print('User date = ',userdate)
    date = dt.strptime(userdate, '%Y-%m-%d')
    date = date - timedelta(days=5)
    date = str(date.date())
    print('##################################')
    print('My date = ',date)

    #print(date)

    
    # Make a call to NOAA
    wd = noaa.get_weather(stationid, datasetid, date, date, mytoken)
    print('wd =====', wd)
    
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

        print('%%%%%%%%%%')
        print(PREC)
        print(TMAX)
        print(TMIN)
        print(SNOW)
        print(jday)
        print('%%%%%%%%%%')


        
        # Populate the Numbers (check this one)
        data = [jday,PREC,TMAX,TMIN,SNOW]
        X = np.asarray(data)
        # Reshape the data
        X = X.reshape(1, -1)
        # Load the RF model:

        # ADM = joblib.load('ADM2_RF.sav')
        # WSH = joblib.load('WSH2_RF.sav')
        # MAD = joblib.load('MAD2_RF.sav')
        # MON = joblib.load('MON2_RF.sav')
        # EIS = joblib.load('EIS2_RF.sav')
        # LAF = joblib.load('LAF2_RF.sav')
        # JEF = joblib.load('JEF2_RF.sav')
        # CAR = joblib.load('CAR2_RF.sav')
        # MOS = joblib.load('MOS2_RF.sav')
        #CAC = joblib.load('CAC2_RF.sav')
        # WIL = joblib.load('WIL2_RF.sav')
        # CAB = joblib.load('CAB2_RF.sav')
        # MOR = joblib.load('MOR2_RF.sav')

        print('%%%%%%%%')
        print(stationid)
        print('%%%%%%%%')
        


        if trailname =='ADM':
            ADM = joblib.load('ADM2_RF.sav')
            print('fitting the model for ADM')
            p = ADM.predict(X)
        if trailname == 'WSH':
            WSH = joblib.load('WSH2_RF.sav')
            print('fitting the model for WSH')
            p = WSH.predict(X)
        if trailname =='MAD':
            MAD = joblib.load('MAD2_RF.sav')
            print('fitting the model for MAD')
            p = MAD.predict(X)
        if trailname =='MON':
            MON = joblib.load('MON2_RF.sav')
            print('fitting the model for MON')
            p = MON.predict(X)
        if trailname =='EIS':
            EIS = joblib.load('EIS2_RF.sav')
            print('fitting the model for EIS')
            p = EIS.predict(X)
        if trailname =='LAF':
            LAF = joblib.load('LAF2_RF.sav')
            print('fitting the model for LAF')
            p = LAF.predict(X)
        if trailname =='CAR':
            CAR = joblib.load('CAR2_RF.sav')
            print('fitting the model for CAR')
            p = CAR.predict(X)
        #if trailname =='CAC':
        #    print('fitting the model for CAC')
        #    p = CAC.predict(X)
        if trailname =='JEF':
            JEF = joblib.load('JEF2_RF.sav')
            print('fitting the model for JEF')
            p = JEF.predict(X)
        if trailname =='MOS':
            MOS = joblib.load('MOS2_RF.sav')
            print('fitting the model for MOS')
            p = MOS.predict(X)
        if trailname =='WIL':
            WIL = joblib.load('WIL2_RF.sav')
            print('fitting the model for WIL')
            p = WIL.predict(X)
        if trailname =='CAB':
            CAB = joblib.load('CAB2_RF.sav')
            print('fitting the model for CAB')
            p = CAB.predict(X)
        if trailname =='MOR':
            MOR = joblib.load('MOR2_RF.sav')
            print('fitting the model for MOR')
            p = MOR.predict(X)
        # Publish the model prediction
        print(p[0])
        return p
    
    except:
        print('Weather data might not be available!')
    
    
