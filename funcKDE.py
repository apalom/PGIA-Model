# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 16:43:39 2018

@author: Alex
"""

def funcKDE(dfHome, hr, numHomes):
    
    loadHr = dfHomeDay.iloc[hr]
    my_kde = st.gaussian_kde(loadHr)
    loadHrSample = my_kde.resample(numHomes)
    
    return (loadHrSample)