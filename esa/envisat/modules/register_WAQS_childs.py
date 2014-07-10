#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: register_WAQS_childs.py

import os
import os.path
import sys
import time

def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

print("\n*********************************************")
print(" Script \'register_WAQS_childs.py\' at work... ")
print("*********************************************\n")

thetime   = time.localtime()
year_str  = str(thetime[0]) + "/"

baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
srcDir  = baseDir + 'waqs_child_temp/'
#srcDir  = baseDir + 'backlog/'
destDir = '/fs14/EOservices/Repositories/MERIS/RR/WAQSrepository/'
ensurePathExists(destDir)

prodregHome   = '/home/uwe/tools/prodreg1.3/'
prodregScript = prodregHome + 'prodreg.sh'
prodregConf   = prodregHome + 'config_waqs.properties'

src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 sind:
for a in range(list_size):
    for item in src_list:
        if item.startswith('MER')==0 or item.startswith('MER_RR__0')==1:
            #print "Removing " + item + " from list."
            src_list.remove(item)

for meris_file in src_list:    
    year  = meris_file[14:18]
    
    destPath = destDir  + year + '/'
    ql_path  = destPath + 'ql/'
    tn_path  = destPath + 'tn/'
    phys_meris_file = srcDir + meris_file
    
    if not os.path.exists(destPath): # wenn Jahr noch nicht existiert
        os.makedirs(ql_path, 0o777)
        os.makedirs(tn_path, 0o777)
        print("year nicht")
    
    # prodreg-Syntax:
    # ./prodreg.sh -c config_dds.properties -e -m -q -t -s DDS -o <outputDir> <products>    
    prodregCommand = prodregScript + " -c " + prodregConf + " -e -m -q -t -s WAQS -o " + year + " " + phys_meris_file
    print(prodregCommand)
    os.system(prodregCommand)

print("\n*********************************************")
print(" Script \'register_WAQS_childs.py\' finished. ")
print("*********************************************\n")

# EOF
