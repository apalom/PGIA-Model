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

from funcLoadData import funcLoadData
[dfSys, dfHome, dfEV, dfNSRDB] = funcLoadData()
dfSys['Gen'].Pg = np.zeros((len(dfSys['Gen'].Pg)))[:]


#---- Define Parameters ----#
day = '2015-07-01'; # peak day for analysis

maxTrials = 100;
XFMR = 75; # Transformer rating (kVA)
XFMRlimit= 1.3 * XFMR;
secLimit = 218 # Amps for Overload Based [218 for 4/0 AL cables in DA411]
chgrRate = 12.9; # Average charger power rating (kW)
maxEV = 2;
maxPV = 2;
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

day_Amp_Flow_Prev = np.zeros((24,numLines));
day_P_bus_Prev = np.zeros((24,numBuses));

outGHI = np.zeros((24,maxTrials));
outTemps = np.zeros((24,maxTrials));
outPxfmr = np.zeros((24,maxTrials));
outL1amp = np.zeros((24,maxTrials));
outL3amp = np.zeros((24,maxTrials));
outL7amp = np.zeros((24,maxTrials));
outFaa = np.zeros((24,maxTrials));
outthetaH = np.zeros((24,maxTrials));
outAvgAmps = np.zeros((24,numLines));

# Filter Home Load Data for Single Day
from funcPeakDay import *
[day, dfHomeDay, dfTempDay, dfGHIDay] = funcPeakDay(day, dfHome, dfNSRDB)
#%%
for trial in range(maxTrials):

    ## -- case Base -- ##
    # Randomly assign EV and PV to buses
    #EVstoHomes = np.random.permutation(numHomes)[0:0]
    #PVtoHomes = np.random.permutation(numHomes)[0:0]
    
    ## -- case A -- ##
    # EVs Only At End of Lines [1, 6, 7, 12]
    #EVstoHomes = [0, 1]#, 4, 5, 6, 7, 10, 11];
    #PVtoHomes = np.random.permutation(numHomes)[0:0];
    
    ## -- case B -- ##
    # EVs + PVs At End of Lines
    #EVstoHomes = [0, 1]#, 4, 5, 6, 7, 10, 11];
    #PVtoHomes = [0, 1]#, 4, 5, 6, 7, 10, 11];
    
    ## -- case C -- ##
    # Randomly assign EV and PV to buses
    EVstoHomes = np.random.permutation(numHomes)[0:maxEV]
    PVtoHomes = np.random.permutation(numHomes)[0:maxPV]
    
    
    # Initialize Day Calculations
    day_P_flows = np.zeros((24,numLines))
    day_L1amp = np.zeros((24,1))
    day_L3amp = np.zeros((24,1))
    day_L7amp = np.zeros((24,1))
    
    day_Amp_flows = np.zeros((24,numLines))
    day_Temps = np.zeros((24,1))
    day_GHI = np.zeros((24,1))
    day_P_bus = np.zeros((24,9))
    day_Home_kW = np.zeros((24,numBuses))
    day_EV_kW = np.zeros((24,numBuses))
    day_PV_kW = np.zeros((24,numBuses))
    day_Slack_kW_kVAR = np.zeros((24,2))
    
    
    for hr in range(24):
        #dfSys['Bus'].Pd = dfSys['Bus'].Pd * (1+(hr/100))
    
        # Apply KDE to Home Loads
        from funcKDE import funcKDE
        [loadHome_kW, loadHome_kVAR, hrTempC, hrGHI] = funcKDE(dfHomeDay, dfTempDay, dfGHIDay, hr, numHomes, numBuses)
        day_Home_kW [hr,:] = loadHome_kW
        day_Temps[hr,:] = hrTempC
        day_GHI[hr,:] = hrGHI
    
        # Apply Poisson to EV Loads
        from funcPoiss import funcPoiss
        [loadEV_kW, loadEV_kVAR, EVatHome] = funcPoiss(dfEV, dfSys, maxEV, chgrRate, hr, EVstoHomes, numHomes, numBuses)
        day_EV_kW[hr,:] = loadEV_kW
        
        # PV Solar Gen (no distribution)
        from funcSolar import funcSolar
        [genPV_kW, genPV_kVAR] = funcSolar(maxPV, hrGHI, hr, PVtoHomes, numHomes, numBuses)    
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
        from funcDCPF import funcDCPF
        [B, B0, P_net, P_net0, P_bus, theta, P_flows, Amp_flows] = funcDCPF(dfSys)

        # Record daily energy 
        day_Slack_kW_kVAR[hr,0] = sum(sum(loadHome_kW + loadEV_kW))
        day_Slack_kW_kVAR[hr,1] = sum(sum(loadHome_kVAR + loadEV_kVAR))
        day_P_flows[hr,:] = P_flows;
        day_L1amp[hr,:] = Amp_flows[0];    
        day_L3amp[hr,:] = Amp_flows[2];    
        day_L7amp[hr,:] = Amp_flows[6];    
        day_Amp_flows[hr,:] = Amp_flows;
                
        day_P_bus[hr,:] = P_bus;  
        day_P_xfmr = day_P_bus[:,0];
                        
    # XFMR Aging Function Call 
    from funcAging import funcAging
    [day_Faa, day_thetaH] = funcAging(day_Temps, day_P_xfmr, XFMR)
    
        
    # Plot Heat Maps
    #from heatmap1 import *
    #[] = heatmap1(day_Amp_flows)
    
    #dfOutput.iloc[trial][:] = sum((day_Amp_flows > secLimit).astype(int))
    maxXFMR = np.max(day_P_xfmr);
    dfAvgAmps = (day_Amp_Flow_Prev + day_Amp_flows);  
    dfAvgPbus = (day_P_bus_Prev + day_P_bus);  
    #dfLineOverloads[trial] = sum((day_Amp_flows > secLimit).astype(int)); 
    #dfXFMRoverloads[trial] = sum((day_P_xfmr > XFMRlimit).astype(int));   
    outGHI[:,trial] = day_GHI[:,0];
    outTemps[:,trial] = day_Temps[:,0];
    outPxfmr[:,trial] = day_P_xfmr;
    outL1amp[:,trial] = day_L1amp[:,0];
    outL3amp[:,trial] = day_L3amp[:,0];
    outL7amp[:,trial] = day_L7amp[:,0];
    outFaa[:,trial] = day_Faa[:,0];
    outthetaH[:,trial] = day_thetaH[:,0];
    
    day_Amp_Flow_Prev = dfAvgAmps;
    day_P_bus_Prev = dfAvgPbus;
    
    print('\n [--- Trial: '+ str(trial) +' CASE: ' + str(maxEV) + 'EVs ' + str(chgrRate) + 'kW chgr ' + str(maxPV) + 'PV ' + str(XFMR) + 'kVA ---] \n')    

#    
#    #Output Data
#    fileName = r'C:\Users\Alex\Documents\GitHub\PGIA-Model\model\data\dayAmps_' + str(trial) + '.csv'
#    #outputFile = open(fileName, 'w')  
#    with open(fileName, 'w') as outputFile:  
#       writer = csv.writer(outputFile)
#       writer.writerows(day_Amp_flows)
#

outAvgAmps = dfAvgAmps/(trial+1);
outAvgPbus = dfAvgPbus/(trial+1);
   
fileName = 'outputData\outPxfmr_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(outPxfmr)
   
fileName = 'outputData\outL1amp_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(outL1amp)

fileName = 'outputData\outL3amp_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(outL3amp)
   
fileName = 'outputData\outL7amp_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(outL7amp)   

fileName = 'outputData\outFaa_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(outFaa)
   
fileName = 'outputData\outAvgAmps_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(outAvgAmps)
   
fileName = 'outputData\outAvgPbus_' + str(trial) + '.csv'
#outputFile = open(fileName, 'w')  
with open(fileName, 'w') as outputFile:  
   writer = csv.writer(outputFile)
   writer.writerows(outAvgPbus)

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

