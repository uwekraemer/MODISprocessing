#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: register_DDS_orbits.py

import os
import os.path
import sys
import time

print "\n********************************************"
print " Script \'register_DDS_orbits.py\' at work... "
print "********************************************\n"

baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
srcDir  = baseDir + 'DDSdownload/'
destDir = '/fs14/EOservices/Repositories/MERIS/RR/DDSrepository/'

prodregHome   = '/home/uwe/tools/prodreg/'
prodregScript = prodregHome + 'prodreg.sh'
prodregConf   = prodregHome + 'config_dds.properties'

src_list = os.listdir(srcDir)
list_size = len(src_list)

thetime   = time.localtime()
year_str  = str(thetime[0])
month_str = str(thetime[1])
day_str   = str(thetime[2])

if thetime[1] < 10:
    month_str = "0"+ month_str

if thetime[2] < 10:
    day_str = "0"+ day_str

datestring = year_str + month_str + day_str

# Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 sind:
for a in range(list_size):
    for item in src_list:
        if item.startswith('MER')==0 or item.startswith('MER_RR__0')==1:
            #print "Removing " + item + " from list."
            src_list.remove(item)


for meris_file in src_list:    
    year  = meris_file[14:18]
    month = meris_file[18:20]
    
    destPath = destDir + year + "/" + month
    phys_meris_file = srcDir + meris_file
    #print destPath, phys_meris_file
    
    if not os.path.exists(destDir + year):     #wenn Jahr noch nicht existiert
        os.mkdir(destDir + year)               #directory year
        os.mkdir(destDir + year + "/"+month)   #directory month
        print "year nicht"
    elif not os.path.exists(destDir + year + "/" + month):     # wenn Monat noch nicht existiert
        os.mkdir(destDir + year + "/" + month)
        print "month nicht"
    
    # prodreg-Syntax:
    # ./prodreg.sh -c config_dds.properties -m -q -t -s DDS -o <outputDir> <products>    
    prodregCommand = prodregScript + " -c " + prodregConf + " -m -q -t -s DDS" + datestring +" -o " + year + "/" + month + " " + phys_meris_file
    #print prodregCommand
    os.system(prodregCommand)

print "\n********************************************"
print " Script \'register_DDS_orbits.py\' finished. "
print "********************************************\n"

# EOF
