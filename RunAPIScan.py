import subprocess
import sys
import time


from subprocess import *

i = 0
total_scanners = 3 #number of scanners


procs = []
#should put some code to insert new rows into DB for latest dates.

for i in range (0,total_scanners):
    procs.append(Popen("cmd /k python APIScan.py "))

procs.append(Popen("cmd /k python Orchestrator.py "))

del procs[:]

print "All done"





