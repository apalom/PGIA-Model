# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 17:05:32 2018

@author: Alex
"""

def funcLoadData():

    # import libraries
    import pandas as pd
    import timeit
    
    #---- Import Case ----#
    timeLoadCase = timeit.default_timer()
    
    dfSys0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\case12.xlsx', sheet_name=None, header=0)
    dfSys = dfSys0;
    
    elapsedLoadCase = timeit.default_timer() - timeLoadCase
    print('Load Case time: {0:.4f} sec'.format(elapsedLoadCase))
    
    #---- Import RMP Load ----#
    timeLoadRMP = timeit.default_timer()
    
    dfHome0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\2015_Residential_Load Profile_v1_WestmartEV_RAW.xlsx', header=0)
    dfHome = dfHome0;
    
    elapsedLoadRMP = timeit.default_timer() - timeLoadRMP
    print('Load RMP time: {0:.4f} sec'.format(elapsedLoadRMP))
    
    #---- Import EVs Connected ----#
    timeLoadEV = timeit.default_timer()
    
    dfEV0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\All_EVProject2013Qtly_Residential_Hr.xlsx', header=0)
    dfEV = dfEV0;
    
    elapsedLoadEV = timeit.default_timer() - timeLoadEV
    print('Load EV time: {0:.4f} sec'.format(elapsedLoadEV))

    #---- Import Solar NSRDB Data ----#
    timeLoadSolar= timeit.default_timer()
    
    dfSolar0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\NSRDB_158327_2016.xlsx', header=0)
    dfSolar = dfSolar0;
    
    elapsedLoadSolar = timeit.default_timer() - timeLoadSolar
    print('Load Solar time: {0:.4f} sec'.format(elapsedLoadSolar))

    return (dfSys, dfHome, dfEV, dfSolar)