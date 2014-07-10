#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_MC_monthly_L3_binning.py

import os
import os.path
import sys
import time

def printUsage():
    print "Usage: process_MC_monthly_L3_binning.py region month"
    print "where region includes:"
    print "\"NorthSea\", \"Estonia\", or  \"BalticSea\"\n"
    print "and month includes:"
    print "yyyymm"

try:
    argc=len(sys.argv)
    if (argc <= 2):          # the program was called without parameters
        print "Region specifier and/or month specifier is missing!"
        printUsage()
        #sys.exit(1)
    else:                   # we have also received parameters
        if ((sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea") or (sys.argv[1]=="Estonia")):
            # do something
            print "Processing " +str(sys.argv[1]) + " request..."
        else:               # incorrect parameter
            #print "Wrong region specifier!"
            printUsage()
            #sys.exit(1)
except:
    print "Error in parameters. Now exiting..."
    sys.exit(1)    

print "\n******************************************************"
print " Script \'process_MC_monthly_L3_binning.py\' at work... "
print "******************************************************\n"

month = sys.argv[2]

# Verzeichnisse
srcDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/'

# tools config
l3binningHome   = '/home/uwe/tools/l3binning/'
l3binningScript = l3binningHome + 'l3binning.sh'
l3BandArithBatchHome   = '/home/uwe/tools/BandArithBatch/'
l3BandArithBatchScript = l3BandArithBatchHome + 'BandArithBatch.sh'
grid_cell_size = "1.2"

if sys.argv[1]=="NorthSea":
    regionSrcID = 'NSEA'
    regiondestID= '_nos_'
    lat_min = "49.0"
    lat_max = "63.0"
    lon_min = "-5.0"
    lon_max = "13.0"
    l3binningConf   = l3binningHome + 'l3binningConfMcNorthseaMonthly.xml'
    l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_northsea_monthly.bindb'
elif sys.argv[1]=="Estonia":
    regionSrcID = 'ESTONIA'
    regiondestID= '_est_'
    lat_min = "57.058884"
    lat_max = "60.57032"
    lon_min = "21.702216"
    lon_max = "30.225435"
    l3binningConf   = l3binningHome + 'l3binningConfMcEstoniaMonthly.xml'
    l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_estonia_monthly.bindb'
else:
    regionSrcID = 'BALTIC'
    regiondestID= '_bas_'
    lat_min = "53.0"
    lat_max = "66.0"
    lon_min = "9.0"
    lon_max = "31.0"
    l3binningConf   = l3binningHome + 'l3binningConfMcBalticSeaMonthly.xml'
    l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_balticsea_monthly.bindb'
   
myDate=time.localtime()

# konstante xml-bausteine fuer request
request_init_block =                              "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
request_init_block = request_init_block +         "<RequestList>\n"
request_init_block = request_init_block +         "    <Request type=\"BINNING\">\n"
request_init_block = request_init_block +         "        <Parameter name=\"process_type\" value=\"init\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"lat_min\" value=\""+lat_min+"\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"lat_max\" value=\""+lat_max+"\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"lon_min\" value=\""+lon_min+"\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"lon_max\" value=\""+lon_max+"\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"resampling_type\" value=\"binning\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"grid_cell_size\" value=\""+grid_cell_size+"\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"band_name.0\" value=\"chlorophyll_concentration_in_sea_water\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"bitmask.0\" value=\"chlorophyll_concentration_in_sea_water != -999.0\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"weight_coefficient.0\" value=\"0.5\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"band_name.1\" value=\"sea_suspended_matter\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"bitmask.1\" value=\"sea_suspended_matter != -999.0\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"weight_coefficient.1\" value=\"0.5\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"band_name.2\" value=\"yellow_substance\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"bitmask.2\" value=\"yellow_substance != -999.0\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"binning_algorithm.2\" value=\"Arithmetic Mean\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"weight_coefficient.2\" value=\"0.5\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"band_name.3\" value=\"transparency\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"bitmask.3\" value=\"transparency != -999.0\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"binning_algorithm.3\" value=\"Arithmetic Mean\" />\n"
request_init_block = request_init_block +         "        <Parameter name=\"weight_coefficient.3\" value=\"0.5\" />\n"
request_init_block = request_init_block +         "    </Request>\n"
request_update_block =                            "    <Request type=\"BINNING\">\n"
request_update_block = request_update_block +     "        <Parameter name=\"process_type\" value=\"update\" />\n"
request_update_block = request_update_block +     "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_update_block = request_update_block +     "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_update_block = request_update_block +     "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
input_prefix =                                "        <InputProduct URL=\"file:"
input_delimiter =                                 "\" />\n"
block_close=                                      "    </Request>\n"
request_finalize_block =                          "    <Request type=\"BINNING\">\n"
request_finalize_block = request_finalize_block + "       <Parameter name=\"process_type\" value=\"finalize\" />\n"
request_finalize_block = request_finalize_block + "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_finalize_block = request_finalize_block + "        <Parameter name=\"delete_db\" value=\"true\" />\n"
request_finalize_block = request_finalize_block + "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_finalize_block = request_finalize_block + "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_finalize_block = request_finalize_block + "        <Parameter name=\"tailoring\" value=\"false\" />\n"
request_finalize_block = request_finalize_block + "        <OutputProduct URL=\"file:"
request_closer =                                  "\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n"

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Datendirectories:
for a in range(list_size):
    for item in src_list:
        if item.endswith('.data')==1 :
            #print "Removing " + item + " from list."
            src_list.remove(item)

list_size = len(src_list)

# Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
proc_list  = {}
proc_count = 0
for item in src_list:
    if item.find(month)>0 and item.find(regionSrcID)>0:
        #print month+" found in "+ item
        #print "Adding ", item, "to proc_list"
        proc_list[proc_count]=item
        proc_count=proc_count+1

entry={}
for item in proc_list:
    entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter

#print proc_list
#sys.exit(1)

# Jetzt geht's los:
output_filename= destDir + month + regiondestID + "wac_acr_1200.dim"

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

print "\n******************************************************"
print " Script \'process_MC_monthly_L3_binning.py\' finished. "
print "******************************************************\n"

# EOF