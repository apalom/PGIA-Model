# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 10:48:57 2019

@author: Alex Palomino
"""

# Organize Line Currents
import pandas as pd
import numpy as np

path1 = 'outputData\\1200\\0-'

#test = np.zeros((maxTrials*24,1))

# Plot F_aa Comparison
ampsL1 = pd.read_csv(path1 + 'outL1amp_1199.csv', header=None)
ampsL3 = pd.read_csv(path1 + 'outL3amp_1199.csv', header=None)
ampsL7 = pd.read_csv(path1 + 'outL7amp_1199.csv', header=None)


ampsL1_V = ampsL1.unstack();
ampsL3_V = ampsL3.unstack();
ampsL7_V = ampsL7.unstack();

data = pd.DataFrame({'L1': ampsL1_V.values, 
                     'L3': ampsL3_V.values,
                     'L7': ampsL7_V.values})


new = np.zeros((data.shape[0]*data.shape[1], 2))

tempDf = pd.DataFrame(new, columns = ['Case','Current']);

colNum = 0

for column in data:
    tempCol = data[column].values;
    tempLabel = column;

    stRow = colNum*len(data);
    enRow = colNum*len(data) + len(data);
    print(stRow, enRow, colNum)
    tempDf.Current.iloc[stRow:enRow] = tempCol;
    tempDf.Case.iloc[stRow:enRow] = tempLabel;
    colNum += 1;
    
data1 = tempDf;











