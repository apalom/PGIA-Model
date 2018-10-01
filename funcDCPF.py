# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 09:28:33 2018

@author: Alex
"""

def funcDCPF(dfSys, hr):
    
    # import libraries
    import pandas as pd
    import numpy as np
    import timeit
    
    # start timer 
    timeDCPF = timeit.default_timer()
    
    print('Hr: ', hr)
    
    ##---- Initialize Values ----##
    base = 100;
    numBus = len(dfSys['Bus'])
    numLine = numBus - 1
    
    err = 10;
    threshold = 0.1;
    
    # Build B Matrix
    B = np.zeros((numBus, numBus));
    
    for line in range(0,numLine):
        f_Bus = dfSys['Branch'].fbus[line]
        t_Bus = dfSys['Branch'].tbus[line]
        B[f_Bus-1,t_Bus-1] = -1/(dfSys['Branch'].x[line])
        B[t_Bus-1,f_Bus-1] = -1/(dfSys['Branch'].x[line])
        print(f_Bus, t_Bus)
        
    # Calculate Net P 
    P_net = np.zeros(numBus);
    P_gen = np.zeros(numBus);
    P_load = np.zeros(numBus);
    # Bus Net P Gen
    for bus in range(0,numBus):
        busNode = dfSys['Bus'].bus_i[bus]
        print('busNode: ' + str(busNode))
        try:
            idx  = dfSys['Bus'].index[dfSys['Bus'].bus_i == busNode][0]
            P_load[busNode-1] = dfSys['Bus'].Pd[idx]
            idx  = dfSys['Gen'].index[dfSys['Gen'].bus == busNode][0]
            P_gen[busNode-1] = dfSys['Gen'].Pg[idx]
    
        except KeyError:
            print(' KeyError')
        except IndexError:
            print('  IndexError')
            
    P_net = (P_gen - P_load)/base;
    # -----
    
    # Remove Slack Bus Row
    P_net0 = P_net[1:numBus];
    B0 = B[1:numBus,1:numBus];
    
    for bus in range(0,numBus-1):  
        B0[bus,bus] = -np.sum(B0[bus,:])
    
    # Calculate theta = inv(B)*P
    theta = np.matmul(np.linalg.inv(B0),(-P_net0))
    
    # Calculate P Flows
    numLine = len(dfSys['Branch']);
    P_flows = np.zeros(numLine);
    
    for line in range(numLine):
        # Get from bus angle
        f_bus = dfSys['Branch'].fbus[line]
        if f_bus == 1:
            f_theta = 0;
        else:
            f_theta = theta[f_bus-2];
        # Get to bus angle    
        t_bus = dfSys['Branch'].tbus[line]
        if t_bus == 1:
            t_theta = 0;
        else:
            t_theta = theta[t_bus-2];
        
        P_flows[line] = base*(f_theta - t_theta)/dfSys['Branch'].x[line];
    
    Amp_flows = np.sqrt(abs(P_flows)/dfSys['Branch'].x);
    
    # Compare Flows with MATPOWER Results
    matP_flows = np.array([-38.46, -97.09, 133.25, 104.75])
    err = abs(P_flows-matP_flows)/matP_flows;
    
    # timeit statement
    elapsedDCPF = timeit.default_timer() - timeDCPF
    print('funcDCPF time: {0:.4f} sec'.format(elapsedDCPF))

    return (B, B0, P_net, P_net0, theta, P_flows, Amp_flows)