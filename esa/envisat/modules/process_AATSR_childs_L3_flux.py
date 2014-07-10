#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_AATSR_childs_L3_flux.py

import os
import os.path
import sys
import time

def printUsage():
    print "Usage: process_AATSR_childs_L3_flux.py region"
    print "where region includes:"
    print "\"NorthSea\"  or  \"BalticSea\"\n"

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print "Region specifier is missing!"
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if ((sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea")):
            # do something
            print "Processing " +str(sys.argv[1]) + " request..."
        else:               # incorrect parameter
            print "Wrong region specifier!"
            printUsage()
            sys.exit(1)
except:
    print "Error in parameters. Now exiting..."
    sys.exit(1)    

print "\n*****************************************************"
print " Script \'process_AATSR_childs_L3_flux.py\' at work... "
print "*****************************************************\n"

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

back_day = 1
# Wir wollen 7 zurueckliegende Tage prozessieren:
days=[back_day, back_day + 1, back_day + 2, back_day + 3, back_day + 4, back_day + 5, back_day + 6]

# Array fuer die Daten der Tage:
previous_dates={}
previous_days={}
daycount=0

for i in days:
    previous_dates[i-1] = get_date_string(get_float_day(i))
    previous_days[daycount]=previous_dates[i-1]
    daycount = daycount + 1

# Verzeichnisse
srcDir = '/fs14/EOservices/InputPool/AATSR/NR/waqs_child_temp/'
destDir = '/fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/'

# tools config
l3binningHome   = '/home/uwe/tools/l3binning/'
l3binningScript = l3binningHome + 'l3binning.sh'


l3binningHome   = '/home/uwe/tools/beam-4.5.1_01/bin/'
l3binningScript = l3binningHome + 'binning.sh'
l3confHome = '/home/uwe/tools/l3binning/'


#=====  old version  ===========================================================
# sst_comb_valid_mask  = '!flags.LAND AND !(flags.NADIR_CLOUD OR flags.FWARD_CLOUD) AND flags.DUAL_SST_VALID'
# sst_nadir_valid_mask = '!flags.LAND AND !(flags.NADIR_CLOUD OR flags.FWARD_CLOUD) AND flags.NADIR_SST_ONLY_VALID'
#===============================================================================

sst_comb_valid_mask  = '!flags.LAND AND flags.DUAL_SST_VALID'
sst_nadir_valid_mask = '!flags.LAND AND !flags.NADIR_CLOUD AND flags.NADIR_SST_ONLY_VALID'

if sys.argv[1]=="NorthSea":
#    regiondestID= '_nos_'
    regiondestID= '_north_sea_'
    lat_min = "49.0"
    lat_max = "63.0"
    lon_min = "-5.0"
    lon_max = "13.0"
    l3binDB = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_aatsr_northsea.bindb'
    l3binningConf   = l3confHome + 'l3binningConfAatsrMcNorthSea.xml'
else:
#    regiondestID= '_bas_'
    regiondestID= '_baltic_sea_'
    lat_min = "53.0"
    lat_max = "66.0"
    lon_min = "9.0"
    lon_max = "31.0"
    l3binDB = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_aatsr_balticsea.bindb'
    l3binningConf   = l3confHome + 'l3binningConfAatsrMcBalticSea.xml'

cells_per_degree = "93"

bands = ['sst_comb', 'sst_nadir']

# konstante xml-bausteine fuer request Baltic Sea
request_init_block =                              '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n'
request_init_block = request_init_block +         '<RequestList>\n'
request_init_block = request_init_block +         '    <Request type=\"BINNING\">\n'
request_init_block = request_init_block +         '        <Parameter name=\"process_type\" value=\"init\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"database\" value=\"' + l3binDB + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"lat_min\" value=\"'  + lat_min +'\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"lat_max\" value=\"'  + lat_max + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"lon_min\" value=\"'  + lon_min + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"lon_max\" value=\"'  + lon_max + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"resampling_type\" value=\"flux-conserving\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"cells_per_degree\" value=\"' + cells_per_degree + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"band_name.0\" value=\"' + bands[0] + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"bitmask.0\" value=\"' + sst_comb_valid_mask + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"weight_coefficient.0\" value=\"1.0\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"band_name.1\" value=\"' + bands[1] + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"bitmask.1\" value=\"' + sst_nadir_valid_mask + '\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n'
request_init_block = request_init_block +         '        <Parameter name=\"weight_coefficient.1\" value=\"1.0\" />\n'
request_init_block = request_init_block +         '    </Request>\n'
request_update_block =                            '    <Request type=\"BINNING\">\n'
request_update_block = request_update_block +     '        <Parameter name=\"process_type\" value=\"update\" />\n'
request_update_block = request_update_block +     '        <Parameter name=\"database\" value=\"' + l3binDB + '\" />\n'
request_update_block = request_update_block +     '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_update_block = request_update_block +     '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
input_prefix =                                    '        <InputProduct URL=\"file:'
input_delimiter =                                 '\" />\n'
block_close =                                     '    </Request>\n'
request_finalize_block =                          '    <Request type=\"BINNING\">\n'
request_finalize_block = request_finalize_block + '        <Parameter name=\"process_type\" value=\"finalize\" />\n'
request_finalize_block = request_finalize_block + '        <Parameter name=\"database\" value=\"' + l3binDB + '\" />\n'
request_finalize_block = request_finalize_block + '        <Parameter name=\"delete_db\" value=\"true\" />\n'
request_finalize_block = request_finalize_block + '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_finalize_block = request_finalize_block + '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_finalize_block = request_finalize_block + '        <Parameter name=\"tailoring\" value=\"false\" />\n'
request_finalize_block = request_finalize_block + '        <OutputProduct URL=\"file:'
request_closer =                                  '\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n'

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Datendirectories:
for a in range(list_size):
    for item in src_list:
        if item.endswith('.data')==1 :
            print "Removing " + item + " from list."
            src_list.remove(item)

list_size = len(src_list)

# Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
proc_list  = {}
proc_count = 0
for item in src_list:
    for d in range(7):
        if item.find(previous_days[d])>0:
            print previous_days[d]+" found in "+ item
            print "Adding ", item, "to proc_list"
            proc_list[proc_count]=item
            proc_count=proc_count+1
            break

entry={}
for item in proc_list:
    entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter

# Jetzt geht's los:
output_filename= destDir + previous_days[6]+"_"+previous_days[0]+ regiondestID + "sst_aatsr_l3_1.2km.dim"

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

print "\n*****************************************************"
print " Script \'process_AATSR_childs_L3_flux.py\' finished. "
print "*****************************************************\n"

# EOF