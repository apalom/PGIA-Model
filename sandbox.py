# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 16:29:21 2018

@author: Alex
"""
import scipy as sp
from scipy import stats as st
import matplotlib.pyplot as plt
import numpy as np


maindat = dfHomeDay;
numHomes = 12;
hr = 19;

maindat = maindat.iloc[hr]
my_kde = st.gaussian_kde(maindat)
sample = my_kde.resample(100)

#x    = sp.linspace(sample[0,0], sample[0,-1], 100)
x    = sp.linspace(0, np.ceil(max(maindat)), 26)
fig  = plt.figure()
fig1 = fig.add_subplot(111)

kde_dist = my_kde(x)
#%%
    
loadHr = dfHomeDay.iloc[hr]
my_kde = st.gaussian_kde(loadHr)
loadSample = my_kde.resample(numHomes)
    

#%%
fig, ax = plt.subplots()

#histogram
ax.hist(sample, 10, density=1)

ax.plot(x, kde_dist, '--')
ax.set_xlabel('Load (kW)')
ax.set_ylabel('Probability density')
ax.set_title(r'Histogram')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()

#%%
ax.hist(x, num_bins, density=1)
plt.plot(x, kde_dist,'b--')
plt.hist(sample, density=1, facecolor='blue', alpha=0.2)
plt.xlabel('Loading (kW)')
plt.xlim(0, 10)
plt.show()

loadCDF = np.zeros((len(x), 3))
loadCDF[:,0] = x;
loadCDF[:,1] = kde_dist;

for i in range(len(loadCDF)):
    loadCDF[i,2] = np.sum(loadCDF[0:i,1])
   
    
#%%
    
np.random.seed(19680801)

# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(437)

num_bins = 50

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=1)

# add a 'best fit' line
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
ax.plot(bins, y, '--')
ax.set_xlabel('Smarts')
ax.set_ylabel('Probability density')
ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()