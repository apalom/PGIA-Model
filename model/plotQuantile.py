# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:34:58 2018

@author: Alex
"""

import numpy as np
from scipy.stats import mstats
import matplotlib.pyplot as plt

# Create 10 columns with 100 rows of random data
rd = dfPxfmr
# Calculate the quantiles column wise
quantiles = mstats.mquantiles(rd, axis=0)
t = np.arange(0,23,1)
# Plot it
labels = ['5%', '25%', '50%', '75%', '95%']
for i, q in enumerate(quantiles):
    plt.plot(t, q, label=labels[i])
plt.legend()

#%%

import numpy as np
import pandas as pd
# Create random data
data = pd.DataFrame(data=dfPxfmr)

# Calculate all the desired values
df = pd.DataFrame({'95%': data.quantile(0.95, axis=1), '75%': data.quantile(0.75, axis=1),
                   '50%': data.quantile(0.50, axis=1), '25%': data.quantile(0.25, axis=1),
                   '5%': data.quantile(0.05, axis=1)})
# And plot it
plot1 = df.plot(color = ['#1F1F1F', '#4A4A4A', 	'#969696', '#C9C9C9', '#E3E3E3'])            
                         
#plt.legend(['95%', '75%', '50%', '25%', '5%'])
plt.ylabel('Loading (kW)')
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Hour (hr)')
plt.xlim(0, 24)
plt.xticks(np.arange(0,24,2))
plt.title('Transformer Loading Quantiles')
plt.legend(loc=(1.04,0.5))
plt.show()
