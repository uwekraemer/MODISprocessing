#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_MC_weekly_L3_binning.py

import os
import os.path
import sys
import time

def printUsage():
    print('Usage: process_MC_weekly_L3_binning.py region first_day_in_week')
    print('where region includes:')
    print('\"NorthSea\"  or  \"BalticSea\" or  \"Estonia\"')
    print('and first_day_in_week is an integer specifying the first day')
    print('to be included in the weekly L3 product. The value is relative')
    print('to the present date, i.e. 1 means yesterday, 2 the day before yesterday, etc.')
    print('The script will then process products with an acquisition date')
    print('represented by the passed value as the first day in the concerned L3 week, and')
    print('the six days before that date.')
    print('Example: if you invoke the script like:')
    print('process_MC_weekly_L3_binning.py \'NorthSea\' 1')
    print('and today\'s date is 20060709, the included acquisition dates will be')
    print('20060708, 20060707, 20060706, 20060705, 20060704, 20060703, 20060702.') 

try:
    argc=len(sys.argv)
    if (argc < 3):          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if ((sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea") or (sys.argv[1]=="Estonia")):
            # do something
            print("Processing " +str(sys.argv[1]) + " request...")
        else:               # incorrect parameter
            print("Wrong region specifier!")
            printUsage()
            sys.exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)    

try:
    first_day_in_week = int(sys.argv[2])
except:
    print("first_day_in_week parameter must be of type integer!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)

print("\n***********************************************************")
print(" Script \'process_modis_MC_weekly_L3_binning.py\' at work... ")
print("***********************************************************\n")

# Verzeichnisse
srcDir = '/fs14/EOservices/OutputPool/MODIS/WAQS-MC/daily-merged/'
destDir = '/fs14/EOservices/OutputPool/MODIS/WAQS-MC/weekly/'

# tools config
l3binningHome   = '/home/uwe/tools/beam-4.5.1_01/bin/'
l3binningScript = l3binningHome + 'binning.sh'
l3confHome = '/home/uwe/tools/l3binning/'
grid_cell_size = '1.2'

if sys.argv[1]=='NorthSea':
    regionSrcID = 'NSEA'
    regiondestID= '_nos_'
    lat_min = '49.0'
    lat_max = '63.0'
    lon_min = '-5.0'
    lon_max = '13.0'
    l3binningConf   = l3confHome + 'l3binningConfMcNorthsea.xml'
    l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_northsea.bindb'
elif sys.argv[1]=='Estonia':
    regionSrcID = 'BALTIC'
    regiondestID= '_est_'
    lat_min = '57.058884'
    lat_max = '60.57032'
    lon_min = '21.702216'
    lon_max = '30.225435'
    l3binningConf   = l3confHome + 'l3binningConfMcEstonia.xml'
    l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_estonia.bindb'
else:
    regionSrcID = 'BALTIC'
    regiondestID= '_bas_'
    lat_min = '53.0'
    lat_max = '66.0'
    lon_min = '9.0'
    lon_max = '31.0'
    l3binningConf   = l3confHome + 'l3binningConfMcBalticSea.xml'
    l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_balticsea.bindb'

    
myDate=time.localtime()

# Einige nuetzliche Funktionen:
def get_float_day(day):
    secs_per_day  = 24*60*60
    return time.mktime(myDate)-day*secs_per_day


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

# Wir wollen 7 zurueckliegende Tage prozessieren:
days= [first_day_in_week,   first_day_in_week+1, first_day_in_week+2, first_day_in_week+3, \
       first_day_in_week+4, first_day_in_week+5, first_day_in_week+6]

print(days)

# Array fuer die Daten der Tage:
previous_dates={}
previous_days={}
daycount=0

for i in days:
    previous_dates[i-1] = get_date_string(get_float_day(i))
    previous_days[daycount]=previous_dates[i-1]
    daycount += 1

print(previous_dates)
print(previous_days)
#sys.exit(1)

# konstante xml-bausteine fuer request
request_init_block =      "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
request_init_block     += "<RequestList>\n"
request_init_block     += "    <Request type=\"BINNING\">\n"
request_init_block     += "            <Parameter name=\"process_type\" value=\"init\" />\n"
request_init_block     += "            <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_init_block     += "            <Parameter name=\"lat_min\" value=\""+lat_min+"\" />\n"
request_init_block     += "            <Parameter name=\"lat_max\" value=\""+lat_max+"\" />\n"
request_init_block     += "            <Parameter name=\"lon_min\" value=\""+lon_min+"\" />\n"
request_init_block     += "            <Parameter name=\"lon_max\" value=\""+lon_max+"\" />\n"
request_init_block     += "            <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_init_block     += "            <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_init_block     += "            <Parameter name=\"resampling_type\" value=\"binning\" />\n"
request_init_block     += "            <Parameter name=\"grid_cell_size\" value=\""+grid_cell_size+"\" />\n"
request_init_block     += "            <Parameter name=\"band_name.0\" value=\"chlorophyll_concentration_in_sea_water\" />\n"
request_init_block     += "            <Parameter name=\"bitmask.0\" value=\"chlorophyll_concentration_in_sea_water != -999.0\" />\n"
request_init_block     += "            <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n"
request_init_block     += "            <Parameter name=\"weight_coefficient.0\" value=\"1.0\" />\n"
#request_init_block     += "            <Parameter name=\"band_name.1\" value=\"sea_suspended_matter\" />\n"
#request_init_block     += "            <Parameter name=\"bitmask.1\" value=\"sea_suspended_matter != -999.0\" />\n"
#request_init_block     += "            <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n"
#request_init_block     += "            <Parameter name=\"weight_coefficient.1\" value=\"1.0\" />\n"
#request_init_block     += "            <Parameter name=\"band_name.2\" value=\"yellow_substance\" />\n"
#request_init_block     += "            <Parameter name=\"bitmask.2\" value=\"yellow_substance != -999.0\" />\n"
#request_init_block     += "            <Parameter name=\"binning_algorithm.2\" value=\"Arithmetic Mean\" />\n"
#request_init_block     += "            <Parameter name=\"weight_coefficient.2\" value=\"1.0\" />\n"
#request_init_block     += "            <Parameter name=\"band_name.3\" value=\"transparency\" />\n"
#request_init_block     += "            <Parameter name=\"bitmask.3\" value=\"transparency != -999.0\" />\n"
#request_init_block     += "            <Parameter name=\"binning_algorithm.3\" value=\"Arithmetic Mean\" />\n"
#request_init_block     += "            <Parameter name=\"weight_coefficient.3\" value=\"1.0\" />\n"
request_init_block     += "        </Request>\n"

request_update_block    = "    <Request type=\"BINNING\">\n"
request_update_block   += "        <Parameter name=\"process_type\" value=\"update\" />\n"
request_update_block   += "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_update_block   += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_update_block   += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"

input_prefix =            "        <InputProduct URL=\"file:"
input_delimiter =         "\" />\n"
block_close=              "    </Request>\n"

request_finalize_block  = "    <Request type=\"BINNING\">\n"
request_finalize_block += "       <Parameter name=\"process_type\" value=\"finalize\" />\n"
request_finalize_block += "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_finalize_block += "        <Parameter name=\"delete_db\" value=\"true\" />\n"
request_finalize_block += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_finalize_block += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_finalize_block += "        <Parameter name=\"tailoring\" value=\"false\" />\n"
request_finalize_block += "        <OutputProduct URL=\"file:"

request_closer =         "\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n"

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Datendirectories:
for a in range(list_size):
    for item in src_list:
        if item.endswith('.data')==1 :
            print("Removing " + item + " from list.")
            src_list.remove(item)

src_list.sort()
list_size = len(src_list)

# Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
proc_list  = {}
proc_count = 0
for item in src_list:
    for d in range(7):
        if item.find(previous_days[d])>0 and item.find(regionSrcID)>0:
            print(previous_days[d]+" found in "+ item)
            print("Adding ", item, "to proc_list")
            proc_list[proc_count]=item
            proc_count += 1
            break

entry={}
for item in proc_list:
    entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter

# Jetzt geht's los:
output_filename= destDir + previous_days[6]+"_"+previous_days[0]+ regiondestID + "wac_mod_1200.dim"

# Requestfile soll noch nicht existieren, bzw. altes loeschen:
if os.path.exists(l3binningConf):
    os.remove(l3binningConf)

# Erst jetzt wird es erzeugt:
requestfile = open(l3binningConf, 'a')
requestfile.write(request_init_block)
requestfile.write(request_update_block)
for line in range(len(entry)):
    requestfile.write(entry[line])

requestfile.write(block_close)
requestfile.write(request_finalize_block+output_filename)
requestfile.write(request_closer)
requestfile.close()

l3binningCommand = l3binningScript + " " + l3binningConf
print(l3binningCommand)
print("Processing L3...")
os.system(l3binningCommand)

print("\n**********************************************************")
print(" Script \'process_modis_MC_weekly_L3_binning.py\' finished. ")
print("**********************************************************\n")

# EOF