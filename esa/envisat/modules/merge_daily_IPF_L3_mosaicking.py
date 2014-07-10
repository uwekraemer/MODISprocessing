#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: merge_daily_IPF_L3_mosaicking.py

import os
import os.path
import sys
import time

def printUsage():
    print("Usage: merge_daily_IPF_L3_mosaicking.py region back_day")
    print("where region includes:")
    print("\"NorthSea\", \"BalticSea\", \"Estonia\", or \"UK\"\n")
    print("and back_day is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

def log_processing_start():
    print("\n******************************************************")
    print(" Script \'merge_daily_IPF_L3_mosaicking.py\' at work... ")
    print("******************************************************\n")

def log_processing_stop():
    print("\n******************************************************")
    print(" Script \'merge_daily_IPF_L3_mosaicking.py\' finished.  ")
    print("******************************************************\n")

try:
    argc=len(sys.argv)
    if argc < 3:          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if (sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea") or (sys.argv[1]=="Estonia") or (sys.argv[1]=="UK"):
            log_processing_start()
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

myDate=time.localtime()

# Some helper functions:
def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

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

previous_day = get_date_string(get_float_day(back_day))

print(previous_day)
#sys.exit(1)

# Directories:
#srcDir  = '/fs14/EOservices/Attic/MERIS/RR/WAQS-IPF/daily/'
srcDir  = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/'
ensurePathExists(srcDir)
ensurePathExists(destDir)

# tools config
l3mosaickingHome   = '/home/uwe/tools/mosaic/'
l3mosaickingScript = l3mosaickingHome + 'mosaic.sh'

pixel_size_x = "0.01078"
pixel_size_y = "0.01078"

if sys.argv[1]=="NorthSea":
    regiondestID= '_nos_'
    west_lon = "-5.0"           # lon_min
    north_lat = "63.0"          # lat_max
    east_lon = "13.0"           # lon_max
    south_lat = "49.0"          # lat_min
    l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfNorthSeaSeaDaily.xml'
elif sys.argv[1]=="BalticSea":
    regiondestID= '_bas_'
    west_lon = "9.0"            # lon_min
    north_lat = "66.0"          # lat_max
    east_lon = "31.0"           # lon_max
    south_lat = "53.0"          # lat_min
    l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfBalticSeaDaily.xml'
elif sys.argv[1]=="Estonia":
    regiondestID= '_est_'
    west_lon = "21.702216"            # lon_min
    north_lat = "60.57032"          # lat_max
    east_lon = "30.225435"           # lon_max
    south_lat = "57.058884"          # lat_min
    l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfEstoniaDaily.xml'
else:
    regiondestID= '_uk_'
    west_lon = "-13.0"            # lon_min
    north_lat = "62.0"          # lat_max
    east_lon = "9.0"           # lon_max
    south_lat = "48.0"          # lat_min
    l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfUnitedKingdomDaily.xml'
    
chl12_expression          = "algal_12"
chl2_expression           = "(l2_flags.WATER and not l2_flags.PCD_16) ? algal_2 : 0.0"
chl2_unflagged_expression = "l2_flags.WATER ? algal_2 : 0.00"
tsm_expression            = "(l2_flags.WATER and not l2_flags.PCD_16) ? total_susp : 0.0"
tsm_unflagged_expression  = "l2_flags.WATER ? total_susp : 0.0"
ys_expression             = "(l2_flags.WATER and not l2_flags.PCD_16) ? yellow_subs : 0.0"
ys_unflagged_expression   = "l2_flags.WATER ? yellow_subs : 0.0"

# constant xml-blocks for request
request_init_block =  '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n'
request_init_block += '<RequestList>\n'
request_init_block += '    <Request type=\"MOSAIC\">\n'
request_init_block += '        <Parameter name=\"west_lon\" value=\"'+west_lon+'\" />\n'
request_init_block += '        <Parameter name=\"north_lat\" value=\"'+north_lat+'\" />\n'
request_init_block += '        <Parameter name=\"east_lon\" value=\"'+east_lon+'\" />\n'
request_init_block += '        <Parameter name=\"south_lat\" value=\"'+south_lat+'\" />\n'
request_init_block += '        <Parameter name=\"projection_name\" value=\"Geographic Lat/Lon\" />\n'
request_init_block += '        <Parameter name=\"projection_parameters\" value=\"\" />\n'
request_init_block += '        <Parameter name=\"pixel_size_x\" value=\"'+pixel_size_x+'\" />\n'
request_init_block += '        <Parameter name=\"pixel_size_y\" value=\"'+pixel_size_y+'\" />\n'
request_init_block += '        <Parameter name=\"orthorectification\" value=\"false\" />\n'
request_init_block += '        <Parameter name=\"orthorectification_dem\" value=\"GETASSE30\" />\n'
request_init_block += '        <Parameter name=\"algal_12.expression\" value=\"'            + chl12_expression          + '\" />\n'
request_init_block += '        <Parameter name="algal_2.expression" value=\"'               + chl2_expression           + '\" />\n'
request_init_block += '        <Parameter name="algal_2_unflagged.expression" value=\"'     + chl2_unflagged_expression + '\" />\n'
request_init_block += '        <Parameter name=\"total_susp.expression\" value=\"'          + tsm_expression            + '\" />\n'
request_init_block += '        <Parameter name="total_susp_unflagged.expression" value=\"'  + tsm_unflagged_expression  + '\" />\n'
request_init_block += '        <Parameter name=\"yellow_subs.expression\" value=\"'         + ys_expression             + '\" />\n'
request_init_block += '        <Parameter name="yellow_subs_unflagged.expression" value=\"' + ys_unflagged_expression   + '\" />\n'
request_init_block += '        <Parameter name=\"condition_operator\" value=\"OR\" />\n'
request_init_block += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_init_block += '        <Parameter name=\"log_prefix\" value=\"mosaic\" />\n'

input_prefix =        '        <InputProduct URL=\"file:'
line_delimiter =                                '\" />\n'
output_prefix =       '        <OutputProduct URL=\"file:'

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

# Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
proc_list  = {}
proc_count = 0
for item in src_list:
    for d in range(7):
        if item.find(previous_day)>0:
            print(previous_day+" found in "+ item)
            print("Adding ", item, "to proc_list")
            proc_list[proc_count]=item
            proc_count += 1
            break

proc_list_size = len(proc_list)
print(proc_list, proc_list_size)
if not proc_list_size:
    print("No input products found! Now quitting.")
    log_processing_stop()
    sys.exit(1)

entry={}
for item in proc_list:
    entry[item] = input_prefix + srcDir + proc_list[item] + line_delimiter

output_filename= destDir + previous_day + regiondestID + "wac_ipf_1200.dim"
output_block = output_prefix + output_filename

# Requestfile soll noch nicht existieren, bzw. altes loeschen:
if os.path.exists(l3mosaickingConf):
    os.remove(l3mosaickingConf)

# Erst jetzt wird es erzeugt:
requestfile = open(l3mosaickingConf, 'a')
requestfile.write(request_init_block)
for line in range(len(entry)):
    requestfile.write(entry[line])

requestfile.write(output_block)
requestfile.write(request_closer)
requestfile.close()

l3mosaickingCommand = l3mosaickingScript + " " + l3mosaickingConf
print(l3mosaickingCommand)
print("Processing L3 Mosaic...")
os.system(l3mosaickingCommand)

log_processing_stop()
# EOF
