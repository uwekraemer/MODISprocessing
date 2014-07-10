#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: make_CalVal_MERIS_childs.py

import os
import os.path
import sys

print("\n*************************************************")
print(" Script \'make_CalVal_MERIS_childs.py\' at work... ")
print("*************************************************\n")

#baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
#baseDir = '/fs14/EOservices/InputPool/AATSR/NR/'
baseDir = '/fs14/EOservices/InputPool/AATSR/TOA/'

srcDir  = baseDir + 'calval_child_temp/'
destDir = baseDir + 'calval_child_temp_temp/'
childgenHome   = '/home/uwe/tools/geoChildgen1.6/'
childgenScript = childgenHome + 'geochildgen.sh'
childgenConf   = childgenHome + 'geochildgen.properties'

print('Getting file listing...')
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS- oder AATSR-Produkte sind:
print('Removing wrong input from list...')
for a in range(list_size):
    for item in src_list:
        if not (item.startswith('MER') or item.startswith('ATS')):
            #print "Removing " + item + " from list."
            src_list.remove(item)

list_size = len(src_list)
if list_size ==0:
    print("Nothing to do here. Now quitting.")
    sys.exit(1)

for meris_file in src_list:    
    year  = meris_file[14:18]
    
    phys_meris_file = srcDir + meris_file
    
    # geoChildGen - Syntax:
    # ./geochildgen.sh ./geochildgen.properties -c -o <outDir> <product>
        
    childgenCommand = childgenScript + " -d " + childgenConf + " -o " + destDir + " " + phys_meris_file
    print(childgenCommand)
    os.system(childgenCommand)

print("\n*************************************************")
print(" Script \'make_CalVal_MERIS_childs.py\' finished.  ")
print("*************************************************\n")

# EOF
