# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 19:53:21 2018

@author: Alex

Filter home load and solar generation data to 
only the user-defined peak-day.
"""

def funcPeakDay(day, dfHome, dfNSRDB):
    
    #import library
    from datetime import datetime
    import pandas as pd
    import numpy as np
    
    #import residential load data
    try:
        dfHome['DATE'] = dfHome['DATE'].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'));
        dfHomeDay = dfHome.loc[dfHome['DATE'] == day]
    except AttributeError:
        #print(' AttributeError')
        dfHomeDay = dfHome.loc[dfHome['DATE'] == day]
    
    dfHomeDay = dfHomeDay.reset_index(drop=True)
    dfHomeDay = dfHomeDay.drop(columns=['DATE', 'Hour'])
    
    #import NSRDB
    yr = 2008;
    tempCol = list(np.arange(2008,2018,1));
    
    col = []
    
    for year in tempCol:
        x = ('yr'+ str(year))
        col.append(x)
    
    #farenheit (F)
    dfTempDay = pd.DataFrame(0, index=np.arange(24), columns=col)
    #global horizontal irradiance (GHI)
    dfGHIDay = pd.DataFrame(0, index=np.arange(24), columns=col)    
        
    m = int(day[6:7]);
    d = int(day[9:10]);
    
    for yr, yrData in dfNSRDB.items():
        tempData = yrData.loc[yrData.Month == m]
        tempData = tempData.loc[tempData.Day == d]
        
        col = 'yr'+ str(yr)
        #print(col)
        dfTempDay[col] = tempData.Temperature.values
        dfGHIDay[col] = tempData.GHI.values
    
#    try:
#        dfSolar['Date'] = dfSolar['Date'].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'));
#        dfSolarDay = dfSolar.loc[dfSolar['Date'] == day]
#    except AttributeError:
#        print(' AttributeError')
#        dfSolarDay = dfSolar.loc[dfSolar['Date'] == day]
#        
#    dfSolarDay = dfSolarDay.reset_index(drop=True)
#    dfSolarDay = dfSolarDay.drop(columns=['Year', 'Month', 'Day'])
#        
#    try:
#        dfAmbient['DATE'] = dfAmbient['DATE'].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'));
#        dfAmbientDay = dfAmbient.loc[dfAmbient['DATE'] == day]
#    except AttributeError:
#        print(' AttributeError')
#        dfAmbientDay = dfAmbient.loc[dfAmbient['DATE'] == day]
#    
#    dfAmbientDay = dfAmbientDay.reset_index(drop=True)
#    dfAmbientDay = dfAmbientDay.drop(columns=['DATE', 'Hour'])
    
    return (day, dfHomeDay, dfTempDay, dfGHIDay)

