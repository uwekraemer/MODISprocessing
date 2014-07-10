#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_wew_weekly_L3.py

import os
import os.path
import sys
import time


def printUsage():
    print "Usage: process_wew_weekly_L3.py region back_day"
    print "where region includes:"
    print "\"NorthSea\", \"BalticSea\", \"Estonia\", or \"UK\"\n"
    print "and back_day is an integer value specifying which day to process:"
    print "1 means yesterday, 2 means the day before yesterday, etc."
    print "Maximum value is 32767.\n"

try:
    argc=len(sys.argv)
    if (argc < 3):          # the program was called incorrectly
        print "\nToo few parameters passed!"
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if ((sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea") or (sys.argv[1]=="Estonia") or (sys.argv[1]=="UK")):
            # do something
            print "Processing " +str(sys.argv[1]) + " request..."
        else:               # incorrect parameter
            print "Wrong region specifier!"
            printUsage()
            sys.exit(1)
except:
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)    

try:
    back_day = int(sys.argv[2])
except:
    print "back_day parameter must be of type integer!"
    printUsage()
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)

print "\n**********************************************"
print " Script \'process_wew_weekly_L3.py\' at work... "
print "**********************************************\n"

# Einige nuetzliche Funktionen:
def get_float_day(day):
    secs_per_day  = 24*60*60
    return time.mktime(time.localtime())-day*secs_per_day


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
days=[back_day, back_day + 1,  back_day + 2,  back_day + 3,  back_day + 4,  back_day + 5,  back_day + 6]

# Array fuer die Daten der Tage:
previous_dates={}
previous_days={}
daycount=0

for i in days:
    previous_dates[i-1] = get_date_string(get_float_day(i))
    previous_days[daycount]=previous_dates[i-1]
    daycount = daycount + 1

print previous_days
#sys.exit(1)

# Verzeichnisse
srcDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/Level2/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/Level3/'

# tools config
l3binningHome    = '/home/uwe/tools/l3binning/'
l3binningScript  = l3binningHome + 'l3binning.sh'
l3BinningBaseDir = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/'

l3BandArithBatchHome   = '/home/uwe/tools/BandArithBatch/'
l3BandArithBatchScript = l3BandArithBatchHome + 'BandArithBatch.sh'

if sys.argv[1]=="NorthSea":
    regiondestID = 'north_sea'
    lat_min = "49.0"
    lat_max = "63.0"
    lon_min = "-5.0"
    lon_max = "13.0"
    l3binningConf = l3binningHome    + 'l3binningConfNorthSea.xml'
    l3BinningDb   = l3BinningBaseDir + 'l3_database_wew_northsea.bindb'
elif sys.argv[1]=="BalticSea":
    regiondestID = 'baltic_sea'
    lat_min = "53.0"
    lat_max = "66.0"
    lon_min = "9.0"
    lon_max = "31.0"
    l3binningConf = l3binningHome    + 'l3binningConfBaltic.xml'
    l3BinningDb   = l3BinningBaseDir + 'l3_database_wew_balticsea.bindb'
elif sys.argv[1]=="Estonia":
    regiondestID = 'estonia'
    lat_min = "57.058884"
    lat_max = "60.57032"
    lon_min = "21.702216"
    lon_max = "30.225435"
    l3binningConf = l3binningHome    + 'l3binningConfEstonia.xml'
    l3BinningDb   = l3BinningBaseDir + 'l3_database_wew_estonia.bindb'
else:
    regiondestID = 'uk'
    lat_min = "48.0"
    lat_max = "62.0"
    lon_min = "-13.0"
    lon_max = "9.0"
    l3binningConf = l3binningHome    + 'l3binningConfUnitedKingdom.xml'
    l3BinningDb   = l3BinningBaseDir + 'l3_database_wew_unitedkingdom.bindb'

grid_cell_size = "1.2"
chl_bitmask = "not result_flags.CHL_OUT and algal_2 != 5"
ys_bitmask  = "not result_flags.YEL_OUT and yellow_subs != 5"
tsm_bitmask = "not result_flags.TSM_OUT and total_susp != 5"

# konstante xml-bausteine fuer request North Sea
request_init_block     =  "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
request_init_block     += "<RequestList>\n"
request_init_block     += "    <Request type=\"BINNING\">\n"
request_init_block     += "        <Parameter name=\"process_type\" value=\"init\" />\n"
request_init_block     += "        <Parameter name=\"database\" value=\"" + l3BinningDb + "\" />\n"
request_init_block     += "        <Parameter name=\"lat_min\" value=\""+lat_min+"\" />\n"
request_init_block     += "        <Parameter name=\"lat_max\" value=\""+lat_max+"\" />\n"
request_init_block     += "        <Parameter name=\"lon_min\" value=\""+lon_min+"\" />\n"
request_init_block     += "        <Parameter name=\"lon_max\" value=\""+lon_max+"\" />\n"
request_init_block     += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_init_block     += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_init_block     += "        <Parameter name=\"resampling_type\" value=\"binning\" />\n"
request_init_block     += "        <Parameter name=\"grid_cell_size\" value=\""+grid_cell_size+"\" />\n"
request_init_block     += "        <Parameter name=\"band_name.0\" value=\"algal_2\" />\n"
request_init_block     += "        <Parameter name=\"bitmask.0\" value=\""+ chl_bitmask + "\" />\n"
request_init_block     += "        <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n"
request_init_block     += "        <Parameter name=\"weight_coefficient.0\" value=\"0.5\" />\n"
request_init_block     += "        <Parameter name=\"band_name.1\" value=\"yellow_subs\" />\n"
request_init_block     += "        <Parameter name=\"bitmask.1\" value=\""+ ys_bitmask + "\" />\n"
request_init_block     += "        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n"
request_init_block     += "        <Parameter name=\"weight_coefficient.1\" value=\"0.5\" />\n"
request_init_block     += "        <Parameter name=\"band_name.2\" value=\"total_susp\" />\n"
request_init_block     += "        <Parameter name=\"bitmask.2\" value=\""+ tsm_bitmask + "\" />\n"
request_init_block     += "        <Parameter name=\"binning_algorithm.2\" value=\"Arithmetic Mean\" />\n"
request_init_block     += "        <Parameter name=\"weight_coefficient.2\" value=\"0.5\" />\n"
request_init_block     += "    </Request>\n"
request_update_block   =  "    <Request type=\"BINNING\">\n"
request_update_block   += "        <Parameter name=\"process_type\" value=\"update\" />\n"
request_update_block   += "        <Parameter name=\"database\" value=\"" + l3BinningDb + "\" />\n"
request_update_block   += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_update_block   += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
input_prefix =            "        <InputProduct URL=\"file:"
input_delimiter =         "\" />\n"
block_close=              "    </Request>\n"
request_finalize_block =  "    <Request type=\"BINNING\">\n"
request_finalize_block += "        <Parameter name=\"process_type\" value=\"finalize\" />\n"
request_finalize_block += "        <Parameter name=\"database\" value=\"" + l3BinningDb + "\" />\n"
request_finalize_block += "        <Parameter name=\"delete_db\" value=\"true\" />\n"
request_finalize_block += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_finalize_block += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_finalize_block += "        <Parameter name=\"tailoring\" value=\"false\" />\n"
request_finalize_block += "        <OutputProduct URL=\"file:"
request_closer =          "\" format=\"BEAM-DIMAP\" />\n"
request_closer +=         "    </Request>\n"
request_closer +=         "</RequestList>\n"

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 oder Level2 sind:
for a in range(list_size):
    for item in src_list:
        if item.endswith('.data')==1 :
            print "Removing " + item + " from list."
            src_list.remove(item)

list_size = len(src_list)

num_days  = len(previous_days)

# Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
proc_list  = {}
proc_count = 0
for item in src_list:
    for d in range(num_days):
        if item.startswith(previous_days[d])==1:
            print previous_days[d]+" found in "+ item
            print "Adding ", item, "to proc_list"
            proc_list[proc_count]=item
            proc_count=proc_count+1
            break

entry={}
for item in proc_list:
    entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter

if len(proc_list) == 0:
    print "Nothing to do. Now quitting."
    sys.exit(1)

output_filename= destDir + previous_days[6]+"_"+previous_days[0]+ "_wew_" + regiondestID + "_l3_"+grid_cell_size+"km.dim"

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
print l3binningCommand
print "Processing L3..."
os.system(l3binningCommand)

# Postprocessing:
l3BandArithBatchParams  = "algal_concentration \"algal_2_mean==0.0?0:exp10(algal_2_mean)\" "
l3BandArithBatchParams += "total_susp_concentration \"total_susp_mean==0.0?0:exp10(total_susp_mean)\" "
l3BandArithBatchParams += "yellow_subs_absorption \"yellow_subs_mean==0.0?0:exp10(yellow_subs_mean)\""

l3BandArithBatchCommand = l3BandArithBatchScript + " " + output_filename + " " + l3BandArithBatchParams
print "Postprocessing L3..."
os.system(l3BandArithBatchCommand)

print "\n**********************************************"
print " Script \'process_wew_weekly_L3.py\' finished. "
print "**********************************************\n"

# EOF
