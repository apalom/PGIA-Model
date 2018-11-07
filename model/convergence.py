# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 12:24:05 2018

@author: Alex
"""

import numpy as np

# Precision level 
prscn = 0.5 #kW

# 95% Confidence level - z-score = 1.96
zScore = 1.96;

# Data to test convergence
maxXFMRperTrial = np.max(dfPxfmr, axis=0)
stdDev = np.std(maxXFMRperTrial)


#https://www.valuationresearch.com/wp-content/uploads/2017/11/SpecialReport_MonteCarloSimulationTrials.pdf
trialsNeeded = ((zScore*(stdDev/prscn)))**2

print('Trials needed to achieve 95% confidence: ', trialsNeeded)

#%% Calculate Running Average

import matplotlib.pyplot as plt

#runningAvg = np.zeros((1,1000))
runningAvg = [];
i = 0;

for i in range(len(maxXFMRperTrial)):
    
    total = np.sum(maxXFMRperTrial[0:i])
    currentAvg = total/(i+1)
    runningAvg.append(currentAvg)
    
#%% Plot Converge

upper_bound = np.array([currentAvg+prscn for i in range(len(maxXFMRperTrial))])
lower_bound = np.array([currentAvg-prscn for i in range(len(maxXFMRperTrial))])

ser = np.linspace(0,1000,1000)    
#runningAvg = runningAvg[1:1000]
plt.plot(ser, runningAvg, 'k')
plt.plot(ser, maxXFMRperTrial, 'b.', markersize = 1.5)
plt.plot(ser, upper_bound, '--', linewidth=1, color='grey')
plt.plot(ser, lower_bound, '--', linewidth=1, color='grey')
plt.ylabel('Running Average (kW)')
plt.ylim((82., 86.5)) 
plt.xlabel('Trials')
plt.title('Maximum Transformer Load Per Trial')
plt.show()

