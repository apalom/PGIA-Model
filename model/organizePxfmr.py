# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:45:25 2019

@author: Alex
"""


# Organize P XFMR
import pandas as pd
import numpy as np

path1 = 'outputData\\50_kW_1200_AggDmd\\Random EV\\4EV_0PV_12-9kW_rdm\\'

#test = np.zeros((maxTrials*24,1))

raw = pd.read_csv(path1 + 'outPxfmr_1199_4-0_rdm_raw.csv', header=None)

raw_V = raw.unstack();

trials = len(raw.columns)

df_P = pd.DataFrame(0, columns=['Hour','kW'], index=np.arange(len(raw_V)))
df_P.kW = raw_V.values

#%% Hours

idx = np.zeros((len(raw_V),1))

for t in range(24):
    idx[1200*t:1200*(t+1)] = t

#%% 

df_P.Hour = idx