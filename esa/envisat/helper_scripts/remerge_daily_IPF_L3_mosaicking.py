#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: merge_daily_IPF_L3_mosaicking.py

import os
import os.path
import sys
import time
from shutil import rmtree

def printUsage():
    print("Usage: remerge_daily_IPF_L3_mosaicking.py start_date end_date")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date")

def log_processing_start():
    print("\n********************************************************")
    print(" Script \'remerge_daily_IPF_L3_mosaicking.py\' at work... ")
    print("********************************************************\n")

def log_processing_stop():
    print("\n********************************************************")
    print(" Script \'remerge_daily_IPF_L3_mosaicking.py\' finished.  ")
    print("********************************************************\n")

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
    sys.exit(1)

# Directories:
#srcDir  = '/fs14/EOservices/Attic/MERIS/RR/WAQS-IPF/daily/'
srcDir  = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/'

# tools config
l3mosaickingHome   = '/home/uwe/tools/mosaic/'
l3mosaickingScript = l3mosaickingHome + 'mosaic.sh'

pixel_size_x = "0.01078"
pixel_size_y = "0.01078"
chl12_expression          = "algal_12"
chl2_expression           = "(l2_flags.WATER and not l2_flags.PCD_16) ? algal_2 : 0.0"
chl2_unflagged_expression = "l2_flags.WATER ? algal_2 : 0.00"
tsm_expression            = "(l2_flags.WATER and not l2_flags.PCD_16) ? total_susp : 0.0"
tsm_unflagged_expression  = "l2_flags.WATER ? total_susp : 0.0"
ys_expression             = "(l2_flags.WATER and not l2_flags.PCD_16) ? yellow_subs : 0.0"
ys_unflagged_expression   = "l2_flags.WATER ? yellow_subs : 0.0"

for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)

    for region in ['NorthSea', 'BalticSea', 'Estonia']:
#    for region in ['NorthSea', 'BalticSea', 'Estonia', 'UK']:

        if region=="NorthSea":
            regiondestID= '_nos_'
            west_lon = "-5.0"           # lon_min
            north_lat = "63.0"          # lat_max
            east_lon = "13.0"           # lon_max
            south_lat = "49.0"          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfNorthSeaSeaDaily_reproc.xml'
        elif region=="BalticSea":
            regiondestID= '_bas_'
            west_lon = "9.0"            # lon_min
            north_lat = "66.0"          # lat_max
            east_lon = "31.0"           # lon_max
            south_lat = "53.0"          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfBalticSeaDaily_reproc.xml'
        elif region=="Estonia":
            regiondestID= '_est_'
            west_lon = "21.702216"            # lon_min
            north_lat = "60.57032"          # lat_max
            east_lon = "30.225435"           # lon_max
            south_lat = "57.058884"          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfEstoniaDaily_reproc.xml'
        else:
            regiondestID= '_uk_'
            west_lon = "-13.0"            # lon_min
            north_lat = "62.0"          # lat_max
            east_lon = "9.0"           # lon_max
            south_lat = "48.0"          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfUnitedKingdomDaily_reproc.xml'
                
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
                if not item.startswith('MER_') or item.startswith('MER_RR__1P') or item.endswith('.data'):
                    src_list.remove(item)
        
        # Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
        proc_list  = {}
        proc_count = 0
        for item in src_list:
            for d in range(7):
                if item.find(date)>0:
                    proc_list[proc_count]=item
                    proc_count=proc_count+1
                    break
        
        proc_list_size = len(proc_list)
        print(proc_list, proc_list_size)
        if proc_list_size==0:
            print("No input products found! Now quitting.")
            log_processing_stop()
            sys.exit(1)
        
        entry={}
        for item in proc_list:
            entry[item] = input_prefix + srcDir + proc_list[item] + line_delimiter
        
        output_filename= destDir + date + regiondestID + "wac_ipf_1200.dim"
        outputDataDir = output_filename[0:len(output_filename)-2] + "ata"
        # Das Produkt soll komplett neu geschrieben werden:
        if os.path.exists(output_filename):
            os.remove(output_filename)
        if os.path.exists(outputDataDir):
            rmtree(outputDataDir)


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
