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

path1 = 'data\\Scenario8\\'
file = '\\outPxfmr_299.csv'

# Plot F_aa Comparison
base = pd.read_csv(path1 + 'Case_Base' + file, header=None)
caseA = pd.read_csv(path1 + 'CaseA' + file, header=None)
caseB = pd.read_csv(path1 + 'CaseB' + file, header=None)
caseC = pd.read_csv(path1 + 'CaseC' + file, header=None)

#%%

data = pd.DataFrame({'Base': base.quantile(0.50, axis=1), 'CaseA': caseA.quantile(0.50, axis=1),
                   'CaseB': caseB.quantile(0.50, axis=1), 'CaseC': caseC.quantile(0.50, axis=1)}) 


#%%

font = {'family' : 'Times New Roman',
        'size'   : 18}
plt.rc('font', **font)
                            
plt.rcParams["figure.figsize"] = [8,6]

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

#test = np.zeros((maxTrials*24,1))

# Plot F_aa Comparison
ampsL1 = pd.read_csv(path1 + 'outL1amp_299.csv', header=None)
ampsL3 = pd.read_csv(path1 + 'outL3amp_299.csv', header=None)
ampsL7 = pd.read_csv(path1 + 'outL7amp_299.csv', header=None)


#%%

ampsL1 = ampsL1.loc[ampsL1[:][0] > 0]
ampsL1 = ampsL1.reset_index()
ampsL1 = ampsL1.drop(labels='index', axis=1)

#%%

data = pd.DataFrame({'L1 - Min': ampsL1.quantile(0.0, axis=1), 'L1 - Mean': ampsL1.quantile(0.50, axis=1), 'L1 - Max': ampsL1.quantile(1.0, axis=1), 
                     'L3 - Min': ampsL3.quantile(0.0, axis=1), 'L3 - Mean': ampsL3.quantile(0.50, axis=1), 'L3 - Max': ampsL3.quantile(1.0, axis=1), 
                     'L7 - Min': ampsL1.quantile(0.0, axis=1), 'L7 - Mean': ampsL7.quantile(0.50, axis=1), 'L7 - Max': ampsL7.quantile(1.0, axis=1)}) 

#%% 

ampsL1_V = ampsL1.unstack();
ampsL3_V = ampsL3.unstack();
ampsL7_V = ampsL7.unstack();

data = pd.DataFrame({'L1': ampsL1_V.values, 
                     'L3': ampsL3_V.values,
                     'L7': ampsL7_V.values})


#%%

new = np.zeros((data.shape[0]*data.shape[1], 2))

tempDf = pd.DataFrame(new, columns = ['Current','Case']);

colNum = 0

for column in data:
    tempCol = data[column].values;
    tempLabel = column;

    stRow = colNum*len(data);
    enRow = colNum*len(data) + len(data);
    print(stRow, enRow, colNum)
    tempDf.Current.iloc[stRow:enRow] = tempCol;
    tempDf.Case.iloc[stRow:enRow] = tempLabel;
    colNum += 1;
    
data1 = tempDf;

#%% Plot Violin Plot 

import seaborn as sns

sns.set(style="whitegrid")
ax = sns.violinplot(x='Case', y='Current', data=data1, palette='Greys')

cases = list(data)

plt.xlabel('Line')
plt.ylabel('Line Current (Amps)')
plt.title('Base Case (0EV)')

#%%

# And plot it        
plot1 = data.plot()
                              
plt.ylabel('Average Line Current (A)')
#plt.ylim(0, 75)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Hour (hr)')
plt.xlim(0, 24)
plt.xticks(np.arange(0,24,2))
plt.title('Line Loading (8EV)')
plt.legend(loc=(1.01,0.25))
plt.show()



#%% Transformer

path1 = 'data\\Scenario8\\'
file = '\\outPxfmr_299.csv'

# Plot F_aa Comparison
base = pd.read_csv(path1 + 'Case_Base' + file, header=None)
caseA = pd.read_csv(path1 + 'CaseA' + file, header=None)
caseB = pd.read_csv(path1 + 'CaseB' + file, header=None)
caseC = pd.read_csv(path1 + 'CaseC' + file, header=None)
