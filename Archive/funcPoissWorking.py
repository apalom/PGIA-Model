# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 09:23:51 2018

@author: Alex
"""

def funcPoiss(dfEV, maxEV, chgrRate, EVstoHomes):
    
    import numpy as np
    import random
    
    percentConnected = dfEV['Q3_max']
    numConnected = np.random.poisson(maxEV * percentConnected)
    
    numConnected = numConnected.clip(max = maxEV)

#%%    
    
    hr = 0
    
    homesPluggedDay = np.zeros((24,2))
    
    for num in numConnected:
        
        print('hr:  ', hr, '   num: ', num)
        
        i = 0

        homesPlugged = np.zeros(num)
        
        if num == 0:
            homesPlugged = np.zeros(len(EVstoHomes))
        
        elif num == 1:
        
            homesPlugged = np.random.permutation(num+1)[0:(num+1)]
            
        
        elif num > 1 and num < maxEV:
        
             while len(homesPlugged) != len(set(homesPlugged)):
            
                 for ev in range(num):
                
                    plugInto = np.random.permutation(num)[0:1][0] + 1                
                    homesPlugged[ev] = plugInto
                    i += 1            
                
                    if (i > 100):
                        homesPlugged = np.linspace(0,len(EVstoHomes)-1,len(EVstoHomes))
                        print('BREAK: homesPlugged: ' + str(homesPlugged))
                        break
                
        elif num == maxEV:
            homesPlugged = np.linspace(0, len(EVstoHomes)-1, len(EVstoHomes)) + 1
            
        print(str(i) + ': homesPlugged: ' + str(homesPlugged))
                
        homesPluggedDay[hr,:] = homesPlugged

        hr += 1
        
        
        

#%%
        
num = 

i = 0

homesPlugged = np.zeros(num)

while len(homesPlugged) != len(set(homesPlugged)):
    
    for ev in range(num):
    
        plugInto = np.random.permutation(num)[0:1][0]                
        homesPlugged[ev] = plugInto
        i += 1            
    
        if (i > 100):
            homesPlugged = np.linspace(0,len(EVstoHomes)-1,len(EVstoHomes))
            print('BREAK: homesPlugged: ' + str(homesPlugged))
            break
        
        
    print(str(i) + ': homesPlugged: ' + str(homesPlugged))

#%%
import timeit

# start timer 
timeMain = timeit.default_timer()
        
num = maxEV

homesPlugged = np.zeros(num)

i = 0

while len(homesPlugged) != len(set(homesPlugged)):
    for ev in range(num):
    
        plugInto = np.random.permutation(num)[0:1][0]
        
        homesPlugged[ev] = plugInto
        i += 1            

        if (i > 100):
            homesPlugged = np.linspace(0,len(EVstoHomes)-1,len(EVstoHomes))
            print('BREAK: homesPlugged: ' + str(homesPlugged))
            break
        
        elif (i <= 100):
            print(str(i) + ': homesPlugged: ' + str(homesPlugged))
                        
            #homeBus = EVstoHomes[plugInto]
            #print('homeBus:  ' + str(homeBus))
            
        #dfSys['Bus'].Pd.iloc[homeBus] = chgrRate
            
# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('homesPluggeed time: {0:.4f} sec'.format(elapsedMain))            
                
#%%    
    return (dfSys, numConnected)
    
