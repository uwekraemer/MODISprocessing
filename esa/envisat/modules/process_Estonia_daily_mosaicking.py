#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_Estonia_daily_mosaicking.py

import os
import os.path
import sys
import time


def printUsage():
    print "Usage: process_Estonia_daily_mosaicking.py back_day"
    print "where back_day is an integer value specifying which day to process:"
    print "1 means yesterday, 2 means the day before yesterday, etc."
    print "Maximum value is 32767.\n"

try:
    argc=len(sys.argv)
    if (argc < 2):          # the program was called incorrectly
        print "\nToo few parameters passed!"
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        try:
            back_day = int(sys.argv[1])
        except:
            print "back_day parameter must be of type integer!"
            printUsage()
            print "\nError in parameters. Now exiting...\n"
            sys.exit(1)
except:
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)    

print "\n*********************************************************"
print " Script \'process_Estonia_daily_mosaicking.py\' at work... "
print "*********************************************************\n"

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
print previous_day

# Directories:
srcDir  = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/'
destDir = srcDir

# tools config
l3mosaickingHome   = '/home/uwe/tools/mosaic/'
#l3mosaickingHome   = '/Users/uwe/Applications/beam-3.7/bin/'
l3mosaickingScript = l3mosaickingHome + 'mosaic3.7.sh'

pixel_size_x = "0.017827408"
pixel_size_y = "0.008968264"

regiondestID= '_est_'
west_lon = "21.702215"           # lon_min
north_lat = "60.57032"          # lat_max
east_lon = "30.225435"           # lon_max
south_lat = "57.058884"          # lat_min
l3mosaickingConf   = l3mosaickingHome + 'l3mosaicMcEstoniaDaily.xml'


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
request_init_block += '        <Parameter name=\"no_data_value\" value=\"-999.0\" />\n'
request_init_block += '        <Parameter name=\"orthorectification\" value=\"false\" />\n'
request_init_block += '        <Parameter name=\"orthorectification_dem\" value=\"GETASSE30\" />\n'
request_init_block += '        <Parameter name=\"chlorophyll_concentration_in_sea_water.expression\" value=\"chlorophyll_concentration_in_sea_water\" />\n'
request_init_block += '        <Parameter name=\"sea_suspended_matter.expression\" value=\"sea_suspended_matter\" />\n'
request_init_block += '        <Parameter name=\"yellow_substance.expression\" value=\"yellow_substance\" />\n'
request_init_block += '        <Parameter name=\"transparency.expression\" value=\"transparency\" />\n'
request_init_block += '        <Parameter name=\"condition_operator\" value=\"OR\" />\n'
request_init_block += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_init_block += '        <Parameter name=\"log_prefix\" value=\"mosaic\" />\n'

print request_init_block

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
      if not item.endswith('.dim') or item.find('NSEA')>1:
            print "Removing " + item + " from list."
            src_list.remove(item)
list_size = len(src_list)

# Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
proc_list  = {}
proc_count = 0
for item in src_list:
    for d in range(7):
        if item.find(previous_day)>-1:
            print previous_day+" found in "+ item
            print "Adding ", item, "to proc_list"
            proc_list[proc_count]=item
            proc_count=proc_count+1
            break

entry={}
output={}
for item in proc_list:
    print item
    entry[item] = input_prefix + srcDir + proc_list[item] + line_delimiter
    output[item] = proc_list[item].replace('BALTIC','ESTONIA')
    print entry[item], output[item]

#sys.exit(1)

# Jetzt geht's los:
output_filename = destDir + output[0]
print output_filename
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
print l3mosaickingCommand
print "Processing L3 Mosaic..."
os.system(l3mosaickingCommand)

print "\n********************************************************"
print " Script \'process_Estonia_daily_mosaicking.py\' finished. "
print "********************************************************\n"

# EOF
