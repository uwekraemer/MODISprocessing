#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: reprocess_AATSR_childs_L3_flux.py

import os
import os.path
import sys
import time

def printUsage():
    print("Usage: reprocess_AATSR_childs_L3_flux.py start_date end_date")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date")
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

print("\n*****************************************************")
print(" Script \'reprocess_AATSR_childs_L3_flux.py\' at work... ")
print("*****************************************************\n")

myDate=time.localtime()



# Verzeichnisse
srcDir = '/fs14/EOservices/InputPool/AATSR/NR/waqs_child_temp/'
destDir = '/fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/'

# tools config
l3binningHome   = '/home/uwe/tools/l3binning/'
l3binningScript = l3binningHome + 'l3binning.sh'
l3BandArithBatchHome   = '/home/uwe/tools/BandArithBatch/'
l3BandArithBatchScript = l3BandArithBatchHome + 'BandArithBatch.sh'
grid_cell_size = "1.2"

sst_comb_valid_mask  = '!flags.LAND AND !(flags.NADIR_CLOUD OR flags.FWARD_CLOUD) AND flags.DUAL_SST_VALID'
sst_nadir_valid_mask = '!flags.LAND AND !(flags.NADIR_CLOUD OR flags.FWARD_CLOUD) AND flags.NADIR_SST_ONLY_VALID'

for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)
    _year  = int(date[0:4])
    _month = int(date[4:6])
    _day   = int(date[6:len(date)])
    _date_struct = (_year, _month, _day, 1, 0, 0, 0, 0, 1)

    # Wir wollen 7 zurueckliegende Tage prozessieren:
    days= make_date_array(_date_struct)
    
    for region in ['NorthSea', 'Baltic']:
        if region=="NorthSea":
            regiondestID= '_north_sea_'
            lat_min = "49.0"
            lat_max = "63.0"
            lon_min = "-5.0"
            lon_max = "13.0"
            l3binDB = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_aatsr_northsea.bindb'
            l3binningConf   = l3binningHome + 'l3binningConfAatsrMcNorthSea.xml'
        else:
            regiondestID= '_baltic_sea_'
            lat_min = "53.0"
            lat_max = "66.0"
            lon_min = "9.0"
            lon_max = "31.0"
            l3binDB = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_aatsr_balticsea.bindb'
            l3binningConf   = l3binningHome + 'l3binningConfAatsrMcBalticSea.xml'

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
        request_init_block = request_init_block +         '        <Parameter name=\"weight_coefficient.0\" value=\"0.5\" />\n'
        request_init_block = request_init_block +         '        <Parameter name=\"band_name.1\" value=\"' + bands[1] + '\" />\n'
        request_init_block = request_init_block +         '        <Parameter name=\"bitmask.1\" value=\"' + sst_nadir_valid_mask + '\" />\n'
        request_init_block = request_init_block +         '        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n'
        request_init_block = request_init_block +         '        <Parameter name=\"weight_coefficient.1\" value=\"0.5\" />\n'
        request_init_block = request_init_block +         '        <Parameter name=\"binning_algorithm.3\" value=\"Arithmetic Mean\" />\n'
        request_init_block = request_init_block +         '        <Parameter name=\"weight_coefficient.3\" value=\"0.5\" />\n'
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
                    print("Removing " + item + " from list.")
                    src_list.remove(item)
        
        list_size = len(src_list)
        
        # Jetzt nehmen wir nur die Produkte, die in der Liste days sind:
        proc_list  = {}
        proc_count = 0
        for item in src_list:
            for d in range(7):
                if item.find(days[d])>0:
                    print("Adding ", item, "to proc_list")
                    proc_list[proc_count]=item
                    proc_count=proc_count+1
                    break
        
        entry={}
        for item in proc_list:
            entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter
        
        # Jetzt geht's los:
        output_filename= destDir + days[6] + "_" + days[0] + regiondestID + "sst_aatsr_l3_1.2km.dim"
        
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

print("\n*****************************************************")
print(" Script \'process_AATSR_childs_L3_flux.py\' finished. ")
print("*****************************************************\n")

# EOF
