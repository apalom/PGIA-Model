# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 16:43:39 2018

@author: Alex
"""

def funcKDE(dfHomeDay, hr, numHomes, numBuses):
    
    from scipy import stats as st
    
    samplekWpHr = dfHomeDay.iloc[hr]
    my_kde = st.gaussian_kde(samplekWpHr)
    samplekWpHr = my_kde.resample(numHomes)
    
    # Note Homes 1 & 2 are on bus 9, H3-4 on b5, H5-6 b7
    # H7-8 on b8, H9-10 on b4, H11-12 on b6
    
    perBusLoad_kW = np.zeros((1, numBuses)))
    perBusLoad_kVAR = np.zeros((1, numBuses))
    
    #Bus 9 
    perBusLoad_kW[0][8] = samplekWpHr[0][0] + samplekWpHr[0][1]

    #Bus 5 
    perBusLoad_kW[0][4] = samplekWpHr[0][2] + samplekWpHr[0][3]
    
    #Bus 7 
    perBusLoad_kW[0][6] = samplekWpHr[0][4] + samplekWpHr[0][5]
    
    #Bus 8
    perBusLoad_kW[0][7] = samplekWpHr[0][6] + samplekWpHr[0][7]
    
    #Bus 4
    perBusLoad_kW[0][3] = samplekWpHr[0][8] + samplekWpHr[0][9]
    
    #Bus 6
    perBusLoad_kW[0][5] = samplekWpHr[0][10] + samplekWpHr[0][11]

    # Handle negative values and calculate kVAR        
    perBusLoad_kW = perBusLoad_kW.clip(min = 0)
    perBusLoad_kVAR = 0.62*perBusLoad_kW
    
    #dfSys['Bus'].Pd = samplekWpHr[0][:]
    #dfSys['Bus'].Qd = samplekVARpHr[0][:]
    
    return (perBusLoad_kW, perBusLoad_kVAR)