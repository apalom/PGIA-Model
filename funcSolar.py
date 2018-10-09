# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 08:12:09 2018

@author: Alex
"""

def funcSolar(maxPV, dfSolarDay, hr, PVtoHomes, numHomes, numBuses):
    
    import numpy as np
    import random
    
    genPV_kW = np.zeros((1, numBuses))
    genPV_kVAR = np.zeros((1, numBuses))    
    sampleSolar_kW = np.zeros((1, numHomes))    

    # Profile from data   
    # DNI Direct Normal Radiation [w/m2]
    pvSize = 35; # Assume 6kW system size ~ 35 m2
    pvEff = 0.20; # Assume system efficiency of 20%
            
  
    for el in PVtoHomes:        
        sampleSolar_kW[0][el] = (dfSolarDay['DNI'][hr]/1000)*pvSize*pvEff

    # Note Homes 1 & 2 are on bus 9, H3-4 on b5, H5-6 b7
    # H7-8 on b8, H9-10 on b4, H11-12 on b6    
    
    #Bus 9 
    bus9_kW = sampleSolar_kW[0][0] + sampleSolar_kW[0][1]
    genPV_kW[0][8] = bus9_kW

    #Bus 5 
    bus5_kW = sampleSolar_kW[0][2] + sampleSolar_kW[0][3]
    genPV_kW[0][4] = bus5_kW

    #Bus 7 
    bus7_kW = sampleSolar_kW[0][4] + sampleSolar_kW[0][5]
    genPV_kW[0][6] = bus7_kW
    
    #Bus 3 
    genPV_kW[0][2] = 0
        
    #Bus 8
    bus8_kW = sampleSolar_kW[0][6] + sampleSolar_kW[0][7]
    genPV_kW[0][7] = bus8_kW
    
    #Bus 4
    bus4_kW = sampleSolar_kW[0][8] + sampleSolar_kW[0][9]
    genPV_kW[0][3] = bus4_kW
    
    #Bus 6
    bus6_kW = sampleSolar_kW[0][10] + sampleSolar_kW[0][11]
    genPV_kW[0][5] = bus6_kW
    
    #Bus 2 
    genPV_kW[0][1] = 0    

    #Slack Bus
    genPV_kW[0][0] = 0
        
    
    # Handle negative values and calculate kVAR        
    genPV_kW = genPV_kW.clip(min = 0)
    genPV_kVAR = 0.01*genPV_kW
    
    return (genPV_kW, genPV_kVAR)