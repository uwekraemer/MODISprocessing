#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_wew_WAQS_childs.py

import os
import os.path
import sys
import time

print("\n************************************************")
print(" Script \'process_wew_WAQS_childs.py\' at work... ")
print("************************************************\n")

thetime   = time.localtime()
year_str  = str(thetime[0]) + "/"

# Verzeichnisse
baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
srcDir  = baseDir + 'waqs_child_temp/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/Level2/'

# tool config
wewHome   = '/home/uwe/tools/wew_water/'
wewScript = wewHome + 'wew-water.sh'
wewConf   = wewHome + 'water1.1.xml'

# konstante xml-bausteine fuer request
request_skeleton_1 =  "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n<RequestList>\n"
request_skeleton_1 += "    <Request type=\"WATER\">\n"
request_skeleton_1 += "        <Parameter name=\"output_format\" value=\"BEAM-DIMAP\" />\n"
request_skeleton_1 += "        <Parameter name=\"Normout\" value=\"false\" />\n"
request_skeleton_1 += "        <Parameter name=\"Extout\" value=\"true\" />\n"
request_skeleton_1 += "        <Parameter name=\"caseI\" value=\"false\" />\n"
request_skeleton_1 += "        <Parameter name=\"caseII\" value=\"true\" />\n"
request_skeleton_1 += "        <Parameter name=\"ozone_norm\" value=\"true\" />\n"
request_skeleton_1 += "        <Parameter name=\"ray_corr\" value=\"false\" />\n"
request_skeleton_1 += "        <InputProduct URL=\"file:"
input_delimiter    =                                                            "\" />\n"
request_skeleton2  =                       "        <OutputProduct URL=\"file:"
output_delimiter   =                                                            "\" format=\"BEAM-DIMAP\" />\n"
request_skeleton3  =                       "    </Request>\n"
request_skeleton3  = request_skeleton3 +   "</RequestList>\n"

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 oder Level2 sind:
for a in range(list_size):
    for item in src_list:
        if not item.startswith('MER') or item.startswith('MER_RR__0') or item.startswith('MER_RR__2'):
            print("Removing " + item + " from list.")
            src_list.remove(item)

# Jetzt geht's los:
for meris_file in src_list:    

    # MER_RR__1PNPDE20051126_053458_000011252042_00463_19555_0425.N1
    # 0         1         2         3         4         5         6
    # 01234567890123456789012345678901234567890123456789012345678901   

    #year  = meris_file[14:18]
    #month = meris_file[18:20]
    #day   = meris_file[20:22]
    
    acquisition_time = meris_file[14:29]
    orbit = meris_file[49:54]
    
    input_filename = srcDir + meris_file
    output_filename= destDir + acquisition_time + "_" + orbit + "_fw.dim"
    
    request = request_skeleton_1 + input_filename + input_delimiter + request_skeleton2 + output_filename + output_delimiter + request_skeleton3

    # Requestfile soll noch nicht existieren:
    if os.path.exists(wewConf):
        os.remove(wewConf)
    
    # Erst jetzt wird es erzeugt:
    requestfile = open(wewConf, 'a')
    requestfile.write(request)
    requestfile.close()

    wewCommand = wewScript + " " + wewConf
    print(wewCommand)
    print("Processing file " + meris_file + " ...")
    os.system(wewCommand)

print("\n************************************************")
print(" Script \'process_wew_WAQS_childs.py\' finished. ")
print("************************************************\n")

# EOF
