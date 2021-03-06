#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: make_WAQS_MERIS_childs_Estonia.py

import os
import os.path
import sys

print "\n***********************************************"
print " Script \'make_WAQS_MERIS_childs_Estonia.py\' at work... "
print "***********************************************\n"

def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
srcDir  = baseDir + 'DDSdownload/'
destDir = baseDir + 'waqs_child_temp_estonia/'

ensurePathExists(srcDir)
ensurePathExists(destDir)

childgenHome   = '/home/uwe/tools/geoChildgen1.3/'
childgenScript = childgenHome + 'geochildgen.sh'
childgenConf   = childgenHome + 'geochildgen_estland.properties'

src_list = os.listdir(srcDir)
list_size = len(src_list)

if list_size == 0:
    print "Nothing to do here. Now quitting."
    sys.exit(1)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 sind:
for a in range(list_size):
    for item in src_list:
        if not item.startswith('MER') or item.startswith('MER_RR__0') or item.startswith('MER_RR__2'):
            print "Removing " + item + " from list."
            src_list.remove(item)

src_list.sort()

for meris_file in src_list:    
    phys_meris_file = srcDir + meris_file
    
    # geoChildGen - Syntax:
    # ./geochildgen.sh ./geochildgen.properties -c -o <outDir> <product>
    childgenCommand = childgenScript + " -g " + childgenConf + " -c -o " + destDir + " " + phys_meris_file
    #print childgenCommand
    os.system(childgenCommand)

print "\n***********************************************"
print " Script \'make_WAQS_MERIS_childs_estonia.py\' finished.  "
print "***********************************************\n"

# EOF
