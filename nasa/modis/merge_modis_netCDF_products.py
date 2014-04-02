#!/usr/bin/env python
# -*- coding: latin-1 -*-
# file: merge_netCDF_products.py

import os.path
from os import listdir,system
from sys import argv, exit
import time

def printUsage():
    print("Usage: merge_modis_netCDF_products.py back_day")
    print("where back_day is an integer value specifying the start day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

argc=len(argv)
if argc < 2:          # the program was called incorrectly
    print("\nToo few parameters passed!")
    printUsage()
    exit(1)

try:
    backDay = int(argv[1])
except TypeError:
    print("back_day parameter must be of type integer!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    exit(1)

today = time.localtime()

# Einige nuetzliche Funktionen:
def get_float_day(day):
    secs_per_day  = 24*60*60
    return time.mktime(today)-day*secs_per_day


def get_date_string(float_day):
    date  = time.localtime(float_day)
    year  = str(date[0])
    month = str(date[1])
    day   = str(date[2])
    if date[1] <10:
        month = "0" + str(date[1])
    if date[2] <10:
        day   = "0" + str(date[2])
    return year + month + day

print("\n****************************************************")
print(" Script \'merge_modis_netCDF_products.py\' at work... ")
print("****************************************************\n")

#L3_MOD_AQU_CHLA_j__20120412_NSEA_PC_ACR___0000
srcDir='/fs14/EOservices/OutputPool/MODIS/WAQS-MC/daily/'

destDir='/fs14/EOservices/OutputPool/MODIS/WAQS-MC/daily-merged/'

bandArithTool='/home/uwe/tools/BandArithBatch/BandArithBatch.sh'
patchTool='/home/uwe/tools/patchTool/patchTool.sh'

_year  = str(today[0])
_month = str(today[1]).zfill(2)
_day   = str(today[2]).zfill(2)
_hour  = str(today[3]).zfill(2)
_minute= str(today[4]).zfill(2)
_second= str(today[5]).zfill(2)
 
#datestring = _year + _month + _day + " " + _hour + ":" + _minute + ":" + _second

# Dateien werden mit dem Datum von vorgestern verarbeitet

arrival_day=get_date_string(get_float_day(backDay))
myDate = arrival_day
#myDate =  _year + _month + _day
#myDate = '20060605'

src_list = listdir(srcDir)
list_size = len(src_list)

for a in range(list_size):
    for item in src_list:
        if item.endswith('___0000.data')==1 or item.startswith('L3_MOD_AQU_')==0 or item.find(myDate)==-1:
            #print "Removing " + item + " from list."
            src_list.remove(item)

print('\nsrc_list=', src_list)
if not len(src_list):
    print('Nothing to do. Now exiting...')
    exit(1)

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
    if northSeaDummyList[count].find('_CHLA_')>0:
        northSeaList[0] = northSeaDummyList[count]
    elif northSeaDummyList[count].find('_SPM_')>0:
        northSeaList[1] = northSeaDummyList[count]
    elif northSeaDummyList[count].find('_YS_')>0:
        northSeaList[2] = northSeaDummyList[count]
    elif northSeaDummyList[count].find('_TR')>0:
        northSeaList[3] = northSeaDummyList[count]

for count in range(4):
    if balticSeaDummyList[count].find('_CHLA_')>0:
        balticSeaList[0] = balticSeaDummyList[count]
    elif balticSeaDummyList[count].find('_SPM_')>0:
        balticSeaList[1] = balticSeaDummyList[count]
    elif balticSeaDummyList[count].find('_YS_')>0:
        balticSeaList[2] = balticSeaDummyList[count]
    elif balticSeaDummyList[count].find('_TR')>0:
        balticSeaList[3] = balticSeaDummyList[count]

#L3_MOD_AQU_20120412_NSEA_PC_ACR___0000
northSeaOutputproduct  = destDir + 'L3_MOD_AQU_' + myDate + '_NSEA_PC_ACR___0000.dim'
northSeaOutputData     = northSeaOutputproduct[:-2]+'ata'

balticSeaOutputproduct = destDir + 'L3_MOD_AQU_' + myDate + '_BALTIC_PC_ACR___0000.dim'
balticSeaOutputData    = balticSeaOutputproduct[:-2]+'ata'

print("northSeaOutputproduct: "  + northSeaOutputproduct)
print("balticSeaOutputproduct: " + balticSeaOutputproduct)

# zuerst die CHL12-Produkte als Zielprodukt fuer Bandarithmetik kopieren:

northSeaDataDirectory   = northSeaList[0][0:len(northSeaList[0])-2] + "ata"
northSeaCopyDataCommand = "cp -rf " + northSeaDataDirectory + " " + northSeaOutputData
print(northSeaCopyDataCommand)

balticSeaDataDirectory   = balticSeaList[0][0:len(balticSeaList[0])-2] + "ata"
balticSeaCopyDataCommand = "cp -rf " + balticSeaDataDirectory + " " + balticSeaOutputData
print(balticSeaCopyDataCommand)

system(northSeaCopyDataCommand)
system(balticSeaCopyDataCommand)

# dann in den .dim-files die Namen korrigieren:
# sed syntax:
# sed -e "s/_CHL12_j__/_/" <file>

northSeaSedCommand  = "sed -e \"s/_CHLA_j__/_/\" " + northSeaList[0] + " > "  + northSeaOutputproduct
balticSeaSedCommand = "sed -e \"s/_CHLA_j__/_/\" " + balticSeaList[0] + " > " + balticSeaOutputproduct
print("sed-commands:" + northSeaSedCommand + "  " + balticSeaSedCommand)
system(northSeaSedCommand)
system(balticSeaSedCommand)


#TODO: include the bandarithmetic + patching stuff (below) when products are ready

exit(1)

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
    print("\nExecuting: " + northSeaCommand)
    system(northSeaCommand)
    print("\nExecuting: " + balticSeaCommand)
    system(balticSeaCommand)

# Jetzt kommt noch das patchTool, damit die Produkte in jedem Fall komplett sind
patchNorthSeaCommand  = patchTool + " " + northSeaOutputproduct
system(patchNorthSeaCommand)
patchBalticSeaCommand = patchTool + " " + balticSeaOutputproduct
system(patchBalticSeaCommand)

print("\n***************************************************")
print(" Script \'merge_modis_netCDF_products.py\' finished. ")
print("***************************************************\n")

#EOF
