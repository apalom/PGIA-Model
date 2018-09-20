# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 16:29:21 2018

@author: Alex
"""
import scipy as sp
from scipy import stats as st
import matplotlib.pyplot as plt

maindat = dfHomeDay;

hr = 3;

maindat = maindat.iloc[hr]
my_kde = st.gaussian_kde(maindat)
sample = my_kde.resample(5000)

#x    = sp.linspace(sample[0,0], sample[0,-1], 400)
x    = sp.linspace(0, 10, 100)
fig  = plt.figure()
fig1 = fig.add_subplot(111)
plt.plot(x, my_kde(x),'b--')
plt.hist(sample, density=True, facecolor='blue', alpha=0.2)
plt.xlabel('Title Here ')
plt.xlim(0, 10)
plt.show()