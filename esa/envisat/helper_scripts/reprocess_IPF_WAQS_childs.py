#!/usr/bin/env python
# -*- coding: latin-1 -*-
# file: process_IPF_WAQS_childs.py


import os
import os.path
import sys
import time
from shutil import rmtree

def printUsage():
    print("Usage: reprocess_IPF_WAQS_childs.py start_date end_date")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date")
    

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


print("\n**************************************************")
print(" Script \'reprocess_IPF_WAQS_childs.py\' at work... ")
print("**************************************************\n")

thetime   = time.localtime()
year_str  = str(thetime[0]) + "/"

# Verzeichnisse
baseDir = '/fs14/EOservices/Repositories/MERIS/RR/WAQSrepository/'
srcDir  = baseDir + start_date[0:4] + '/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily/2009/'

# tools config
pconvertTool   = '/home/uwe/tools/pconvert/pconvert.sh'
bandarithTool='/home/uwe/tools/BandArithBatch/BandArithBatch.sh'
bandarithParams = ' algal_12 \"l2_flags.WATER and !l2_flags.PCD_15 ? algal_1 : (l2_flags.WATER and !l2_flags.PCD_16 ? algal_2 : 0.00)\"'


for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)
    # Inputliste holen
    src_list = os.listdir(srcDir)
    list_size = len(src_list)

    # Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 oder Level2 sind:
    for a in range(list_size):
        for item in src_list:
            if not item.startswith('MER') or item.startswith('MER_RR__0') or item.startswith('MER_RR__1') or not item.find(date)>0:
                src_list.remove(item)
    
    # Jetzt geht's los:
    for meris_file in src_list:
        
        # MER_RR__1PNPDE20051126_053458_000011252042_00463_19555_0425.N1
        # 0         1         2         3         4         5         6
        # 01234567890123456789012345678901234567890123456789012345678901   
    
        # pconvert syntax: ./pconvert.sh -f dim -o ./ -b 17,18 <product>
        meris_file_path = srcDir + meris_file
        outputProductDataDir = destDir + meris_file[0:len(meris_file)-2] + 'data'
        if os.path.exists(outputProductDataDir):
            rmtree(outputProductDataDir)
        pconvertCommand = pconvertTool + ' -f dim -o ' + destDir + ' -b 16,17,18,33 ' + meris_file_path
        print("Processing file " + meris_file + " ...")
        os.system(pconvertCommand)
        
        pconvertOutputProduct = destDir + meris_file[0:60] +'dim'
        print(pconvertOutputProduct)
        # bandarith batch syntax:
        #<productName> [-d <destProductName>]<bandName> <expression> [<bandName> <expression>]
    
        bandarithCommand = bandarithTool + ' ' + meris_file_path + ' -d ' + pconvertOutputProduct + bandarithParams
        os.system(bandarithCommand)

print("\n************************************************")
print(" Script \'process_IPF_WAQS_childs.py\' finished. ")
print("************************************************\n")

# EOF
