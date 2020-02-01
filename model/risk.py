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

sns.set(style="whitegrid", font='Times New Roman', font_scale=1.5)
#plt.figure(figsize=(12,8))

bns = np.arange(0,np.max(lolData.values),1)
n, bins, patches = plt.hist(lolData.values, bins=bns, density=True, cumulative=True, alpha=0.90)
#plt.plot(bns, n)

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')

#%% Test Day Value

T_left = 3500; # 3500 days left of life
t_until = 3500; # 90 days until replacement

dayRatio = int(np.ceil(T_left/t_until)); # What is the prob that you lose dayRatio days before next service? 

if dayRatio > len(n):
    print("\nProbability of failure before next service: \n 0.00")
else:
    fail_prob = n[dayRatio]
    print("\nProbability of failure before next service: \n", np.round(fail_prob,4))   

#%% Plot data points

from scipy.optimize import curve_fit

def func(x, a, b, c):
     return a * np.exp(b * x) + c

xdata = np.arange(0,259,1); ydata = n;
popt, pcov = curve_fit(func, xdata, ydata)

sns.set(style="whitegrid", font='Times New Roman')

plt.plot(xdata, ydata, '.', markersize=3)

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')

#%% Fitting

x0 = np.linspace(0,260,261)
p_Exp = st.expon.fit(lolData['Loss Days'].values)
p_Gam = st.gamma.fit(lolData['Loss Days'].values)
p_Norm = st.norm.fit(lolData['Loss Days'].values)
p_sNorm = st.skewnorm.fit(lolData['Loss Days'].values)
p_WeiMin = st.weibull_min.fit(lolData['Loss Days'].values)

#plotting
rP_Exp = st.expon.pdf(x0, *p_Exp)
rP_Gam = st.gamma.pdf(x0, *p_Gam)
rP_Norm = st.norm.pdf(x0, *p_Norm)
rP_sNorm = st.skewnorm.pdf(x0, *p_sNorm)
rp_WeiMin = st.weibull_min.pdf(x0, *p_WeiMin)

plt.figure(figsize=(12,8))

bns = np.arange(0,260,1)
#n, bins, patches = plt.hist(lolData.values, bins=bns, density=True, cumulative=True, alpha=0.75)
plt.hist(lolData.values, bins=bns, density=True, cumulative=False, alpha=0.60, label='Data')
plt.plot(x0, rP_Exp, alpha=0.90, label='Exponential Fit')
plt.plot(x0, rP_Gam, alpha=0.90, label='Gamma Fit')
plt.plot(x0, rP_Norm, alpha=0.90, label='Norm Fit')
plt.plot(x0, rP_sNorm, alpha=0.90, label='Skew Norm Fit')
plt.plot(x0, rp_WeiMin, alpha=0.90, label='Weibull Min Fit')

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')

plt.legend()

#%% KS Test

print('\nExpon: ', st.kstest(lolData['Loss Days'].values,'expon', args=(p_Exp)))
print('Gamma: ', st.kstest(lolData['Loss Days'].values,'gamma', args=(p_Gam)))
print('Skew Norm: ', st.kstest(lolData['Loss Days'].values,'skewnorm', args=(p_sNorm)))
print('Weibull: ', st.kstest(lolData['Loss Days'].values,'weibull_min', args=(p_WeiMin)))

#%%

rP_Gam = st.gamma.pdf(x0, *p_Gam)
c , p = st.chisquare(lolData['Loss Days'].values, rP_Gam, ddof=len(p_Gam))