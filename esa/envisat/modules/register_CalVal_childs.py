#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: register_CalVal_childs.py

from os import listdir, makedirs, system
from os.path import exists
from sys import argv, exit
from time import localtime

def printUsage():
    print("Usage: register_CalVal_childs.py sensor type")
    print("where sensor includes:")
    print("\"AATSR\"  or  \"MERIS\"\n")
    print("and type must be \"NR\" or \"TOA\" for AATSR")
    print("and \"RR\" for MERIS.")

try:
    argc=len(argv)
    if argc < 3:          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        exit(1)
    else:                   # we have also received parameters
        sensor = argv[1]
        productType = argv[2]
        if sensor in ["AATSR", "MERIS"] and productType in ["NR", "TOA", "RR"]:    #TODO: handle wrong combinations properly!
            # do something
            print("\nRegistering " + sensor + " childs for CalVal...")
        else:               # incorrect parameters
            print("Wrong parameters!")
            printUsage()
            exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    exit(1)    

print("\n***********************************************")
print(" Script \'register_CalVal_childs.py\' at work... ")
print("***********************************************\n")

if sensor == "AATSR":
    product_id = 'ATS'
    initialIncomingDir = '/fs14/EOservices/InputPool/AATSR/'
    baseDir = initialIncomingDir + productType + '/'
    initialDestDir = '/CalValRepositories/AATSR/'
    destDir = initialDestDir + productType + '/'
else:
    product_id = 'MER'
    baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
    destDir = '/CalValRepositories/MERIS/RR/'

srcDir  = baseDir + 'calval_child_temp/'

thetime   = localtime()
year_str  = str(thetime[0]) + "/"


prodregHome   = '/home/uwe/tools/prodreg1.5.3/'
prodregScript = prodregHome + 'prodreg.sh'
prodregConf   = prodregHome + 'config.properties'

src_list = listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 sind:
for a in range(list_size):
    for item in src_list:
        if not item.startswith(product_id):
            print("Removing " + item + " from list.")
            src_list.remove(item)


for product_file in src_list:
    # 01234567890123456789012345678901234567890123456789012345678901
    # ATS_NR__2PNMAP20060914_103214_000003362051_00137_23738_0001.N1
    # MER_RR__2PQBCM20030514_104937_000002002016_00223_06289_0002.N1
    year  = product_file[14:18]
    month = product_file[18:20]
    
    destMonthPath = destDir + year + "/" + month
    phys_product_file = srcDir + product_file
    #print destPath, phys_product_file
    
    if not exists(destMonthPath): 
        makedirs(destMonthPath)
        print("New date.")
    
    # prodreg-Syntax:
    # ./prodreg.sh -c config_dds.properties -e -m -q -t -s DDS -o <outputDir> <products>    
    prodregCommand = prodregScript + " -c " + prodregConf + " -m -e -q -t -s CalVal -o " + destMonthPath +" " + phys_product_file
    print(prodregCommand)
    system(prodregCommand)


print("\n***********************************************")
print(" Script \'register_CalVal_childs.py\' finished.  ")
print("***********************************************\n")

# EOF
