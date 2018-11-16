# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:34:58 2018

@author: Alex
"""

import numpy as np
from scipy.stats import mstats
import matplotlib.pyplot as plt
import pandas as pd


#data = pd.read_csv(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\CaseA\outPxfmr_299.csv', header=None)
                 
path1 = 'data\\Scenario4\\'
file = '\\outFaa_299.csv'

# Plot F_aa Comparison
base = pd.read_csv(path1 + 'Case_Base' + file, header=None)
caseA = pd.read_csv(path1 + 'CaseA1' + file, header=None)

#%%

# Create data
#data = pd.DataFrame(CaseA)

hr = np.arange(0,24,1)

# Calculate all the desired values
dfbase = pd.DataFrame({'95%': base.quantile(0.95, axis=1), '75%': base.quantile(0.75, axis=1),
                   '50%': base.quantile(0.50, axis=1), '25%': base.quantile(0.25, axis=1),
                   '5%': base.quantile(0.05, axis=1)})

dfA = pd.DataFrame({'95%': caseA.quantile(0.95, axis=1), '75%': caseA.quantile(0.75, axis=1),
                   '50%': caseA.quantile(0.50, axis=1), '25%': caseA.quantile(0.25, axis=1),
                   '5%': caseA.quantile(0.05, axis=1)})
# And plot it

ax = dfbase.plot(color = ['#1F1F1F', '#4A4A4A', 	'#969696', '#C9C9C9', '#E3E3E3'], linestyle = ':')            
dfA.plot(ax=ax, color = ['#1F1F1F', '#4A4A4A', 	'#969696', '#C9C9C9', '#E3E3E3'])

#pltBase = dfbase.plot(color = ['#1F1F1F', '#4A4A4A', 	'#969696', '#C9C9C9', '#E3E3E3'], linestyle = ':')            
#pltA = dfA.plot(color = ['#1F1F1F', '#4A4A4A', 	'#969696', '#C9C9C9', '#E3E3E3']) 
                         
                         
plt.ylabel('Average F_aa')
#plt.ylim(0, 120)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Hour (hr)')
plt.xlim(0, 24)
plt.xticks(np.arange(0,24,2))
plt.title('Accelerated Transformer Aging')
plt.legend(loc=(1.04,0.5))
plt.show()
                 
#%%

maxTrials = 300;
                         
hr = np.arange(0,24,1)

for col in range(maxTrials):
    hourLoad = data[:][col]
    plt.scatter(hr, hourLoad, s=1.5, c=hourLoad, cmap='Reds')

plt.ylabel('Loading (kW)')
plt.ylim(0, 120)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Hour (hr)')
plt.xlim(0, 24)
plt.xticks(np.arange(0,24,2))
plt.title('Transformer Loading Quantiles')
#plt.legend(loc=(1.04,0.5))
plt.show()