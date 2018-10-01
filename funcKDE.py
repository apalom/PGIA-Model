# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 16:43:39 2018

@author: Alex
"""

def funcKDE(dfHomeDay, hr, numHomes, numBuses):
    
    from scipy import stats as st
    import numpy as np
    
    sampleKDE_kW = dfHomeDay.iloc[hr]
    my_kde = st.gaussian_kde(sampleKDE_kW)
    sampleKDE_kW = my_kde.resample(numHomes)
    
    # Note Homes 1 & 2 are on bus 9, H3-4 on b5, H5-6 b7
    # H7-8 on b8, H9-10 on b4, H11-12 on b6
    
    loadHome_kW = np.zeros((1, numBuses))
    loadHome_kVAR = np.zeros((1, numBuses))
    
    #Bus 9 
    loadHome_kW[0][8] = sampleKDE_kW[0][0] + sampleKDE_kW[0][1]

    #Bus 5 
    loadHome_kW[0][4] = sampleKDE_kW[0][2] + sampleKDE_kW[0][3]
    
    #Bus 7 
    loadHome_kW[0][6] = sampleKDE_kW[0][4] + sampleKDE_kW[0][5]
    
    #Bus 8
    loadHome_kW[0][7] = sampleKDE_kW[0][6] + sampleKDE_kW[0][7]
    
    #Bus 4
    loadHome_kW[0][3] = sampleKDE_kW[0][8] + sampleKDE_kW[0][9]
    
    #Bus 6
    loadHome_kW[0][5] = sampleKDE_kW[0][10] + sampleKDE_kW[0][11]

    # Handle negative values and calculate kVAR        
    loadHome_kW = loadHome_kW.clip(min = 0)
    loadHome_kVAR = 0.62*loadHome_kW
    
    #dfSys['Bus'].Pd = sampleKDE_kW[0][:]
    #dfSys['Bus'].Qd = samplekVARpHr[0][:]
    
    return (loadHome_kW, loadHome_kVAR)