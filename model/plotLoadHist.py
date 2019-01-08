# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 09:21:36 2018

@author: Alex
"""

import matplotlib.pyplot as plt

hr = 19

bin_edges = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
n, bins, patches = plt.hist(dfHomeDay.iloc[hr,:], bins=bin_edges, density=True, rwidth=0.9, color='lightgray')

font = {'family' : 'Times New Roman',
        'weight' : 'ultralight',
        'size'   : 10.0}
plt.rc('font', **font)
                            
plt.rcParams["figure.figsize"] = [8,6]
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Loading (kW)')
plt.xlim([0,14])
plt.ylabel('Frequency')
#plt.title('Loading Histogram (19:00)')
kdeLine = dfHomeDay.iloc[hr,:].plot.kde(color='black')

print(plt.rcParams)

#%%

dfHomeDay.iloc[hr,:].plot.kde()

#%%

from scipy import stats as st
import numpy as np

hr = 19

sampleKDE_kW = dfHomeDay.iloc[hr]
my_kde = st.gaussian_kde(sampleKDE_kW)
sampleKDE_kW = my_kde.resample(numHomes)