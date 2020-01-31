# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:13:25 2020

@author: Alex
"""

import numpy as np
from scipy import stats as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

lolData = pd.read_csv(r'outputData\50_kW_1200_AggDmd\Random EV-PV\4EV_4PV_12-9kW_rdm\LOL.csv')

my_kde = st.gaussian_kde(lolData['Loss Days'].values)
sample = my_kde.resample(1)[0][0]

#%% Plot CDF

sns.set(style="whitegrid", font='Times New Roman')
plt.figure(figsize=(12,8))

bns = np.arange(0,260,1)
#n, bins, patches = plt.hist(lolData.values, bins=bns, density=True, cumulative=True, alpha=0.75)
n, bins, patches = plt.hist(lolData.values, bins=bns, density=True, cumulative=False, alpha=0.90)

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')

#%% Plot data points

from scipy.optimize import curve_fit

def func(x, a, b, c):
     return a * np.exp(b * x) + c

xdata = np.arange(0,259,1); ydata = n;
popt, pcov = curve_fit(func, xdata, ydata)

sns.set(style="whitegrid", font='Times New Roman')

plt.plot(xdata, ydata, '.', markersize=1)

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')

#%% Fitting

p_Exp = st.expon.fit(lolData['Loss Days'].values)
p_Gam = st.gamma.fit(lolData['Loss Days'].values)
p_Norm = st.norm.fit(lolData['Loss Days'].values)
p_sNorm = st.skewnorm.fit(lolData['Loss Days'].values)

#plotting
rP_Exp = st.expon.pdf(xdata, *p_Exp)
rP_Gam = st.gamma.pdf(xdata, *p_Gam)
rP_Norm = st.norm.pdf(xdata, *p_Norm)
rP_sNorm = st.skewnorm.pdf(xdata, *p_sNorm)

plt.figure(figsize=(12,8))

bns = np.arange(0,260,10)
#n, bins, patches = plt.hist(lolData.values, bins=bns, density=True, cumulative=True, alpha=0.75)
plt.hist(lolData.values, bins=bns, density=True, cumulative=False, alpha=0.60, label='Data')
plt.plot(xdata, rP_Exp, alpha=0.90, label='Exponential Fit')
plt.plot(xdata, rP_Gam, alpha=0.90, label='Gamma Fit')
plt.plot(xdata, rP_Norm, alpha=0.90, label='Norm Fit')
plt.plot(xdata, rP_sNorm, alpha=0.90, label='Skew Norm Fit')

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')

plt.legend()

