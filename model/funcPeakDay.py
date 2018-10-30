# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 19:53:21 2018

@author: Alex
"""

def funcPeakDay(day, dfHome, dfSolar):
    
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
    
    return (day, dfHomeDay, dfSolarDay)

