#!/usr/bin/env python
# -*- coding: latin-1 -*-
# file: remerge_netCDF_products.py

import os
import os.path
import sys
import time
from shutil import rmtree

def printUsage():
    print("Usage: remerge_netCDF_products.py start_date end_date")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date")
    

try:
    argc=len(sys.argv)
    if argc < 3:          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        start_date = sys.argv[1]
        end_date   = sys.argv[2]
        if int(start_date) <= int(end_date):
            # do something
            print("\nReprocessing products from " + start_date + " to " + end_date + "...\n")
        else:               # incorrect parameters
            print("Wrong parameters!")
            printUsage()
            sys.exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)    



print("\n************************************************")
print(" Script \'remerge_netCDF_products.py\' at work... ")
print("************************************************\n")

srcDir='/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily/'
bandArithTool='/home/uwe/tools/BandArithBatch/BandArithBatch.sh'
patchTool='/home/uwe/tools/patchTool/patchTool.sh'
destDir='/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/'

for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)
    print(date)    
    src_list = os.listdir(srcDir)
    list_size = len(src_list)
    
    for a in range(list_size):
        for item in src_list:
            if item.endswith('___0000.data')==1 or item.startswith('L3_ENV_MER_')==0 or item.find(date)==-1:
                #print "Removing " + item + " from list."
                src_list.remove(item)
    
    print('\nsrc_list=', src_list)
    if len(src_list) == 0:
        print('Nothing to do. Continuing...')
        continue
    
    # dummy arrays
    northSeaDummyList   = ['a','b','c','d']
    northSeaList        = ['e','f','g','h']
    
    balticSeaDummyList  = ['i','j','k','l']
    balticSeaList       = ['m','n','o','p']
    
    northSeaCount  = 0
    balticSeaCount = 0
    
    list_size = len(src_list)
    
    for item in range(list_size):
        if src_list[item].find('NSEA')>0:
            #print northSeaCount
            #print "Adding file " + src_list[item] + " to North Sea list..."
            northSeaDummyList[northSeaCount] = srcDir + src_list[item]
            northSeaCount += 1
        elif src_list[item].find('BALTIC')>0:
            #print balticSeaCount
            #print "Adding file " + src_list[item] + " to Baltic Sea list..."
            balticSeaDummyList[balticSeaCount] = srcDir + src_list[item]
            balticSeaCount += 1
    
    # Listen durchsortieren, damit eine feste Reihenfolge
    # von Produkten vorliegt, und zwar so: chl12, spm, ys, tr
    
    for count in range(4):
        if northSeaDummyList[count].find('_CHL12_')>0:
            northSeaList[0] = northSeaDummyList[count]
        elif northSeaDummyList[count].find('_SPM_')>0:
            northSeaList[1] = northSeaDummyList[count]
        elif northSeaDummyList[count].find('_YS_')>0:
            northSeaList[2] = northSeaDummyList[count]
        elif northSeaDummyList[count].find('_TR')>0:
            northSeaList[3] = northSeaDummyList[count]
    
    for count in range(4):
        if balticSeaDummyList[count].find('_CHL12_')>0:
            balticSeaList[0] = balticSeaDummyList[count]
        elif balticSeaDummyList[count].find('_SPM_')>0:
            balticSeaList[1] = balticSeaDummyList[count]
        elif balticSeaDummyList[count].find('_YS_')>0:
            balticSeaList[2] = balticSeaDummyList[count]
        elif balticSeaDummyList[count].find('_TR')>0:
            balticSeaList[3] = balticSeaDummyList[count]
    
    northSeaOutputproduct  = destDir + 'L3_ENV_MER_' + date + '_NSEA_PC_ACR___0000.dim'
    northSeaOutputData     = destDir + 'L3_ENV_MER_' + date + '_NSEA_PC_ACR___0000.data'
    balticSeaOutputproduct = destDir + 'L3_ENV_MER_' + date + '_BALTIC_PC_ACR___0000.dim'
    balticSeaOutputData    = destDir + 'L3_ENV_MER_' + date + '_BALTIC_PC_ACR___0000.data'
    
    print("northSeaOutputproduct: "  + northSeaOutputproduct)
    print("balticSeaOutputproduct: " + balticSeaOutputproduct)
    
    
    # zuerst die CHL12-Produkte als Zielprodukt fuer Bandarithmetik kopieren:
    
    northSeaDataDirectory  = northSeaList[0][0:len(northSeaList[0])-2] + "ata"
    if os.path.exists(northSeaOutputData):
        print("Deleting " + northSeaOutputData + " directory...")
        rmtree(northSeaOutputData)
    northSeaCopyDataCommand = "cp -rf " + northSeaDataDirectory + "* " + northSeaOutputData
    
    balticSeaDataDirectory  = balticSeaList[0][0:len(balticSeaList[0])-2] + "ata"
    if os.path.exists(balticSeaOutputData):
        print("Deleting " + balticSeaOutputData + " directory...")
        rmtree(balticSeaOutputData)
    balticSeaCopyDataCommand = "cp -rf " + balticSeaDataDirectory + "* " + balticSeaOutputData
    
    os.system(northSeaCopyDataCommand)
    os.system(balticSeaCopyDataCommand)
    
    # dann in den .dim-files die Namen korrigieren:
    # sed syntax:
    # sed -e "s/_CHL12_j__/_/" <file>
    
    northSeaSedCommand  = "sed -e \"s/_CHL12_j__/_/\" " + northSeaList[0] + " > "  + northSeaOutputproduct
    balticSeaSedCommand = "sed -e \"s/_CHL12_j__/_/\" " + balticSeaList[0] + " > " + balticSeaOutputproduct
    os.system(northSeaSedCommand)
    os.system(balticSeaSedCommand)
    
    bands = ['sea_suspended_matter', 'yellow_substance', 'transparency']
    print("\n") 
    print(northSeaList)
    print("\n") 
    print(balticSeaList)
    
    # bandarith batch syntax:
    #<productName> [-d <destProductName>]<bandName> <expression> [<bandName> <expression>]
    
    # Hier werden die fehlenden drei Baender in das produkt kopiert.
    # Falls Baender fehlen sollten, werden sie als virtuelle Baender
    # nachtraeglich mit dem patchTool angelegt (siehe weiter unten)
    for count in range(3):
        northSeaCommand  = bandArithTool + " " + northSeaList[count+1] + " -d "  + northSeaOutputproduct  + " " + bands[count] + " \"" + bands[count] + "\""
        balticSeaCommand = bandArithTool + " " + balticSeaList[count+1] + " -d " + balticSeaOutputproduct + " " + bands[count] + " \"" + bands[count] + "\""
        os.system(northSeaCommand)
        os.system(balticSeaCommand)
    
    # Jetzt kommt noch das patchTool, damit die Produkte in jedem Fall komplett sind
    patchNorthSeaCommand  = patchTool + " " + northSeaOutputproduct
    os.system(patchNorthSeaCommand)
    patchBalticSeaCommand = patchTool + " " + balticSeaOutputproduct
    os.system(patchBalticSeaCommand)
    
print("\n***********************************************")
print(" Script \'remerge_netCDF_products.py\' finished. ")
print("***********************************************\n")
    
#EOF
