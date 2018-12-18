# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

df = pd.read_excel(r'C:\Users\Alex Palomino\Documents\GitHub\PGIA-Model\data\starPlot.xlsx', sheet_name=None, header=0)

# number of variable
categories=list(df)[1:]
N = len(categories)
 
# We are going to plot the first line of the data frame.
# But we need to repeat the first value to close the circular graph:
profile = 4;
values=df.loc[profile].drop('Label').values.flatten().tolist()
values += values[:1]

 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
 
# Initialise the spider plot
ax = plt.subplot(111, polar=True)
 
# Draw one axe per variable + add labels labels yet
locs, labels = plt.xticks(angles[:-1], categories, color='black', size=12)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([1,2,3,4], ["1","2","3","4"], color="grey", size=7)
plt.ylim(0,4)
 
# Plot data
plt.title(df.Label[profile], size=16)
ax.plot(angles, values, linewidth=1, linestyle='solid')
 
# Fill area
ax.fill(angles, values, 'b', alpha=0.1)
