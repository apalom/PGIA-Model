# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 09:28:33 2018

@author: Alex
"""

# import libraries
import pandas as pd
import numpy as np
import timeit

# start timer 
start_time = timeit.default_timer()


# Import Case File
#df = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\sys\case4gs.xlsx', sheet_name=None, header=0)
    #df['Bus'].Pd

##---- Initialize Values ----##
base = 100;
numBus = len(df['Bus'])

err = 10;
threshold = 0.1;

# Build B Matrix
B = np.zeros((numBus, numBus));

for bus in range(0,numBus):
    f_Bus = df['Branch'].fbus[bus]
    t_Bus = df['Branch'].tbus[bus]
    B[f_Bus-1,t_Bus-1] = -1/(df['Branch'].x[bus])
    B[t_Bus-1,f_Bus-1] = -1/(df['Branch'].x[bus])
    print(f_Bus, t_Bus)

for bus in range(0,numBus):  
    B[bus,bus] = -np.sum(B[:,bus])

# Calculate Net P 
P_net = np.zeros(numBus);
P_gen = np.zeros(numBus);
P_load = np.zeros(numBus);
# Bus Net P Gen
for bus in range(0,numBus):
    busNode = df['Bus'].bus_i[bus]
    print('busNode: ' + str(busNode))
    try:
        idx  = df['Bus'].index[df['Bus'].bus_i == busNode][0]
        P_load[busNode-1] = df['Bus'].Pd[idx]
        idx  = df['Gen'].index[df['Gen'].bus == busNode][0]
        P_gen[busNode-1] = df['Gen'].Pg[idx]

    except KeyError:
        print('  KeyError')
    except IndexError:
        print('  IndexError')
        
P_net = P_gen - P_load;
# -----

# Per-Unitize P_Net
P_netPU = P_net/base;

# Remove Slack Bus Row
P_netPU = P_netPU[1:4];
B_PU = B[1:4,1:4];

# Calculate theta = inv(B)*P
theta = np.matmul(np.linalg.inv(B_PU),(-P_netPU))

# Calculate P Flows
numLine = len(df['Branch']);
P_flows = np.zeros(numLine);

for line in range(numLine):
    # Get from bus angle
    f_bus = df['Branch'].fbus[line]
    if f_bus == 1:
        f_theta = 0;
    else:
        f_theta = theta[f_bus-2];
    # Get to bus angle    
    t_bus = df['Branch'].tbus[line]
    if t_bus == 1:
        t_theta = 0;
    else:
        t_theta = theta[t_bus-2];
    
    P_flows[line] = base*(f_theta - t_theta)/df['Branch'].x[line];
    Amp_flow[line] = P_flows[line]

# Calculate Load Flows

P12 = base*(0 - theta[0])/df['Branch'].x[0]
P13 = base*(0 - theta[1])/df['Branch'].x[1]
P24 = base*(theta[0] - theta[2])/df['Branch'].x[2]
P34 = base*(theta[1] - theta[2])/df['Branch'].x[3]

matP_flows = np.array([-38.46, -97.09, 133.25, 104.75])


err = abs(P_flows-matP_flows)/matP_flows;

# timeit statement
elapsed = timeit.default_timer() - start_time
print('Execution time: {0:.4f} sec'.format(elapsed))