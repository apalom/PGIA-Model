# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 09:21:36 2018

@author: Alex
"""

import matplotlib.pyplot as plt


bin_edges = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
n, bins, patches = plt.hist(dfHomeDay.iloc[19,:], bins=bin_edges, density=True, rwidth=0.9, color='#607c8e')

font = {'family' : 'Times New Roman',
        'size'   : 18}
plt.rc('font', **font)
                            
plt.rcParams["figure.figsize"] = [8,6]
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Loading (kW)')
plt.ylabel('Frequency')
plt.title('Loading Histogram (19:00)')

print(plt.rcParams["figure.figsize"])