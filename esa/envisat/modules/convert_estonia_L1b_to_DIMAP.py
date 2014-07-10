#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: convert_estonia_L1b_to_DIMAP.py

#Konvertierung von .N1 nach dimap fuer Estland

import os.path
import os
import sys
from time import localtime, strftime, time

print("\n********************************************")
print(" Script \'get_estonia_L1b.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("********************************************\n")

def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

basepath='/fs14/EOservices/InputPool/MERIS/RR/waqs_child_temp_estonia/'
pconvertTool='/home/uwe/tools/beam-4.9/bin/pconvert.sh'
dimapDestDir='/fs14/EOservices/OutputPool/MERIS/RR/L1b-Estonia/'
n1destDir = '/fs14/EOservices/Repositories/MERIS/RR/temp_estonia/'

ensurePathExists(basepath)
ensurePathExists(dimapDestDir)
ensurePathExists(n1destDir)

logfilename = '/home/uwe/logs/pconvert_L1b_Estonia.log'
print(logfilename)

thetime   = localtime()
_year  = str(thetime[0])
_month = str(thetime[1])
_day   = str(thetime[2])
_hour  = str(thetime[3]) 
_minute= str(thetime[4])
_second= str(thetime[5])
 
if thetime[1] < 10:
    _month = "0"+ _month

if thetime[2] < 10:
    _day = "0"+ _day

datestring = _year + _month + _day + " " + _hour + ":" + _minute + ":" + _second

try:
    logfile = open(logfilename, 'a')
    logfile.write('\nat '+datestring+':\n')
except:
    print("unable to open the log file")
    sys.exit(1)

src_list = os.listdir(basepath)
list_size = len(src_list)

if not list_size:
    print("No files to process. Now quitting.")
    sys.exit(1)

src_list.sort()

filecounter=0
starttime=time()

for meris_file in src_list:     
    meris_file_path = basepath + meris_file
    
    if meris_file.startswith('MER_'):
        pconvertCommand = pconvertTool + " -f dim -o " + dimapDestDir + " " + meris_file_path
        
        print("Converting " + meris_file + " to DIMAP format..." + '\n')
        os.system(pconvertCommand)
        logfile.write(meris_file+'\n')             # erfolgreich prozessiertes file, logfile waechst mit
        filecounter += 1
        n1destPath = n1destDir + meris_file
        print('Moving N1 file to repository...')
        os.rename(meris_file_path, n1destPath)

endtime=time()
    
elapsed = endtime - starttime
logfile.write("Processed " + str(filecounter) + " files." +'\n')
logfile.close()

print("\n********************************************")
print(" Script \'get_estonia_L1b.py\' finished.  ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("********************************************\n")

#EOF
