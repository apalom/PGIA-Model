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

for file in files:
    
    data[yr] = pd.read_csv(file)
    yr += 1;
    
#%% Parse Date

#colNames = ['Year', 'Month', 'Day', 'Date', 'Hour', 'Minute', 'GHI', 'Temperature']
tempCol = list(np.arange(2008,2018,1));

col = []

for year in tempCol:
    x = ('yr'+ str(year))
    col.append(x)
#tempCol = 'yr'*10 + list(np.arange(2008,2018,1))

  
tempDayData = pd.DataFrame(0, index=np.arange(24), columns=col)

#yr = 2007;
month = 7;
day = 1;
i = 0;

for key, yrData in data.items():
    j = 'yr'+str(key)
    print(j)
    tempData = yrData.loc[yrData.Month == month]
    tempData = tempData.loc[tempData.Day == day]
    
    tempDayData[col[i]] = tempData.Temperature.values
    i += 1;

#%%     
    
dfGHI = pd.read_excel('data\\NSRDB\\10yrGHI.xlsx')
dfCelcius = pd.read_excel('data\\NSRDB\\10yrTemp.xlsx')
dfFarenheit = dfCelcius.apply(lambda x: x*(9/5) + 32)

