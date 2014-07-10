#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: make_WAQS_AATSR_childs.py

import os
import os.path
import sys

print("\n***********************************************")
print(" Script \'make_WAQS_AATSR_childs.py\' at work... ")
print("***********************************************\n")

baseDir = '/fs14/EOservices/InputPool/AATSR/NR/'
srcDir  = baseDir + 'RA_temp/'
destDir = baseDir + 'waqs_child_temp/'
childgenHome   = '/home/uwe/tools/geoChildgen1.3/'
childgenScript = childgenHome + 'geochildgen.sh'
childgenConf   = childgenHome + 'geochildgen.properties'

src_list = os.listdir(srcDir)
src_list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine aatsr-Produkte oder Level0 sind:
for src_count in range(src_list_size):
    for item in src_list:
        if item.startswith('ATS')==0:
            src_list.remove(item)

src_list_size = len(src_list)

if src_list_size == 0:
    print("Nothing to do here. Now quitting.")
    sys.exit(1)

for aatsr_file_count in range(src_list_size):
    # ATS_NR__2PNMAP20060501_100612_000003362047_00194_21791_0001.N1
    # 0         1         2         3         4         5         6
    # 01234567890123456789012345678901234567890123456789012345678901
    phys_aatsr_file = src_list[aatsr_file_count]
    acq_date  = phys_aatsr_file[14:22]           # Bsp: 20060501
    rel_orbit = phys_aatsr_file[42:49]           # Bsp: _00194_
    
    phys_aatsr_file_path = srcDir + phys_aatsr_file
    
    # geoChildGen - Syntax:
    # ./geochildgen.sh ./geochildgen.properties -c -o <outDir> <product>
        
    childgenCommand = childgenScript + " -g " + childgenConf + " -c -o " + destDir + " " + phys_aatsr_file_path
    os.system(childgenCommand)

    # Testen, ob der Quellorbit geloescht werden kann.
    # Annahme: wenn im Zielverzeichnis ein (child)-Produkt existiert,
    # wo das Akquisitionsdatum und der relative Orbit uebereinstimmen,
    # war das Erzeugen des child-Produkts erfolgreich. 
    dest_list = os.listdir(destDir)
    dest_list_size = len(dest_list)
    for child in dest_list:
        if (child.find(acq_date)>0 and child.find(rel_orbit)>0):
            print("Child creation successful. Removing orbit " + phys_aatsr_file + " from source directory.")
            os.remove(phys_aatsr_file_path)

print("\n***********************************************")
print(" Script \'make_WAQS_AATSR_childs.py\' finished.  ")
print("***********************************************\n")

#EOF
