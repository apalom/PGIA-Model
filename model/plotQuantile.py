# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:34:58 2018

@author: Alex
"""

import numpy as np
from scipy.stats import mstats
import matplotlib.pyplot as plt
import pandas as pd


dfPxfmr = pd.read_csv(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\CaseA\xfmrGen_1199.csv', header=None)
                 
#%%

# Create random data
data = pd.DataFrame(data=dfPxfmr)

hr = np.arange(0,24,1)

# Calculate all the desired values
df = pd.DataFrame({'95%': data.quantile(0.95, axis=1), '75%': data.quantile(0.75, axis=1),
                   '50%': data.quantile(0.50, axis=1), '25%': data.quantile(0.25, axis=1),
                   '5%': data.quantile(0.05, axis=1)})
# And plot it
plot1 = df.plot(color = ['#1F1F1F', '#4A4A4A', 	'#969696', '#C9C9C9', '#E3E3E3'])            
                         
                         
plt.ylabel('Loading (kW)')
plt.ylim(0, 120)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Hour (hr)')
plt.xlim(0, 24)
plt.xticks(np.arange(0,24,2))
plt.title('Transformer Loading Quantiles')
plt.legend(loc=(1.04,0.5))
plt.show()
                 
#%%
                         
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