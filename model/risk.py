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

lolData00 = pd.read_csv(r'outputData\50_kW_1200_AggDmd\Base_Case\LOL.csv')
lolData40 = pd.read_csv(r'outputData\50_kW_1200_AggDmd\EV Set\4EV_0PV_12-9kW_set\LOL.csv')
lolData44 = pd.read_csv(r'outputData\50_kW_1200_AggDmd\Random EV-PV\4EV_4PV_12-9kW_rdm\LOL.csv')
lolData80 = pd.read_csv(r'outputData\50_kW_1200_AggDmd\EV Set\8EV_0PV_12-9kW_set\LOL.csv')
lolData88 = pd.read_csv(r'outputData\50_kW_1200_AggDmd\Random EV-PV\8EV_8PV_12-9kW_rdm\LOL.csv')

#my_kde = st.gaussian_kde(lolData['Loss Days'].values)
#sample = my_kde.resample(1)[0][0]

#%%

bns = np.arange(0,2000,1);
n00, _, _ = plt.hist(lolData00.values, bins=bns, density=True, cumulative=True, fc='b', ec='b')
n40, _, _ = plt.hist(lolData40.values, bins=bns, density=True, cumulative=True, alpha=0.50)
n44, _, _ = plt.hist(lolData44.values, bins=bns, density=True, cumulative=True, alpha=0.50)
n80, _, _ = plt.hist(lolData80.values, bins=bns, density=True, cumulative=True, alpha=0.50)
n88, _, _ = plt.hist(lolData88.values, bins=bns, density=True, cumulative=True, alpha=0.50)
daysCDF = np.array([n00, n40, n44, n80, n88]).T

#%% Output LoL CDF

sns.set(style="whitegrid", font='Times New Roman', font_scale=1.5)
f = plt.figure(figsize=(8,6))

x = np.arange(0,len(bns)-1,1)
plt.plot(x, n00, label='Base')
plt.plot(x, n40, label='40')
plt.plot(x, n44, label='44')
plt.plot(x, n80, label='80')
plt.plot(x, n88, label='88')

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')
plt.legend()

f.savefig("cdf_LoL1.pdf", bbox_inches='tight')

#%% Plot CDF

sns.set(style="whitegrid", font='Times New Roman', font_scale=1.5)
f = plt.figure(figsize=(12,8))

bns=500;
n, bins, patches = plt.hist(lolData44.values, bins=bns, density=True, cumulative=True, alpha=0.90)
#plt.plot(bns, n)

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')

#%% Test Day Value

T_left = 3500; # 3500 days left of life
t_until = 100; # 90 days until replacement

#dayRatio = int(np.ceil(T_left/t_until)); 
dayRatio = int((T_left/t_until)); # What is the prob that you lose dayRatio days before next service? 

if dayRatio >= len(n44):
    print("\nProbability of failure before next service: \n 0.00")
else:
    fail_prob = 1 - n44[dayRatio]
    #print(fail_prob**t_until*100)
    print("\nProbability of failure before next service: \n", np.round(fail_prob,4))   

#%%
import random

T_left = 3500; # 3500 days left of life
t_until = 10; # 90 days until replacement

my_kde = st.gaussian_kde(lolData44['Loss Days'].values)

daysLost = 0;
fail_prob = 1 - n;    
for d in range(t_until):
        
    daysLost += np.clip(int(my_kde.resample(1)[0][0]), a_min=0, a_max=np.max(lolData.values));

if daysLost >= T_left:
    print("\nTransformer Failed")
else:
    daysLeft = int(T_left-daysLost)
    print("\nTransformer has "+str(daysLeft)+" days left.")    

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

sns.set(style="whitegrid", font='Times New Roman', font_scale=1.5)
lolData = pd.read_csv(r'outputData\50_kW_1200_AggDmd\Random EV-PV\4EV_4PV_12-9kW_rdm\LOL.csv')

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

bns = np.arange(0,262,1)
#n, bins, patches = plt.hist(lolData.values, bins=bns, density=True, cumulative=True, alpha=0.75)
n, bins, patches = plt.hist(lolData.values, bins=bns, density=True, cumulative=False, alpha=0.60, label='Data')
plt.plot(x0, rP_Exp, alpha=0.90, label='Exponential Fit')
plt.plot(x0, rP_Gam, alpha=0.90, label='Gamma Fit')
plt.plot(x0, rP_Norm, alpha=0.90, label='Norm Fit')
plt.plot(x0, rP_sNorm, alpha=0.90, label='Skew Norm Fit')
plt.plot(x0, rp_WeiMin, alpha=0.90, label='Weibull Min Fit')

plt.title('Loss-of-Life Distribution')
plt.ylabel('Likelihood')
plt.xlabel('Days')

plt.legend()

#%% Calculate RMSE

from sklearn.metrics import mean_squared_error
from math import sqrt

rms = sqrt(mean_squared_error(n, rP_Gam))
print(rms)

#%% KS Test

print('\nExpon: ', st.kstest(lolData['Loss Days'].values,'expon', args=(p_Exp)))
print('Gamma: ', st.kstest(lolData['Loss Days'].values,'gamma', args=(p_Gam)))
print('Skew Norm: ', st.kstest(lolData['Loss Days'].values,'skewnorm', args=(p_sNorm)))
print('Weibull: ', st.kstest(lolData['Loss Days'].values,'weibull_min', args=(p_WeiMin)))

#%%

rP_Gam = st.gamma.pdf(x0, *p_Gam)
c , p = st.chisquare(lolData['Loss Days'].values, rP_Gam, ddof=len(p_Gam))