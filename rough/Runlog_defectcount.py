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
        # var1 = str(var)
        DClist.append(var[0])
        print (var[0])
    
print (count)

plt.plot(DClist)