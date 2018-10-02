# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 16:30:52 2018

@author: Alex

"""

# import libraries
import pandas as pd
import numpy as np
import timeit
from itertools import permutations 

# start timer 
timeMain = timeit.default_timer()

# Load Data Function Call 
#from funcLoadData import *
#[dfSys, dfHome, dfEV, dfSolar] = funcLoadData()
#dfSys['Gen'].Pg = np.zeros((len(dfSys['Gen'].Pg)))[:]

#---- Define Parameters ----#
day = '2015-07-01'; # peak day for analysis

maxTrial = 100
XFMR = 50; # Transformer rating (kVA)
secondaryL = 100 # Meters = 328 ft
chgrRate = 19.2; # Average charger power rating (kW)
maxEV = 4;
maxPV = 4;
numHomes = 12;


inputData = {'maxTrial': [maxTrial], 
             'XFMR': [XFMR], 
             'secondaryL': [secondaryL], 
             'chgrRate': [chgrRate], 
             'maxEV': [maxEV], 
             'maxPV': [maxPV], 
             'numHomes': [numHomes]}

dfInput = pd.DataFrame(data=inputData);

# Filter Home Load Data for Single Day
from funcPeakDay import *
[day, dfHomeDay, dfSolarDay] = funcPeakDay(day, dfHome, dfSolar)

# Run Monte Carlo
from funcMonteCarlo import *
[day, dfHomeDay, dfSolarDay] = funcPeakDay(day, dfSys, dfHome, dfEV, dfSolar, dfInput)


'''
for hr in range(24):
    #dfSys['Bus'].Pd = dfSys['Bus'].Pd * (1+(hr/100))

    # Apply KDE to Home Loads
    from funcKDE import *
    [loadHome_kW, loadHome_kVAR] = funcKDE(dfHomeDay, hr, numHomes, numBuses)
    day_Home_kW [hr,:] = loadHome_kW

    # Apply Poisson to EV Loads
    from funcPoiss import *
    [loadEV_kW, loadEV_kVAR, EVatHome] = funcPoiss(dfEV, dfSys, maxEV, chgrRate, hr, EVstoHomes, numHomes, numBuses)
    day_EV_kW[hr,:] = loadEV_kW
    
    # PV Solar Gen (no distribution)
    from funcSolar import *
    [genPV_kW, genPV_kVAR] = funcSolar(maxPV, dfSolarDay, hr, PVtoHomes, numHomes, numBuses)    
    day_PV_kW[hr,:] = genPV_kW
       
    # Sum Home and EV Loads
    dfSys['Bus'].Pd = (loadHome_kW + loadEV_kW)[0][:]
    dfSys['Bus'].Qd = (loadHome_kVAR + loadEV_kVAR)[0][:]
    
    # Calculate PV Gen
    dfSys['Gen'].Pg[1:] = genPV_kW[0][1:]
    dfSys['Gen'].Pg[1:] = genPV_kVAR[0][1:]
    
    # Calculate Slack Bus Gen
    slackBus = dfSys['Gen'][dfSys['Gen'].bus == 1].index[0]
       
    dfSys['Gen'].Pg[slackBus] = sum(sum(loadHome_kW + loadEV_kW - genPV_kW))
    dfSys['Gen'].Qg[slackBus] = sum(sum(loadHome_kVAR + loadEV_kVAR - genPV_kVAR))
            
    # DC Powerflow Function Call 
    from funcDCPF import *
    [B, B0, P_net, P_net0, theta, P_flows, Amp_flows] = funcDCPF(dfSys)
    
    # Record daily energy import
    day_Slack_kW_kVAR[hr,0] = sum(sum(loadHome_kW + loadEV_kW))
    day_Slack_kW_kVAR[hr,1] = sum(sum(loadHome_kVAR + loadEV_kVAR))
    day_P_flows[hr,:] = P_flows;
    day_Amp_flows[hr,:] = Amp_flows;
'''

# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))

print('\n [--- CASE: ' + str(maxEV) + 'EVs ' + str(chgrRate) + 'kW chgr ' + str(maxPV) + 'PV ---]')