# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 19:53:21 2018

@author: Alex

Filter home load and solar generation data to 
only the user-defined peak-day.
"""

def funcPeakDay(day, dfHome, dfSolar, dfAmbient):
    
    #import library
    from datetime import datetime
    
    try:
        dfHome['DATE'] = dfHome['DATE'].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'));
        dfHomeDay = dfHome.loc[dfHome['DATE'] == day]
    except AttributeError:
        print(' AttributeError')
        dfHomeDay = dfHome.loc[dfHome['DATE'] == day]
    
    dfHomeDay = dfHomeDay.reset_index(drop=True)
    dfHomeDay = dfHomeDay.drop(columns=['DATE', 'Hour'])
        
    try:
        dfSolar['Date'] = dfSolar['Date'].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'));
        dfSolarDay = dfSolar.loc[dfSolar['Date'] == day]
    except AttributeError:
        print(' AttributeError')
        dfSolarDay = dfSolar.loc[dfSolar['Date'] == day]
        
    dfSolarDay = dfSolarDay.reset_index(drop=True)
    dfSolarDay = dfSolarDay.drop(columns=['Year', 'Month', 'Day'])
        
    try:
        dfAmbient['DATE'] = dfAmbient['DATE'].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'));
        dfAmbientDay = dfAmbient.loc[dfAmbient['DATE'] == day]
    except AttributeError:
        print(' AttributeError')
        dfAmbientDay = dfAmbient.loc[dfAmbient['DATE'] == day]
    
    dfAmbientDay = dfAmbientDay.reset_index(drop=True)
    dfAmbientDay = dfAmbientDay.drop(columns=['DATE', 'Hour'])
    
    return (day, dfHomeDay, dfSolarDay, dfAmbientDay)

