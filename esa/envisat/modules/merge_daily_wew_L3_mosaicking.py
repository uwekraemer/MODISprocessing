#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: merge_daily_wew_L3_mosaicking.py

import os
import os.path
import sys
import time
import shutil

def printUsage():
    print("Usage: merge_daily_wew_L3_mosaicking.py region back_day")
    print("where region includes:")
    print("\"NorthSea\", \"BalticSea\", \"Estonia\", or \"UK\"\n")
    print("and back_day is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

try:
    argc=len(sys.argv)
    if (argc < 3):          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if ((sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea") or (sys.argv[1]=="UK") or (sys.argv[1]=="Estonia")):
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
print(" Script \'merge_daily_wew_L3_mosaicking.py\' at work... ")
print("******************************************************\n")

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

previous_day = get_date_string(get_float_day(back_day))
print(previous_day)
#sys.exit(1)

# Directories:
srcDir  = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/Level2/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/'

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
    l3mosaickingConf   = l3mosaickingHome + 'l3mosaicWeWNorthSeaDaily.1.1.xml'
elif sys.argv[1]=="BalticSea":
    regiondestID= '_bas_'
    west_lon = "9.0"            # lon_min
    north_lat = "66.0"          # lat_max
    east_lon = "31.0"           # lon_max
    south_lat = "53.0"          # lat_min
    l3mosaickingConf   = l3mosaickingHome + 'l3mosaicWeWBalticSeaDaily.1.1.xml'
elif sys.argv[1]=="Estonia":
    regiondestID= '_est_'
    west_lon = "21.702216"           # lon_min
    north_lat = "60.57032"          # lat_max
    east_lon = "30.225435"           # lon_max
    south_lat = "57.058884"          # lat_min
    l3mosaickingConf   = l3mosaickingHome + 'l3mosaicWeWEstoniaDaily.1.1.xml'
else:
    regiondestID= '_uk_'
    west_lon = "-13.0"            # lon_min
    north_lat = "62.0"          # lat_max
    east_lon = "9.0"           # lon_max
    south_lat = "48.0"          # lat_min
    l3mosaickingConf   = l3mosaickingHome + 'l3mosaicWeWUnitedKingdomDaily.1.1.xml'


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
request_init_block += '        <Parameter name=\"algal_concentration_flags.expression\" value=\"(algal_2==5.0 or result_flags.CHL_OUT) ? 0.0 : exp10(algal_2)\" />\n'
request_init_block += '        <Parameter name=\"algal_concentration_noflags.expression\" value=\"algal_2==5.0 ? 0.0 : exp10(algal_2)\" />\n'
request_init_block += '        <Parameter name=\"total_susp_concentration_flags.expression\" value=\"(total_susp==5.0 or result_flags.TSM_OUT) ? 0.0 : exp10(total_susp)\" />\n'
request_init_block += '        <Parameter name=\"total_susp_concentration_noflags.expression\" value=\"total_susp==5.0 ? 0.0 : exp10(total_susp)\" />\n'
request_init_block += '        <Parameter name=\"yellow_subs_absorption_flags.expression\" value=\"(yellow_subs==5.0 or result_flags.YEL_OUT) ? 0.0 : exp10(yellow_subs)\" />\n'
request_init_block += '        <Parameter name=\"yellow_subs_absorption_noflags.expression\" value=\"yellow_subs==5.0 ? 0.0 : exp10(yellow_subs)\" />\n'
request_init_block += '        <Parameter name=\"condition_operator\" value=\"OR\" />\n'
request_init_block += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_init_block += '        <Parameter name=\"log_prefix\" value=\"mosaic\" />\n'

input_prefix =                                '        <InputProduct URL=\"file:'
line_delimiter =                                                               '\" />\n'
output_prefix =                               '        <OutputProduct URL=\"file:'

request_closer = "\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n"

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen:
for a in range(list_size):
    for item in src_list:
      if item.endswith('.data')==1 :
           # print "Removing " + item + " from list."
            src_list.remove(item)
list_size = len(src_list)

# Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
proc_list  = {}
proc_count = 0
for item in src_list:
    if item.find(previous_day)>-1:
        proc_list[proc_count]=item
        proc_count=proc_count+1

entry={}
for item in proc_list:
    entry[item] = input_prefix + srcDir + proc_list[item] + line_delimiter
    #print entry[item]

if len(proc_list) == 0:
    print("Nothing to do. Now quitting.")
    sys.exit(1)

# Jetzt geht's los:
output_filename= destDir + previous_day + regiondestID + "wac_wew_1200.dim"
output_data_directory = output_filename[0:len(output_filename)-2] + "ata"

# Alles soll neu geschrieben werden:
if os.path.exists(output_data_directory):
    print("Removing existing directory " + output_data_directory)
    shutil.rmtree(output_data_directory)
if os.path.exists(output_filename):
    print("Removing existing file " + output_filename)
    os.remove(output_filename)

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

print("\n*****************************************************")
print(" Script \'merge_daily_wew_L3_mosaicking.py\' finished. ")
print("*****************************************************\n")

# EOF
