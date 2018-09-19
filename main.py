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

# Load Data Function Call 
from funcLoadData import *
[dfSys, dfHome, dfEV] = funcLoadData()


# DC Powerflow Function Call 
from funcDCPF import *
[B, B0, P_net, P_net0, theta, P_flows, Amp_flows] = funcDCPF(dfSys)



# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))