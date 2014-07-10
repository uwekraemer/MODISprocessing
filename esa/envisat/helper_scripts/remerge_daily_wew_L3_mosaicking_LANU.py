#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: remerge_daily_wew_L3_mosaicking_noflags.py

import os
import os.path
import sys
import time
from shutil import rmtree

def printUsage():
    print("Usage: reprocess_IPF_weekly_L3_binning.py start_date end_date")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date")

def make_date_array(start_tupel):
    float_start_date = time.mktime(start_tupel)
    result=[]
    result.append(str(start_tupel[0]) + str(start_tupel[1]).rjust(2,'0') + str(start_tupel[2]).rjust(2,'0'))
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

print("\n****************************************************************")
print(" Script \'remerge_daily_wew_L3_mosaicking_noflags.py\' at work... ")
print("****************************************************************\n")

# Directories:
srcDir  = '/EOData2/related/GeoInfoServices/LANU/MERIS/RR/WAQS-WeW/daily/'
destDir = '/EOData2/related/GeoInfoServices/LANU/MERIS/RR/WAQS-WeW/daily-merged/'

# tools config
l3mosaickingHome   = '/home/uwe/tools/mosaic/'
l3mosaickingScript = l3mosaickingHome + 'mosaic.sh'

l3BandArithBatchHome   = '/home/uwe/tools/BandArithBatch/'
l3BandArithBatchScript = l3BandArithBatchHome + 'BandArithBatch.sh'

pixel_size_x = "0.01078"
pixel_size_y = "0.01078"

for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)
    _year  = int(date[0:4])
    _month = int(date[4:6])
    _day   = int(date[6:len(date)])
    _date_struct = (_year, _month, _day, 1, 0, 0, 0, 0, 1)

    # Wir wollen 7 zurueckliegende Tage prozessieren:
    days= make_date_array(_date_struct)
    print(days)
    #for region in ['NorthSea', 'BalticSea', 'Estonia']:
    for region in ['NorthSea', 'BalticSea']:
        if region=="NorthSea":
            regiondestID= '_nos_'
            west_lon = "-5.0"           # lon_min
            north_lat = "63.0"          # lat_max
            east_lon = "13.0"           # lon_max
            south_lat = "49.0"          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicWeWNorthSeaDaily.1.1.xml'
        elif region=="BalticSea":
            regiondestID= '_bas_'
            west_lon = "9.0"            # lon_min
            north_lat = "66.0"          # lat_max
            east_lon = "31.0"           # lon_max
            south_lat = "53.0"          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicWeWBalticSeaDaily.1.1.xml'
        elif region=="Estonia":
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
        
        # Jetzt nehmen wir nur das Produkt mit dem ersten Datum aus der Liste days:
        proc_list  = {}
        proc_count = 0
        for item in src_list:
            if item.find(days[0])>-1:
                print(days[0] +" found in "+ item)
                print("Adding ", item, "to proc_list")
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
        output_filename= destDir + days[0] + regiondestID + "wac_wew_1200.dim"
        output_data_directory = output_filename[0:len(output_filename)-2] + "ata"
        
        # Alles soll neu geschrieben werden:
        if os.path.exists(output_data_directory):
            print("Removing existing directory " + output_data_directory)
            rmtree(output_data_directory)
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
        print("Executing command " + l3mosaickingCommand + "...")
        os.system(l3mosaickingCommand)

print("\n***************************************************************")
print(" Script \'remerge_daily_wew_L3_mosaicking_noflags.py\' finished. ")
print("***************************************************************\n")

# EOF
