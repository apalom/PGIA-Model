# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 16:30:52 2018

@author: Alex

"""

# start timer 
timeMain = timeit.default_timer()

# import libraries
import pandas as pd
import numpy as np
import timeit

#---- Define Parameters ----#
day = '2015-07-01'; # peak day for analysis
maxEV = 2;
XFMR = 50;


# Load Data Function Call 
#from funcLoadData import *
#[dfSys, dfHome, dfEV] = funcLoadData()

# Filter Home Load Data for Single Day
from funcPeakDay import *
[day, dfHomeDay] = funcPeakDay(day, dfHome)

day_P_flows = np.zeros((24,len(dfSys)+1))

for hr in range(24):
    #dfSys['Bus'].Pd = dfSys['Bus'].Pd * (1+(hr/100))

    # DC Powerflow Function Call 
    from funcDCPF import *
    [B, B0, P_net, P_net0, theta, P_flows, Amp_flows] = funcDCPF(dfSys)
    
    day_P_flows[hr,:] = P_flows;


# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))