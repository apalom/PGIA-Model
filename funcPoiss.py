# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 09:23:51 2018

@author: Alex
"""

def funcPoiss(dfEV, dfSys, maxEV, chgrRate, hr, EVstoHomes, numHomes, numBuses):
    
    import numpy as np
    import random
    
    samplePoiss_kW = np.zeros((1, numHomes))    
    loadEV_kW = np.zeros((1, numBuses))
    loadEV_kVAR = np.zeros((1, numBuses))    

    # Profile from data    
    percentConnected = dfEV['Q3_max'][hr]
    numConnected = np.random.poisson(maxEV * percentConnected)    
    
    if (numConnected > maxEV):
        numConnected = maxEV
        
    EVatHome = np.zeros(maxEV)
    
    if (numConnected == 0):
        EVatHome = np.zeros(maxEV)
    
    elif (numConnected > 0 and numConnected < maxEV):
        while sum(EVatHome) != numConnected:
            for ev in range(numConnected):
                EVatHome[ev] = 1
        
    elif (numConnected == maxEV):
        EVatHome = np.ones(maxEV)
    
    i = 0
    for el in EVstoHomes:        
        samplePoiss_kW[0][el] = EVatHome[i] * chgrRate
        i += 1
          
    # Note Homes 1 & 2 are on bus 9, H3-4 on b5, H5-6 b7
    # H7-8 on b8, H9-10 on b4, H11-12 on b6    
    
    #Bus 9     
    bus9_kW = samplePoiss_kW[0][0] + samplePoiss_kW[0][1]
    loadEV_kW[0][8] = bus9_kW

    #Bus 5 
    bus5_kW = bus9_kW + samplePoiss_kW[0][2] + samplePoiss_kW[0][3]
    loadEV_kW[0][4] = bus5_kW
    
    #Bus 7 
    bus7_kW = samplePoiss_kW[0][4] + samplePoiss_kW[0][5]
    loadEV_kW[0][6] = bus7_kW
    
    # Bus 3
    bus3_kW = bus5_kW + bus7_kW
    loadEV_kW[0][2] = bus3_kW
    
    #Bus 8
    bus8_kW = samplePoiss_kW[0][6] + samplePoiss_kW[0][7]
    loadEV_kW[0][7] = bus8_kW
    
    #Bus 4
    bus4_kW = bus8_kW + samplePoiss_kW[0][8] + samplePoiss_kW[0][9]
    loadEV_kW[0][3] = bus4_kW
    
    #Bus 6
    bus6_kW = samplePoiss_kW[0][10] + samplePoiss_kW[0][11]
    loadEV_kW[0][5] = bus6_kW

    # Bus 2
    bus2_kW = bus4_kW + bus6_kW
    loadEV_kW[0][1] = bus2_kW
    
    #Bus 1
    loadEV_kW[0][0] = 0

    # Handle negative values and calculate kVAR        
    loadEV_kW = loadEV_kW.clip(min = 0)
    loadEV_kVAR = 0.62*loadEV_kW

    
    return (loadEV_kW, loadEV_kVAR, EVatHome)

