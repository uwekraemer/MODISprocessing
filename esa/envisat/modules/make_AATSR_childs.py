#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: make_AATSR_childs.py

from os import listdir, remove, system
from sys import argv, exit 

def printUsage():
    print("Usage: make_AATSR_childs.py type")
    print("where server includes:")
    print("\"NR\", or \"TOA\"\n")

try:
    argc=len(argv)
    if (argc == 1):          # the program was called without parameters
        print("Type specifier is missing!")
        printUsage()
        exit(1)
    else:                   # we have also received parameters
        if (argv[1] in ['NR', 'TOA']):
            typeID = argv[1]
            print("\nCreating AATSR " + typeID + " child products...")
        else:               # incorrect parameter
            print("Wrong type specifier!")
            printUsage()
            exit(1)
except:
    print("Error in parameters. Now exiting...")
    exit(1)    



baseDir = '/fs14/EOservices/InputPool/AATSR/' + typeID + '/'   # bcserver7
srcDir  = baseDir + 'RA_temp/'
waqs_destDir   = baseDir + 'waqs_child_temp/'
calval_destDir = baseDir + 'calval_child_temp/'

childgenHome   = '/home/uwe/tools/geoChildgen1.3/'            # bcserver7
#childgenHome   = '/uwe/tools/geoChildgen1.3/'        # bcG5
childgenScript = childgenHome + 'geochildgen.sh'
childgenConf   = childgenHome + 'geochildgen.properties'

old_childgenHome   = '/home/uwe/tools/geoChildGen/'            # bcserver7
#old_childgenHome   = '/uwe/tools/geoChildGen/'         # bcG5
old_childgenScript = old_childgenHome + 'geochildgen.sh'
old_childgenConf   = old_childgenHome + 'geochildgen.properties'

src_list = listdir(srcDir)
src_list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine aatsr-Produkte oder Level0 sind:
for src_count in range(src_list_size):
    for item in src_list:
        if item.startswith('ATS')==0:
            src_list.remove(item)

src_list_size = len(src_list)
if src_list_size == 0:
    print("Nothing to do here. Now quitting.\n")
    exit(1)

print("\n******************************************")
print(" Script \'make_AATSR_childs.py\' at work... ")
print("******************************************\n")

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

    if typeID == 'NR':
        waqs_childgenCommand   = childgenScript + " -g " + childgenConf + " -c -o " + waqs_destDir + " " + phys_aatsr_file_path
        print(waqs_childgenCommand)
        system(waqs_childgenCommand)

    calval_childgenCommand = childgenScript + " -d " + childgenConf + " -c -o " + calval_destDir + " " + phys_aatsr_file_path
    print(calval_childgenCommand)
    system(calval_childgenCommand)

    # Testen, ob der Quellorbit geloescht werden kann.
    # Annahme: wenn im Zielverzeichnis ein (child)-Produkt existiert,
    # wo das Akquisitionsdatum und der relative Orbit uebereinstimmen,
    # war das Erzeugen des child-Produkts erfolgreich.
    
    # Zuerst fuer waqs-Produkte:
    if typeID == 'NR':
        waqs_dest_list = listdir(waqs_destDir)
        waqs_dest_list_size = len(waqs_dest_list)
        for child in waqs_dest_list:
            if (child.find(acq_date)>0 and child.find(rel_orbit)>0):
                print("Child creation successful. Removing orbit " + phys_aatsr_file + " from source directory.")
                try:
                    remove(phys_aatsr_file_path)
                except:
                    print("\nCould not remove product. It has been already deleted by another process.\n")

    # Dann fuer calval-Produkte:
    calval_dest_list = listdir(calval_destDir)
    calval_dest_list_size = len(calval_dest_list)
    for child in calval_dest_list:
        if (child.find(acq_date)>0 and child.find(rel_orbit)>0):
            print("Child creation successful. Removing orbit " + phys_aatsr_file + " from source directory.")
            try:
                remove(phys_aatsr_file_path)
            except:
                print("\nCould not remove product. It has been already deleted by another process.\n")

print("\n******************************************")
print(" Script \'make_AATSR_childs.py\' finished.  ")
print("******************************************\n")

#EOF
