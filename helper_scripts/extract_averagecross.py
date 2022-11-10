#this script will extract sequences based on the chimera library schema generates
#it requires, crossover containing file (should be only one line), multiple sequence alignment file, chimerafile

import sys
import statistics

optfile=open(sys.argv[1],'r')
outputfile=open("Average_xo.txt",'w')
crosspoint=[]

for line in optfile:
    line_split=line.strip().split()
    if not '#' in line:
        crosspoint.append(line_split)
median_e=statistics.median(float(crosspoint[x][0]) for x in range(0,len(crosspoint)))
for y in range(0,len(crosspoint)):
    if float(median_e) == float(crosspoint[y][0]):
#        print(float(median_e), ' and ', float(crosspoint[y][0]), ' l ', y)
        xopoint=" ".join(str(crosspoint[y][t]) for t in range(2, len(crosspoint[y])))
        outputfile.write(xopoint+'\n')
#        print(xopoint, " crospoint ",crosspoint[y][2:])
        break
