#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: reprocess_wew_weekly_L3.py

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
    print("Each date in the interval [start_date; end_date] results in an array")
    print("of dates to be processed.")
    print("NOTE: start_date and end_date represent the last date")
    print("included in the weekly mean!")

def make_date_array(start_tupel):
    float_start_date = time.mktime(start_tupel)
    result=[]
    result.append(str(start_tupel[0]) + str(start_tupel[1]).rjust(2,'0') + str(start_tupel[2]).rjust(2,'0'))
    for i in range(6):
        date_tupel=time.gmtime(float_start_date - (i)*24*60*60)    
        date_str = str(date_tupel[0]) + str(date_tupel[1]).rjust(2,'0') + str(date_tupel[2]).rjust(2,'0')
        result.append(date_str)
        print("date_str", date_str)
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

# Verzeichnisse
srcDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily_merged_BSH_Indicator/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/weekly/'

# tools config
l3binningHome    = '/home/uwe/tools/l3binning/'
l3binningScript  = l3binningHome + 'l3binning.sh'
l3BinningBaseDir = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/'

l3BandArithBatchHome   = '/home/uwe/tools/BandArithBatch/'
l3BandArithBatchScript = l3BandArithBatchHome + 'BandArithBatch.sh'

grid_cell_size = "1.2"
#chl_bitmask = "not result_flags.CHL_IN and not result_flags.CHL_OUT and algal_2 != 5"
#ys_bitmask  = "not result_flags.YEL_IN and not result_flags.YEL_OUT and yellow_subs != 5"
#tsm_bitmask = "not result_flags.TSM_IN and not result_flags.TSM_OUT and total_susp != 5"
chl_bitmask = "algal_concentration_flags != 0"
ys_bitmask  = "yellow_subs_absorption_flags != 0"        
tsm_bitmask = "total_susp_concentration_flags != 0"

for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)
    _year  = int(date[0:4])
    _month = int(date[4:6])
    _day   = int(date[6:len(date)])
    _date_struct = (_year, _month, _day, 1, 0, 0, 0, 0, 1)
  
    
   

    # Wir wollen 7 zurueckliegende Tage prozessieren:
    days= make_date_array(_date_struct)

    for region in ['NorthSea']:
#    for region in ['NorthSea', 'BalticSea', 'Estonia', 'UK']:
        if region=="NorthSea":
            regiondestID = 'north_sea'
            lat_min = "49.0"
            lat_max = "63.0"
            lon_min = "-5.0"
            lon_max = "13.0"
            l3binningConf = l3binningHome    + 'l3binningConfNorthSea.xml'
            l3BinningDb   = l3BinningBaseDir + 'l3_database_wew_northsea_r.bindb'
        elif region=="BalticSea":
            regiondestID = 'baltic_sea'
            lat_min = "53.0"
            lat_max = "66.0"
            lon_min = "9.0"
            lon_max = "31.0"
            l3binningConf = l3binningHome    + 'l3binningConfBaltic.xml'
            l3BinningDb   = l3BinningBaseDir + 'l3_database_wew_balticsea_r.bindb'
        elif region=="Estonia":
            regiondestID = 'estonia'
            lat_min = "57.058884"
            lat_max = "60.57032"
            lon_min = "21.702216"
            lon_max = "30.225435"
            l3binningConf = l3binningHome    + 'l3binningConfEstonia.xml'
            l3BinningDb   = l3BinningBaseDir + 'l3_database_wew_estonia_r.bindb'
        else:
            regiondestID = 'uk'
            lat_min = "48.0"
            lat_max = "62.0"
            lon_min = "-13.0"
            lon_max = "9.0"
            l3binningConf = l3binningHome    + 'l3binningConfUnitedKingdom.xml'
            l3BinningDb   = l3BinningBaseDir + 'l3_database_wew_unitedkingdom_r.bindb'
        
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
        request_init_block     += "        <Parameter name=\"band_name.0\" value=\"algal_concentration_flags\" />\n"
        request_init_block     += "        <Parameter name=\"bitmask.0\" value=\""+ chl_bitmask + "\" />\n"
        request_init_block     += "        <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n"
        request_init_block     += "        <Parameter name=\"weight_coefficient.0\" value=\"0.5\" />\n"
        request_init_block     += "        <Parameter name=\"band_name.1\" value=\"yellow_subs_absorption_flags\" />\n"
        request_init_block     += "        <Parameter name=\"bitmask.1\" value=\""+ ys_bitmask + "\" />\n"
        request_init_block     += "        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n"
        request_init_block     += "        <Parameter name=\"weight_coefficient.1\" value=\"0.5\" />\n"
        request_init_block     += "        <Parameter name=\"band_name.2\" value=\"total_susp_concentration_flags\" />\n"
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
        print("list_size", list_size)
        # Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 oder Level2 sind:
        for a in range(list_size):
            for item in src_list:
                if item.endswith('.data')==1 :
                    print("Removing " + item + " from list.")
                    src_list.remove(item)
        
        list_size = len(src_list)
  
        
        num_days  = len(days)
        
        # Jetzt nehmen wir nur die Produkte, die in der Liste previous_days sind:
        proc_list  = {}
        proc_count = 0
        for item in src_list:
            for d in range(num_days):
                if item.startswith(days[d])==1:
                    print(days[d]+" found in "+ item)
                    print("Adding ", item, "to proc_list")
                    proc_list[proc_count]=item
                    proc_count=proc_count+1
                    print("proc_count", proc_count)
                    break
        
        entry={}
        for item in proc_list:
            entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter
        
        if len(proc_list) == 0:
            print("Nothing to do. Now quitting.")
            sys.exit(1)
        
        output_filename= destDir + days[6]+"_" + days[0]+ "_wew_" + regiondestID + "_l3_" + grid_cell_size+"km.dim"
      
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
  #      os.system(l3binningCommand)
        
        # Postprocessing:
        l3BandArithBatchParams  = "algal_concentration \"algal_2_mean==0.0?0:exp10(algal_2_mean)\" "
        l3BandArithBatchParams += "total_susp_concentration \"total_susp_mean==0.0?0:exp10(total_susp_mean)\" "
        l3BandArithBatchParams += "yellow_subs_absorption \"yellow_subs_mean==0.0?0:exp10(yellow_subs_mean)\""
        
        l3BandArithBatchCommand = l3BandArithBatchScript + " " + output_filename + " " + l3BandArithBatchParams
        print("Postprocessing L3...")
   #     os.system(l3BandArithBatchCommand)

print("\n**********************************************")
print(" Script \'process_wew_weekly_L3.py\' finished. ")
print("**********************************************\n")

# EOF
