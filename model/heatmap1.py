# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 15:04:36 2018

@author: Alex
"""

def heatmap1(day_Amp_flows):
    
    import seaborn as sns; sns.set()
    import numpy as np
    
    heatArray = day_Amp_flows.transpose()
    
    maxVal = np.max(heatArray);
    minVal = np.min(heatArray);
    
    ax = sns.heatmap(heatArray, vmin=minVal, vmax=maxVal, cmap='gist_heat_r')
    
    return() 