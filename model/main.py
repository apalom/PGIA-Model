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
import csv

# start timer 
timeMain = timeit.default_timer()

# Load Data Function Call 
from funcLoadData import *
[dfSys, dfHome, dfEV, dfSolar] = funcLoadData()
dfSys['Gen'].Pg = np.zeros((len(dfSys['Gen'].Pg)))[:]


#---- Define Parameters ----#
day = '2015-07-01'; # peak day for analysis

maxTrials = 3;
XFMR = 50; # Transformer rating (kVA)
XFMRlimit= 1.3 * XFMR;
#secLength = 100 # Meters = 328 ft
secLimit = 80 # Amps for Overload Based [218 for 4/0 AL cables in DA411]
chgrRate = 12.9; # Average charger power rating (kW)
maxEV = 4;
maxPV = 4;
numHomes = 12;

# Calculate system values
numBuses = len(dfSys['Bus'])
numLines = len(dfSys['Branch'])

'''
#Load Per Secondary
    UGTX_4/0AWG_SAL_NTRXC (Trade Name: Sweetbrier)
    Allowable Ampacity-Direct Burial: 315 Amps (600V)
    Allowable Ampacity-In Duct: 240 Amps (600V)
    AC Resistance @ 75C: 0.101 / 1000ft
    AC Resistance @ 90C: 0.105 / 1000ft
    Voltage = 240V
    
    Per-Unit Reactance
    Sweetbriar has resistance of 0.101 / 1000ft. 
        Assume 250ft per cable = 0.02525 
        Assume 125ft per cable = 0.012625
    zBase = 0.576
    pu_X = 0.02525/zBase = 0.0438
    pu_X = 0.012625/zBase = 0.0219

outputData = {'L1': np.zeros((maxTrials)), 'L2': np.zeros((maxTrials)),
              'L3': np.zeros((maxTrials)), 'L4': np.zeros((maxTrials)), 
              'L5': np.zeros((maxTrials)), 'L6': np.zeros((maxTrials)),
              'L7': np.zeros((maxTrials)), 'L8': np.zeros((maxTrials))}
dfOverloads = pd.DataFrame(data=outputData);
'''

dfLineOverloads = np.zeros((maxTrials,numLines));
dfXFMRoverloads = np.zeros((maxTrials,1));
dfPxfmr = np.zeros((24,maxTrials));
dfAvgAmps = np.zeros((24,numLines));
day_Amp_Flow_Prev = np.zeros((24,numLines));
day_P_bus_Prev = np.zeros((24,numBuses));

# Filter Home Load Data for Single Day
from funcPeakDay import *
[day, dfHomeDay, dfSolarDay] = funcPeakDay(day, dfHome, dfSolar)

for trial in range(maxTrials):

    ## -- case A -- ##
    # EVs Only At End of Lines [1, 6, 7, 12]
    EVstoHomes = [0, 5, 6, 11];
    PVtoHomes = np.random.permutation(numHomes)[0:maxPV];
    
    ## -- case B -- ##
    # EVs + PVs At End of Lines
    #EVstoHomes = [0, 5, 6, 11];
    #PVtoHomes = [0, 5, 6, 11];
    
    ## -- case C -- ##
    # Randomly assign EV and PV to buses
    #EVstoHomes = np.random.permutation(numHomes)[0:maxEV]
    #PVtoHomes = np.random.permutation(numHomes)[0:maxPV]
    
    
    # Initialize Day Calculations
    day_P_flows = np.zeros((24,numLines))
    day_Amp_flows = np.zeros((24,numLines))
    day_P_bus = np.zeros((24,9))
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
        [B, B0, P_net, P_net0, P_bus, theta, P_flows, Amp_flows] = funcDCPF(dfSys)
        
        # Record daily energy import
        day_Slack_kW_kVAR[hr,0] = sum(sum(loadHome_kW + loadEV_kW))
        day_Slack_kW_kVAR[hr,1] = sum(sum(loadHome_kVAR + loadEV_kVAR))
        day_P_flows[hr,:] = P_flows;
        day_Amp_flows[hr,:] = Amp_flows;    
        day_P_bus[hr,:] = P_bus;  
        day_P_xfmr = day_P_bus[:,0];
    
        
    # Plot Heat Maps
    #from heatmap1 import *
    #[] = heatmap1(day_Amp_flows)
    
    #dfOutput.iloc[trial][:] = sum((day_Amp_flows > secLimit).astype(int))
    maxXFMR = np.max(day_P_xfmr);
    dfAvgAmps = (day_Amp_Flow_Prev + day_Amp_flows);  
    dfAvgPbus = (day_P_bus_Prev + day_P_bus);  
    dfLineOverloads[trial] = sum((day_Amp_flows > secLimit).astype(int)); 
    dfXFMRoverloads[trial] = sum((day_P_xfmr > XFMRlimit).astype(int));   
    dfPxfmr[:,trial] = day_P_xfmr;
    
    day_Amp_Flow_Prev = dfAvgAmps;
    
    print('\n [--- Trial: '+ str(trial) +' CASE: ' + str(maxEV) + 'EVs ' + str(chgrRate) + 'kW chgr ' + str(maxPV) + 'PV ---] \n')    

#    
#    #Output Data
#    fileName = r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\dayAmps_' + str(trial) + '.csv'
#    #outputFile = open(fileName, 'w')  
#    with open(fileName, 'w') as outputFile:  
#       writer = csv.writer(outputFile)
#       writer.writerows(day_Amp_flows)
#

dfAvgAmps = dfAvgAmps/(trial+1);
dfAvgPbus = dfAvgPbus/(trial+1);

fileName = r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\dayAvgAmps_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(day_Amp_flows)
   
fileName = r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\lineOverloads_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(dfLineOverloads)
   
fileName = r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\avgPbus_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(dfAvgPbus)
   
fileName = r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\xfmrGen_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(dfPxfmr)
   
fileName = r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\xfmrOverloads_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(dfXFMRoverloads)


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

