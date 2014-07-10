#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_IPF_weekly_L3_binning.py

import os
import os.path
import sys
import time

def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

def printUsage():
    print("Usage: process_IPF_weekly_L3_binning.py region back_day")
    print("where region includes:")
    print("\"NorthSea\", \"BalticSea\", \"Estonia\", or \"UK\"\n")
    print("and back_day is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

try:
    argc=len(sys.argv)
    if argc < 3:          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if (sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea") or (sys.argv[1]=="Estonia") or (sys.argv[1]=="UK"):
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
    back_day = int(sys.argv[2])
except:
    print("back_day parameter must be of type integer!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)

print("\n******************************************************")
print(" Script \'process_IPF_weekly_L3_binning.py\' at work... ")
print("******************************************************\n")

# Directories:
srcDir  = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/weekly/'
l3binningDatabaseDir = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/'
ensurePathExists(destDir)
ensurePathExists(l3binningDatabaseDir)

# tools config
l3binningHome   = '/home/uwe/tools/l3binning/'
l3binningScript = l3binningHome + 'l3binning.sh'

grid_cell_size = "1.2"

if sys.argv[1]=="NorthSea":
    regiondestID= '_nos_'
    l3binningConf   = l3binningHome + 'l3binningConfIpfNorthSea.xml'
    l3binningDatabase = l3binningDatabaseDir + 'l3_database_ipf_northsea.bindb'
    lat_min = "49.0"
    lat_max = "63.0"
    lon_min = "-5.0"
    lon_max = "13.0"
elif sys.argv[1]=="BalticSea":
    regiondestID= '_bas_'
    l3binningConf   = l3binningHome + 'l3binningConfIpfBalticSea.xml'
    l3binningDatabase = l3binningDatabaseDir + 'l3_database_ipf_balticsea.bindb'
    lat_min = "53.0"
    lat_max = "66.0"
    lon_min = "9.0"
    lon_max = "31.0"
elif sys.argv[1]=="Estonia":
    regiondestID= '_est_'
    l3binningConf   = l3binningHome + 'l3binningConfIpfEstonia.xml'
    l3binningDatabase = l3binningDatabaseDir + 'l3_database_ipf_estonia.bindb'
    lat_min = "57.058884"
    lat_max = "60.57032"
    lon_min = "21.702216"
    lon_max = "30.225435"
else:
    regiondestID= '_uk_'
    l3binningConf   = l3binningHome + 'l3binningConfIpfUnitedKingdom.xml'
    l3binningDatabase = l3binningDatabaseDir + 'l3_database_ipf_unitedkingdom.bindb'
    lat_min = "48.0"
    lat_max = "62.0"
    lon_min = "-13.0"
    lon_max = "9.0"

myDate=time.localtime()

# Some helper functions:
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

# process 7 back dating days:
days=[back_day, back_day + 1, back_day + 2, back_day + 3, back_day + 4, back_day + 5, back_day + 6]

# Arrays for the dates:
previous_dates={}
previous_days={}
daycount=0

for i in days:
    previous_dates[i-1] = get_date_string(get_float_day(i))
    previous_days[daycount]=previous_dates[i-1]
    daycount += 1

print(previous_days)
#sys.exit(1)

# constant xml-blocks for request
request_init_block =      '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n'
request_init_block +=     '<RequestList>\n'
request_init_block +=     '    <Request type=\"BINNING\">\n'
request_init_block +=     '        <Parameter name=\"process_type\" value=\"init\" />\n'
request_init_block +=     '        <Parameter name=\"database\" value=\"'+l3binningDatabase+'\" />\n'
request_init_block +=     '        <Parameter name=\"lat_min\" value=\"'+lat_min+'\" />\n'
request_init_block +=     '        <Parameter name=\"lat_max\" value=\"'+lat_max+'\" />\n'
request_init_block +=     '        <Parameter name=\"lon_min\" value=\"'+lon_min+'\" />\n'
request_init_block +=     '        <Parameter name=\"lon_max\" value=\"'+lon_max+'\" />\n'
request_init_block +=     '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_init_block +=     '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_init_block +=     '        <Parameter name=\"resampling_type\" value=\"binning\" />\n'
request_init_block +=     '        <Parameter name=\"grid_cell_size\" value=\"'+grid_cell_size+'\" />\n'
request_init_block +=     '        <Parameter name=\"band_name.0\" value=\"algal_12\" />\n'
request_init_block +=     '        <Parameter name=\"bitmask.0\" value=\"\" />\n'
request_init_block +=     '        <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n'
request_init_block +=     '        <Parameter name=\"weight_coefficient.0\" value=\"0.5\" />\n'
request_init_block +=     '        <Parameter name=\"band_name.1\" value=\"yellow_subs\" />\n'
request_init_block +=     '        <Parameter name=\"bitmask.1\" value=\"l2_flags.WATER and not l2_flags.PCD_16\" />\n'
request_init_block +=     '        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n'
request_init_block +=     '        <Parameter name=\"weight_coefficient.1\" value=\"0.5\" />\n'
request_init_block +=     '        <Parameter name=\"band_name.2\" value=\"total_susp\" />\n'
request_init_block +=     '        <Parameter name=\"bitmask.2\" value=\"l2_flags.WATER and not l2_flags.PCD_16\" />\n'
request_init_block +=     '        <Parameter name=\"binning_algorithm.2\" value=\"Arithmetic Mean\" />\n'
request_init_block +=     '        <Parameter name=\"weight_coefficient.2\" value=\"0.5\" />\n'
request_init_block +=     '    </Request>\n'
request_update_block =    '    <Request type=\"BINNING\">\n'
request_update_block +=   '        <Parameter name=\"process_type\" value=\"update\" />\n'
request_update_block +=   '        <Parameter name=\"database\" value=\"'+l3binningDatabase+'\" />\n'
request_update_block +=   '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_update_block +=   '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
input_prefix =            '        <InputProduct URL=\"file:'
input_delimiter =                                   '\" />\n'
block_close =             '    </Request>\n'
request_finalize_block =  '    <Request type=\"BINNING\">\n'
request_finalize_block += '        <Parameter name=\"process_type\" value=\"finalize\" />\n'
request_finalize_block += '        <Parameter name=\"database\" value=\"'+l3binningDatabase+'\" />\n'
request_finalize_block += '        <Parameter name=\"delete_db\" value=\"true\" />\n'
request_finalize_block += '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_finalize_block += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_finalize_block += '        <Parameter name=\"tailoring\" value=\"false\" />\n'
request_finalize_block += '        <OutputProduct URL=\"file:'

request_closer = "\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n"

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen:
for a in range(list_size):
    for item in src_list:
        if item.startswith('MER_')==0 or item.startswith('MER_RR__1P')==1 or item.endswith('.data'):
            #print "Removing " + item + " from list."
            src_list.remove(item)

list_size = len(src_list)

# Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
proc_list  = {}
proc_count = 0
for item in src_list:
    for d in range(7):
        if item.find(previous_days[d])>0:
            print(previous_days[d]+" found in "+ item)
            print("Adding ", item, "to proc_list")
            proc_list[proc_count]=item
            proc_count += 1
            break

entry={}
for item in proc_list:
    entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter

# Jetzt geht's los:

output_filename= destDir + previous_days[6]+"_"+previous_days[0] + regiondestID + "wac_ipf_1200.dim"

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

print("\n******************************************************")
print(" Script \'process_IPF_weekly_L3_binning.py\' finished. ")
print("******************************************************\n")

# EOF