# Defect count plotter
# This program reads defect count data from run log and plots defect count vs repeats
import re
import matplotlib.pyplot as plt
import json
import csv

fhand = open('Run.log', 'r')
fplot = open('defcount.csv', 'w')

count = 0
var1 = 0
DClist = []

for line in fhand:
    line = line.rstrip()
    var = re.findall('Defect Count: ([0-9]+)', line)
    if len(var) > 0:
        count = count+1
        DClist.append(var[0])
        print (var[0])
    
# Printing original list 
print (DClist) 
for i in range(0, len(DClist)): 
    DClist[i] = int(DClist[i]) 

# Printing modified list
print (DClist)
print (count)

plt.plot(DClist, marker = 'o', color= 'b')
plt.title('Defect Stability')
# improvement: Title can be auto selected to layer name from run log

plt.xlabel('Repeats') 
plt.ylabel('Count') 

plt.show(DClist)
