# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 19:53:21 2018

@author: Alex
"""

def funcPeakDay(day, dfHome):
    
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
        
    return (day, dfHomeDay)

