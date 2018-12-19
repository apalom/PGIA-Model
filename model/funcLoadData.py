# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 17:05:32 2018

@author: Alex
"""

def funcLoadData():

    # import libraries
    import pandas as pd
    import numpy as np
    import timeit
    
    #---- Import Case ----#
    timeLoadCase = timeit.default_timer()
    
    #dfSys0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\case12.xlsx', sheet_name=None, header=0)
    #dfSys0 = pd.read_excel(r'C:\Users\Alex Palomino\Documents\GitHub\PGIA-Model\model\data\case12.xlsx', sheet_name=None, header=0)
    dfSys0 = pd.read_excel('data\\case12.xlsx', sheet_name=None, header=0)
    dfSys = dfSys0;
    
    elapsedLoadCase = timeit.default_timer() - timeLoadCase
    print('Load Case time: {0:.4f} sec'.format(elapsedLoadCase))
    
    #---- Import RMP Load ----#
    timeLoadRMP = timeit.default_timer()
    
    #dfHome0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\2015_Residential_Load Profile_v1_WestmartEV_RAW.xlsx', header=0);
    dfHome0 = pd.read_excel('data\\2015_Residential_Load Profile_v1_WestmartEV_RAW.xlsx', header=0);
    dfHome = dfHome0;
    
    elapsedLoadRMP = timeit.default_timer() - timeLoadRMP
    print('Load RMP time: {0:.4f} sec'.format(elapsedLoadRMP))
    
    #---- Import EVs Connected ----#
    timeLoadEV = timeit.default_timer()
    
    #dfEV0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\All_EVProject2013Qtly_Residential_Hr.xlsx', header=0);
    dfEV0 = pd.read_excel('data\\All_EVProject2013Qtly_Residential_Hr.xlsx', header=0);
    dfEV = dfEV0;
    
    elapsedLoadEV = timeit.default_timer() - timeLoadEV
    print('Load EV time: {0:.4f} sec'.format(elapsedLoadEV))

    #---- Import NSRDB Data ----#
    timeLoadSolar= timeit.default_timer()

    import glob
        
    files = glob.glob("data/NSRDB/158327*.csv")
    
    dfNSRDB = {}
    yr = 2008;
    
    tempCol = list(np.arange(2008,2018,1));    
    col = []    
    for year in tempCol:
        x = ('yr'+ str(year))
        col.append(x)

    for file in files:
        
        dfNSRDB[yr] = pd.read_csv(file)
        # -- Need Celcius temps for Transformer Aging -- #
        #dfNSRDB[yr].Temperature = dfNSRDB[yr].Temperature.apply(lambda x: x*(9/5) + 32)
    
        yr += 1;

    elapsedLoadSolar = timeit.default_timer() - timeLoadSolar
    print('Load NSRDB time: {0:.4f} sec'.format(elapsedLoadSolar))

#    #---- Import Solar NSRDB Data ----#
#    timeLoadSolar= timeit.default_timer()
#    
#    #dfSolar0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\NSRDB_158327_2016.xlsx', header=0);
#    dfSolar0 = pd.read_excel('data\\NSRDB_158327_2016.xlsx', header=0);
#    dfSolar = dfSolar0;
#    
#    elapsedLoadSolar = timeit.default_timer() - timeLoadSolar
#    print('Load Solar time: {0:.4f} sec'.format(elapsedLoadSolar))
#
#    #---- Import Ambient Temp Data ----#
#    timeLoadAmbient= timeit.default_timer()
#
#    #dfAmbient0 = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\NOAA_SLC_2016_season.xlsx');
#    dfAmbient0 = pd.read_excel('data\\NOAA_SLC_2016_season.xlsx');
#    dfAmbient = dfAmbient0;
#    
#    elapsedLoadAmbient = timeit.default_timer() - timeLoadAmbient
#    print('Load Ambient Temp time: {0:.4f} sec'.format(elapsedLoadAmbient))

    return (dfSys, dfHome, dfEV, dfNSRDB)



