#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: remerge_daily_IPF_L3_mosaicking.py

import os
import os.path
from sys import argv, exit
from time import mktime, localtime

def printUsage():
    print("Usage: remerge_daily_AATSR_L3_mosaicking.py <start_date> <end_date>")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date")

def log_processing_start():
    print("\n********************************************************")
    print(" Script \'remerge_daily_AATSR_L3_mosaicking.py\' at work... ")
    print("********************************************************\n")

def log_processing_stop():
    print("\n********************************************************")
    print(" Script \'remerge_daily_AATSR_L3_mosaicking.py\' finished.  ")
    print("********************************************************\n")

def make_date_array(start_tupel):
    float_start_date = mktime(start_tupel)
    result=[]
    result.append(str(start_tupel[0]) + str(start_tupel[1]).rjust(2,'0') + str(start_tupel[2]).rjust(2,'0'))
    return result

try:
    argc=len(argv)
    if (argc < 3):          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        exit(1)
    else:                   # we have also received parameters
        start_date = argv[1]
        end_date   = argv[2]
        if (int(start_date) <= int(end_date) ):
            # do something
            print("\nReprocessing products from " + start_date + " to " + end_date + "...\n")
        else:               # incorrect parameters
            print("Wrong parameters!")
            printUsage()
            exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    exit(1)    

try:
    back_day = int(argv[2])
except:
    print("back_day parameter must be of type integer!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    exit(1)

# Directories:
srcDir  = '/fs14/EOservices/InputPool/AATSR/NR/waqs_child_temp/'
destDir = '/fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/daily-merged/'

# tools config
l3mosaickingHome   = '/home/uwe/tools/mosaic/'
l3mosaickingScript = '/home/uwe/tools/beam-4.1.1/bin/mosaic.sh'

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
    for region in ['NorthSea', 'BalticSea', 'Estonia']:
        if region=='NorthSea':
            regiondestID= '_north_sea_'
            west_lon = '-5.0'           # lon_min
            north_lat = '63.0'          # lat_max
            east_lon = '13.0'           # lon_max
            south_lat = '49.0'          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfNorthSeaDaily_re.xml'
        elif region=='BalticSea':
            regiondestID= '_baltic_sea_'
            west_lon = '9.0'            # lon_min
            north_lat = '66.0'          # lat_max
            east_lon = '31.0'           # lon_max
            south_lat = '53.0'          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfBalticSeaDaily_re.xml'
        elif region=='Estonia':
            regiondestID= '_estonia_'
            west_lon = '21.702216'            # lon_min
            north_lat = '60.57032'          # lat_max
            east_lon = '30.225435'           # lon_max
            south_lat = '57.058884'          # lat_min
            l3mosaickingConf   = l3mosaickingHome + 'l3mosaicIpfEstoniaDaily_re.xml'
            
#=====  old version  ===========================================================
#        sst_nadir_expression = '(!flags.LAND AND !(flags.NADIR_CLOUD OR flags.FWARD_CLOUD) AND flags.NADIR_SST_ONLY_VALID) ? sst_nadir : 0.0'
#        sst_comb_expression  = '(!flags.LAND AND !(flags.NADIR_CLOUD OR flags.FWARD_CLOUD) AND flags.DUAL_SST_VALID) ? sst_comb : 0.0'
#===============================================================================

        sst_nadir_expression = '(!flags.LAND AND !flags.NADIR_CLOUD AND flags.NADIR_SST_ONLY_VALID) ? sst_nadir : 0.0'
        sst_comb_expression  = '(!flags.LAND AND flags.DUAL_SST_VALID) ? sst_comb : 0.0'
        
        # constant xml-blocks for request
        request_init_block =  '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n'
        request_init_block += '<RequestList>\n'
        request_init_block += '    <Request type=\"MOSAIC\">\n'
        request_init_block += '        <Parameter name=\"west_lon\" value=\"' + west_lon + '\" />\n'
        request_init_block += '        <Parameter name=\"north_lat\" value=\"' + north_lat + '\" />\n'
        request_init_block += '        <Parameter name=\"east_lon\" value=\"' + east_lon + '\" />\n'
        request_init_block += '        <Parameter name=\"south_lat\" value=\"' + south_lat +'  \" />\n'
        request_init_block += '        <Parameter name=\"projection_name\" value=\"Geographic Lat/Lon\" />\n'
        request_init_block += '        <Parameter name=\"projection_parameters\" value=\"\" />\n'
        request_init_block += '        <Parameter name=\"pixel_size_x\" value=\"' + pixel_size_x + '\" />\n'
        request_init_block += '        <Parameter name=\"pixel_size_y\" value=\"' + pixel_size_y + '\" />\n'
        request_init_block += '        <Parameter name=\"no_data_value\" value=\"9999.0\" />\n'
        request_init_block += '        <Parameter name=\"orthorectification\" value=\"false\" />\n'
        request_init_block += '        <Parameter name=\"orthorectification_dem\" value=\"GETASSE30\" />\n'
        request_init_block += '        <Parameter name=\"sst_nadir.expression\" value=\"' + sst_nadir_expression + '\" />\n'
        request_init_block += '        <Parameter name=\"sst_comb.expression" value=\"'   + sst_comb_expression  + '\" />\n'
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
                if not item.startswith('ATS_NR__2P') or not item.endswith('.N1'):
                    #print "Removing " + item + " from list."
                    src_list.remove(item)
        
        # Jetzt nehmen wir nur das Produkt mit dem ersten Datum aus der Liste days:
        proc_list  = []
        proc_count = 0
        for item in src_list:
            if item.find(days[0])>-1:
                print(days[0] +" found in "+ item)
                print("Adding ", item, "to proc_list")
                proc_list.append(item)
                proc_count=proc_count+1
        
        if proc_count==0:
            print("No input products found! Now quitting.")
            log_processing_stop()
            exit(1)
        
        entry=[]
        for counter in range(proc_count):
            entry.append(input_prefix + srcDir + proc_list[counter] + line_delimiter)
        
        output_filename= destDir + days[0] + regiondestID + "sst_aatsr_1.2km.dim"
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
