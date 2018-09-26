# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 09:23:51 2018

@author: Alex
"""

def funcPoiss(dfEV, dfSys, maxEV, chgrRate, hr, EVstoHomes):
    
    import numpy as np
    import random
    
    percentConnected = dfEV['Q3_max'][hr]
    numConnected = np.random.poisson(maxEV * percentConnected)
    
    numConnected = numConnected.clip(max = maxEV)
    
    EVatHome = np.zeros(maxEV)
    
    if (numConnected == 0):
        EVatHome = np.zeros(maxEV)
    
    elif (numConnected > 0 and numConnected < maxEV):
        while sum(EVatHome) != numConnected:
            for ev in range(numConnected):
                EVatHome[ev] = 1
        
    elif (numConnected == maxEV):
        EVatHome = np.ones(maxEV)
        
    loadEV = np.zeros(len(dfSys['Bus']))
    
    i = 0
    for el in EVstoHomes:        
        loadEV[el] = EVatHome[i] * chgrRate
        i += 1
    
    return (EVatHome, loadEV)

