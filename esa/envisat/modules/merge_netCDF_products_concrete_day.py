#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: merge_netCDF_products_concrete_day.py

import os.path
import os
import sys
import time

today=time.localtime()
#print today
concreteday=(2011, 12, 11, 1, 0, 0, 0, 0, 1)
#print concreteday

# Einige nuetzliche Funktionen:
def get_float_day(day):
    secs_per_day  = 24*60*60
    return time.mktime(concreteday)-day*secs_per_day


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

print("\n***********************************************************")
print(" Script \'merge_netCDF_products_concrete_day.py\' at work... ")
print("***********************************************************\n")

srcDir='/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily/'
bandArithTool='/home/uwe/tools/BandArithBatch/BandArithBatch.sh'
patchTool='/home/uwe/tools/patchTool/patchTool.sh'
destDir='/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/'


_year  = str(concreteday[0])
_month = str(concreteday[1])
_day   = str(concreteday[2])
#_hour  = str(today[3]) 
#_minute= str(today[4])
#_second= str(today[5])
 
if concreteday[1] < 10:
    _month = "0"+ _month

if concreteday[2] < 10:
    _day = "0"+ _day

#datestring = _year + _month + _day + " " + _hour + ":" + _minute + ":" + _second

# Dateien werden mit dem Datum von vorgestern verarbeitet

arrival_day=get_date_string(get_float_day(0))
myDate = arrival_day
#myDate =  _year + _month + _day
#myDate = '20060605'

src_list = os.listdir(srcDir)
list_size = len(src_list)

for a in range(list_size):
    for item in src_list:
        if item.endswith('___0000.data')==1 or item.startswith('L3_ENV_MER_')==0 or item.find(myDate)==-1:
            #print "Removing " + item + " from list."
            src_list.remove(item)

print('\nsrc_list=', src_list)
if (len(src_list) == 0):
    print('Nothing to do. Now exiting...')
    sys.exit(1)

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
        northSeaCount = northSeaCount + 1
    elif src_list[item].find('BALTIC')>0:
        #print balticSeaCount
        #print "Adding file " + src_list[item] + " to Baltic Sea list..."
        balticSeaDummyList[balticSeaCount] = srcDir + src_list[item]
        balticSeaCount = balticSeaCount + 1

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

northSeaOutputproduct  = destDir + 'L3_ENV_MER_' + myDate + '_NSEA_PC_ACR___0000.dim'
northSeaOutputData     = destDir + 'L3_ENV_MER_' + myDate + '_NSEA_PC_ACR___0000.data'
balticSeaOutputproduct = destDir + 'L3_ENV_MER_' + myDate + '_BALTIC_PC_ACR___0000.dim'
balticSeaOutputData    = destDir + 'L3_ENV_MER_' + myDate + '_BALTIC_PC_ACR___0000.data'

print("northSeaOutputproduct: "  + northSeaOutputproduct)
print("balticSeaOutputproduct: " + balticSeaOutputproduct)


# zuerst die CHL12-Produkte als Zielprodukt fuer Bandarithmetik kopieren:

northSeaDataDirectory  = northSeaList[0][0:len(northSeaList[0])-2] + "ata"
northSeaCopyDataCommand = "cp -rf " + northSeaDataDirectory + "* " + northSeaOutputData

balticSeaDataDirectory  = balticSeaList[0][0:len(balticSeaList[0])-2] + "ata"
balticSeaCopyDataCommand = "cp -rf " + balticSeaDataDirectory + "* " + balticSeaOutputData

os.system(northSeaCopyDataCommand)
os.system(balticSeaCopyDataCommand)

# dann in den .dim-files die Namen korrigieren:
# sed syntax:
# sed -e "s/_CHL12_j__/_/" <file>

northSeaSedCommand  = "sed -e \"s/_CHL12_j__/_/\" " + northSeaList[0] + " > "  + northSeaOutputproduct
balticSeaSedCommand = "sed -e \"s/_CHL12_j__/_/\" " + balticSeaList[0] + " > " + balticSeaOutputproduct
print("sed-commands:" + northSeaSedCommand + "  " + balticSeaSedCommand)
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
    print("\nExecuting: " + northSeaCommand)
    os.system(northSeaCommand)
    print("\nExecuting: " + balticSeaCommand)
    os.system(balticSeaCommand)

# Jetzt kommt noch das patchTool, damit die Produkte in jedem Fall komplett sind
patchNorthSeaCommand  = patchTool + " " + northSeaOutputproduct
os.system(patchNorthSeaCommand)
patchBalticSeaCommand = patchTool + " " + balticSeaOutputproduct
os.system(patchBalticSeaCommand)

print("\n***********************************************************")
print(" Script \'merge_netCDF_products_concrete_day.py\' finished. ")
print("***********************************************************\n")

#EOF
