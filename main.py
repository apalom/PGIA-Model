# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 16:30:52 2018

@author: Alex

"""

# start timer 
start_time = timeit.default_timer()

# import libraries
import pandas as pd
import numpy as np
import timeit


# Import Case File
df = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\sys\case4gs.xlsx', sheet_name=None, header=0)

# function call 
from funcDCPF import funcDCPF

[B, B0, P_net, P_net0, theta, P_flows, Amp_flows] = funcDCPF(df)



# timeit statement
elapsed = timeit.default_timer() - start_time
print('Main time: {0:.4f} sec'.format(elapsed))