# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:46:46 2018

@author: Alex
"""

import pandas as pd
import numpy as np
import math

xfmrRating = 50

#dfTemp = pd.read_excel(r'C:\Users\Alex\Documents\GitHub\PGIA-Model\data\july1_temp.xlsx');
thetaA = dfTemp.TEMPC;
L = day_P_xfmr;

# Transformer Parameters
dThetaTOr = 65; # 
dThetaH = 10;
n = 0.8 # for ONAN cooling
g = 29.38; # gallons of oil in 50kVA xfmr
w = 713; # weight of xfmr
C = 0.05*w + 1.33*g; # oil-time constant
P_rl = 586; # rated load loss W
P_nll = 86; # no load loss W
R = P_rl / P_nll;

tauTOr = (C*dThetaTOr)/P_rl

#thetaH = np.zeros((len(L),1))
dThetaTO = np.zeros((len(L),1))
dThetaTOu = np.zeros((len(L),1))
tauTO = np.zeros((len(L),1))
Faa = np.zeros((len(L),1))

num = np.zeros((len(L),1))
den = np.zeros((len(L),1))


dThetaTO[0] = 25
tauTO[0] = 5

for t in range(1,len(L)):
    
    K = L[t] / xfmrRating;

    dThetaTOu[t] = dThetaTOr*((((K**2)*R)+1)/(R+1))**n
    
    tauTO[t] = tauTOr * ((dThetaTOu[t]/dThetaTOr) - (dThetaTO[t-1]/dThetaTOr)) / ((dThetaTOu[t]/dThetaTOr)**(1/n) - (dThetaTO[t-1]/dThetaTOr)**(1/n))

    num[t] = ((dThetaTOu[t]/dThetaTOr) - (dThetaTO[t-1]/dThetaTOr));
    den[t] = ((dThetaTOu[t]/dThetaTOr)**(1/n) - (dThetaTO[t-1]/dThetaTOr)**(1/n));

    dThetaTO[t] = (dThetaTOu[t] - dThetaTO[t-1])*(1 - math.exp(-1/tauTO[t])) + dThetaTO[t-1]

    thetaH[t] = thetaA[t] + dThetaTO[t] + dThetaH

    Faa[t] = math.exp(((15000/383) - (15000/(thetaH[t] + 273))))

    print(t, Faa[t])

















