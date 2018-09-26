# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 16:43:39 2018

@author: Alex
"""

def funcKDE(dfSys, dfHomeDay, hr, numHomes):
    
    from scipy import stats as st
    
    samplekWpHr = dfHomeDay.iloc[hr]
    my_kde = st.gaussian_kde(samplekWpHr)
    samplekWpHr = my_kde.resample(numHomes)
    samplekWpHr = samplekWpHr.clip(min = 0)
    samplekVARpHr = 0.62*samplekWpHr
    
    dfSys['Bus'].Pd = samplekWpHr[0][:]
    dfSys['Bus'].Qd = samplekVARpHr[0][:]
    
    return (dfSys, samplekWpHr, samplekVARpHr)