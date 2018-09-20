# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 16:29:21 2018

@author: Alex
"""
import scipy as sp
from scipy import stats as st
import matplotlib.pyplot as plt

maindat = dfHomeDay;


my_kde = st.gaussian_kde(maindat)
sample = my_kde.resample(10000)

x    = sp.linspace(sample[0,0], sample[0,-1],400)
fig  = plt.figure()
fig1 = fig.add_subplot(111)
plt.plot(x, my_kde(x),'b--')
plt.xlabel('Title Here ')
plt.show()