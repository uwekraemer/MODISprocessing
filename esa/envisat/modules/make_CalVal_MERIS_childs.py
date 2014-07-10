#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: make_CalVal_MERIS_childs.py

import os
import os.path
import sys

def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
srcDir  = baseDir + 'DDSdownload/'
destDir = baseDir + 'calval_child_temp/'

ensurePathExists(destDir)

childgenHome   = '/home/uwe/tools/geoChildgen1.3/'
childgenScript = childgenHome + 'geochildgen.sh'
childgenConf   = childgenHome + 'geochildgen.properties'

src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 sind:
for a in range(list_size):
    for item in src_list:
        if item.startswith('MER')==0 or item.startswith('MER_RR__0')==1:
            #print "Removing " + item + " from list."
            src_list.remove(item)

list_size = len(src_list)
if list_size ==0:
    print("Nothing to do here. Now quitting.")
    sys.exit(1)

print("\n*************************************************")
print(" Script \'make_CalVal_MERIS_childs.py\' at work... ")
print("*************************************************\n")

for meris_file in src_list:    
    year  = meris_file[14:18]
    
    phys_meris_file = srcDir + meris_file
    
    # geoChildGen - Syntax:
    # ./geochildgen.sh ./geochildgen.properties -c -o <outDir> <product>
        
    childgenCommand = childgenScript + " -d " + childgenConf + " -c -o " + destDir + " " + phys_meris_file
    print(childgenCommand)
    os.system(childgenCommand)

print("\n*************************************************")
print(" Script \'make_CalVal_MERIS_childs.py\' finished.  ")
print("*************************************************\n")

# EOF
