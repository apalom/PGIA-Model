# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 09:37:05 2018

@author: Alex
"""

import numpy as np
from scipy.stats import mstats
import matplotlib.pyplot as plt
import pandas as pd
from os import path


#%% Plot System Data

path1 = 'data\\Scenario4\\'
file = '\\outPxfmr_299.csv'

# Plot F_aa Comparison
base = pd.read_csv(path1 + 'Case_Base' + file, header=None)
caseA = pd.read_csv(path1 + 'CaseA1' + file, header=None)
caseB = pd.read_csv(path1 + 'CaseB1' + file, header=None)
caseC = pd.read_csv(path1 + 'CaseC1' + file, header=None)

#%%

data = pd.DataFrame({'Base': base.quantile(0.50, axis=1), 'CaseA': caseA.quantile(0.50, axis=1),
                   'CaseB': caseB.quantile(0.50, axis=1), 'CaseC': caseC.quantile(0.50, axis=1)}) 

#%%

hr = np.arange(0,24,1)

# And plot it        
plot1 = data.plot()
                              
plt.ylabel('Average Loading (kW)')
plt.ylim(0, 80)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Hour (hr)')
plt.xlim(0, 24)
plt.xticks(np.arange(0,24,2))
plt.title('Transformer Loading (4EV)')
plt.legend(loc=(0.04,0.65))
plt.show()

#%% Plot Line Currents

path1 = 'data\\Scenario4\\Case_Base\\'

# Plot F_aa Comparison
ampsL1 = pd.read_csv(path1 + 'outL1amp_299.csv', header=None)
ampsL3 = pd.read_csv(path1 + 'outL3amp_299.csv', header=None)
ampsL7 = pd.read_csv(path1 + 'outL7amp_299.csv', header=None)


#%%

data = pd.DataFrame({'L1': ampsL1.quantile(0.50, axis=1), 'L3': ampsL3.quantile(0.50, axis=1),
                   'L7': ampsL7.quantile(0.50, axis=1)}) 

# And plot it        
plot1 = data.plot()
                              
plt.ylabel('Average Line Current (A)')
plt.ylim(0, 75)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Hour (hr)')
plt.xlim(0, 24)
plt.xticks(np.arange(0,24,2))
plt.title('Line Loading (4EV)')
plt.legend(loc=(0.04,0.65))
plt.show()