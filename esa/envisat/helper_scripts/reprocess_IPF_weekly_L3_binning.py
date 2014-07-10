#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: reprocess_IPF_weekly_L3_binning.py

import os
import os.path
import sys
import time
from shutil import rmtree

def printUsage():
    print("Usage: reprocess_IPF_weekly_L3_binning.py start_date end_date")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date.")
    print("Each date in the interval [start_date; end_date] results in an array")
    print("of dates to be processed.")
    print("NOTE: start_date and end_date represent the last date")
    print("included in the weekly mean!")

def make_date_array(start_tupel):
    float_start_date = time.mktime(start_tupel)
    result=[]
    result.append(str(start_tupel[0]) + str(start_tupel[1]).rjust(2,'0') + str(start_tupel[2]).rjust(2,'0'))
    for i in range(6):
        date_tupel=time.gmtime(float_start_date - (i+1)*24*60*60)
        date_str = str(date_tupel[0]) + str(date_tupel[1]).rjust(2,'0') + str(date_tupel[2]).rjust(2,'0')
        result.append(date_str)
    return result

try:
    argc=len(sys.argv)
    if (argc < 3):          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        start_date = sys.argv[1]
        end_date   = sys.argv[2]
        if (int(start_date) <= int(end_date) ):
            # do something
            print("\nReprocessing products from " + start_date + " to " + end_date + "...\n")
        else:               # incorrect parameters
            print("Wrong parameters!")
            printUsage()
            sys.exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)    

print("\n********************************************************")
print(" Script \'reprocess_IPF_weekly_L3_binning.py\' at work... ")
print("********************************************************\n")

# Directories:
srcDir  = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily/2009/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/weekly/2009/'
l3binningDatabaseDir = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/'

# tools config
l3binningHome   = '/home/uwe/tools/l3binning/'
l3binningScript = l3binningHome + 'l3binning.sh'

grid_cell_size = "1.2"

for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)
    _year  = int(date[0:4])
    _month = int(date[4:6])
    _day   = int(date[6:len(date)])
    _date_struct = (_year, _month, _day, 1, 0, 0, 0, 0, 1)

    # Wir wollen 7 zurueckliegende Tage prozessieren:
    days= make_date_array(_date_struct)
    print(days)
    #sys.exit(1)
    for region in ['NorthSea', 'BalticSea', 'Estonia']:
#    for region in ['NorthSea', 'BalticSea', 'Estonia', 'UK']:
        if region=="NorthSea":
            regiondestID= '_nos_'
            l3binningConf   = l3binningHome + 'l3binningConfIpfNorthSea.xml'
            l3binningDatabase = l3binningDatabaseDir + 'l3_database_ipf_northsea_reproc.bindb'
            lat_min = "49.0"
            lat_max = "63.0"
            lon_min = "-5.0"
            lon_max = "13.0"
        elif region=="BalticSea":
            regiondestID= '_bas_'
            l3binningConf   = l3binningHome + 'l3binningConfIpfBalticSea.xml'
            l3binningDatabase = l3binningDatabaseDir + 'l3_database_ipf_balticsea_reproc.bindb'
            lat_min = "53.0"
            lat_max = "66.0"
            lon_min = "9.0"
            lon_max = "31.0"
        elif region=="Estonia":
            regiondestID= '_est_'
            l3binningConf   = l3binningHome + 'l3binningConfIpfEstonia.xml'
            l3binningDatabase = l3binningDatabaseDir + 'l3_database_ipf_estonia_reproc.bindb'
            lat_min = "57.058884"
            lat_max = "60.57032"
            lon_min = "21.702216"
            lon_max = "30.225435"
        else:
            regiondestID= '_uk_'
            l3binningConf   = l3binningHome + 'l3binningConfIpfUnitedKingdom.xml'
            l3binningDatabase = l3binningDatabaseDir + 'l3_database_ipf_unitedkingdom_reproc.bindb'
            lat_min = "48.0"
            lat_max = "62.0"
            lon_min = "-13.0"
            lon_max = "9.0"
        
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
                if item.find(days[d])>0:
                    print(days[d]+" found in "+ item)
                    print("Adding ", item, "to proc_list")
                    proc_list[proc_count]=item
                    proc_count=proc_count+1
                    break
        
        entry={}
        for item in proc_list:
            entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter
        
        # Jetzt geht's los:
        
        output_filename= destDir + days[6]+"_"+days[0] + regiondestID + "wac_ipf_1200.dim"
        outputDataDir = output_filename[0:len(output_filename)-2] + "ata"
        # Das Produkt soll komplett neu geschrieben werden:
        if os.path.exists(output_filename):
            os.remove(output_filename)
        if os.path.exists(outputDataDir):
            rmtree(outputDataDir)
        
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
print(" Script \'reprocess_IPF_weekly_L3_binning.py\' finished. ")
print("******************************************************\n")

# EOF
