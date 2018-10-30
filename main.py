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

maxTrials = 10
XFMR = 50; # Transformer rating (kVA)
#secLength = 100 # Meters = 328 ft
secLimit = 80 # Amps for Overload 
chgrRate = 19.2; # Average charger power rating (kW)
maxEV = 6;
maxPV = 3;
numHomes = 12;

# Calculate system values
numBuses = len(dfSys['Bus'])
numLines = len(dfSys['Branch'])

'''
# Create Input DataFrame
inputData = {'maxTrials': [maxTrials], 
             'XFMR': [XFMR], 
             'secLimit': [secLimit], 
             'chgrRate': [chgrRate], 
             'maxEV': [maxEV], 
             'maxPV': [maxPV], 
             'numHomes': [numHomes]}
dfInput = pd.DataFrame(data=inputData);
'''

outputData = {'L1': np.zeros((maxTrials)), 'L2': np.zeros((maxTrials)),
              'L3': np.zeros((maxTrials)), 'L4': np.zeros((maxTrials)), 
              'L5': np.zeros((maxTrials)), 'L6': np.zeros((maxTrials)),
              'L7': np.zeros((maxTrials)), 'L8': np.zeros((maxTrials))}
dfOutput = pd.DataFrame(data=outputData);

# Filter Home Load Data for Single Day
from funcPeakDay import *
[day, dfHomeDay, dfSolarDay] = funcPeakDay(day, dfHome, dfSolar)

for trial in range(maxTrials):

    # Randomly assign EV and PV to buses
    EVstoHomes = np.random.permutation(numHomes)[0:maxEV]
    PVtoHomes = np.random.permutation(numHomes)[0:maxPV]
    
    # Initialize Day Calculations
    day_P_flows = np.zeros((24,numLines))
    day_Amp_flows = np.zeros((24,numLines))
    day_Home_kW = np.zeros((24,numBuses))
    day_EV_kW = np.zeros((24,numBuses))
    day_PV_kW = np.zeros((24,numBuses))
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
        
    # Plot Heat Maps
    from heatmap1 import *
    [] = heatmap1(day_Amp_flows)
    
    dfOutput.iloc[trial][:] = sum((day_Amp_flows > secLimit).astype(int))
    
    print('\n [--- Trial: '+ str(trial) +' CASE: ' + str(maxEV) + 'EVs ' + str(chgrRate) + 'kW chgr ' + str(maxPV) + 'PV ---]')


# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))

#print('\n [--- CASE: ' + str(maxEV) + 'EVs ' + str(chgrRate) + 'kW chgr ' + str(maxPV) + 'PV ---]')

#%%
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

