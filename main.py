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
#[dfSys, dfHome, dfEV] = funcLoadData()
#dfSys['Gen'].Pg = np.zeros((len(dfSys['Gen'].Pg)))[:]

#---- Define Parameters ----#
day = '2015-07-01'; # peak day for analysis

XFMR = 50; # Transformer rating (kVA)
secondaryL = 100 # Meters = 328 ft
chgrRate = 6.6; # Average charger power rating (kW)
maxEV = 4;
numHomes = 12;
numBuses = len(dfSys['Bus']) ;
numLines = numBuses - 1;
EVstoHomes = np.random.permutation(numHomes)[0:maxEV];

# Filter Home Load Data for Single Day
from funcPeakDay import *
[day, dfHomeDay] = funcPeakDay(day, dfHome)

day_P_flows = np.zeros((24,numLines))
day_Amp_flows = np.zeros((24,numLines))
day_Home_kW = np.zeros((24,numBuses))
day_EV_kW = np.zeros((24,numBuses))
day_Slack_kW_kVAR = np.zeros((24,2))

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
       
    # Sum Home and EV Loads
    dfSys['Bus'].Pd = (loadHome_kW + loadEV_kW)[0][:]
    dfSys['Bus'].Qd = (loadHome_kVAR + loadEV_kVAR)[0][:]
    
    slackBus = dfSys['Gen'][dfSys['Gen'].bus == 1].index[0]
       
    dfSys['Gen'].Pg[slackBus] = sum(sum(loadHome_kW + loadEV_kW))
    dfSys['Gen'].Qg[slackBus] = sum(sum(loadHome_kVAR + loadEV_kVAR))
            
    # DC Powerflow Function Call 
    from funcDCPF import *
    [B, B0, P_net, P_net0, theta, P_flows, Amp_flows] = funcDCPF(dfSys, hr)
    
    # Record daily energy import
    day_Slack_kW_kVAR[hr,0] = sum(sum(loadHome_kW + loadEV_kW))
    day_Slack_kW_kVAR[hr,1] = sum(sum(loadHome_kVAR + loadEV_kVAR))
    day_P_flows[hr,:] = P_flows;
    day_Amp_flows[hr,:] = Amp_flows;

# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))

print('\n [--- CASE: ' + str(maxEV) + 'EVs ' + str(chgrRate) + 'kW ---]')