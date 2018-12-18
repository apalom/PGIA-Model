# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 18:20:47 2018

@author: Alex Palomino
"""

#%% Load Temp/Solar Data

import pandas as pd
import numpy as np
import glob


files = glob.glob("data/NSRDB/158327*.csv")

data = {}
yr = 2008;

tempCol = list(np.arange(2008,2018,1));

col = []

for year in tempCol:
    x = ('yr'+ str(year))
    col.append(x)

dfTemp = pd.DataFrame(0, index=np.arange(24), columns=col)
dfGHI = pd.DataFrame(0, index=np.arange(24), columns=col)

for file in files:
    
    data[yr] = pd.read_csv(file)
    data[yr].Temperature = data[yr].Temperature.apply(lambda x: x*(9/5) + 32)

    yr += 1;

#%%

yr = 2008;
tempCol = list(np.arange(2008,2018,1));

col = []

for year in tempCol:
    x = ('yr'+ str(year))
    col.append(x)

dfTempDay = pd.DataFrame(0, index=np.arange(24), columns=col)
dfGHIDay = pd.DataFrame(0, index=np.arange(24), columns=col)    

day = '2015-07-01';

m = int(day[6:7]);
d = int(day[9:10]);

for key, yrData in data.items():
    j = 'yr'+str(key)
    print(j)
    tempData = yrData.loc[yrData.Month == m]
    tempData = tempData.loc[tempData.Day == d]
    
    col = 'yr'+ str(yr)
    dfTempDay[col] = tempData.Temperature.values
    dfGHIDay[col] = tempData.GHI.values
    
    yr += 1;

#%%

from scipy import stats as st
import numpy as np

sampleKDE_F = dfTempDay.iloc[0]
my_kde = st.gaussian_kde(sampleKDE_F)
sampleKDE_F = my_kde.resample(1)[0][0]


#    
##%% Parse Date
#
#tempDayData = pd.DataFrame(0, index=np.arange(24), columns=col)
#
##yr = 2007;
#month = 7;
#day = 1;
#i = 0;
#
#for key, yrData in data.items():
#    j = 'yr'+str(key)
#    print(j)
#    tempData = yrData.loc[yrData.Month == month]
#    tempData = tempData.loc[tempData.Day == day]
#    
#    tempDayData[col[i]] = tempData.Temperature.values
#    i += 1;
#
##%%     
#    
#dfGHI = pd.read_excel('data\\NSRDB\\10yrGHI.xlsx')
#dfCelcius = pd.read_excel('data\\NSRDB\\10yrTemp.xlsx')
#dfFarenheit = dfCelcius.apply(lambda x: x*(9/5) + 32)
#
