#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_old_products_to_attic.py

# Put products to the attic if they are older than a specified amount of days
# Script assumes that there is a directory 'Attic' on the same level as 'OutputPool'.

import os
import sys
from os.path import join,split,getsize,getmtime
from time import time, localtime, strftime, ctime
from shutil import copy2, move

backdays = 50       # file age

now = time()

print "\n**************************************************"
print " Script \'put_old_products_to_attic.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "**************************************************\n"

# These directories are being scanned for older files
sourceDirectories = ['/fs14/EOservices/InputPool/MERIS/L3_netCDF/meris_chl12/',
                     '/fs14/EOservices/InputPool/MERIS/L3_netCDF/meris_spm',
                     '/fs14/EOservices/InputPool/MERIS/L3_netCDF/meris_trans12',
                     '/fs14/EOservices/InputPool/MERIS/L3_netCDF/meris_ys',
                     '/fs14/EOservices/InputPool/MODIS/L3_netCDF/modis_chla',
                     '/fs14/EOservices/InputPool/AATSR/NR/waqs_child_temp',
                     '/fs14/EOservices/OutputPool/AATSR/',
                     '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-caseR/',
                     '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/',
                     '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily/',
                     '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/',
                     '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/',
                     '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/',
                     '/fs14/EOservices/OutputPool/MERIS/RR/L1b-Estonia/',
                     '/fs14/EOservices/OutputPool/MODIS/WAQS-MC/daily/'
                     ]

# The loop runs over all subdirectories of all items in the 'sourceDirectories' list.
# If the time of last modification of a file is older than the above specified amount
# of days, the file will be moved to the attic. The path to the file moved to the attic
# is constructed such that the directory name 'OutputPool' is replaced by 'Attic'. 
# Thus, the original directory structure will be kept. 
#
for item in sourceDirectories:
    for root, dirs, files in os.walk(item, topdown=False):
        for file in files:
            filepath = join(root,file)
            filetime = getmtime(filepath)
            fileage = (now - filetime)/86400
            if fileage > backdays:
                print filepath, " is " + "%d" % (fileage) + " days old."
                if filepath.find('InputPool') > 0:
                    attic_path = split(filepath.replace('InputPool','Attic'))[0]
                else:
                    attic_path = split(filepath.replace('OutputPool','Attic'))[0]
                attic_file = join(attic_path, file)
                try:
                    if not os.path.exists(attic_path):
                        print "Trying to create attic directory " + attic_path + " ..."
                        try:
                            os.makedirs(attic_path, 0777)
                        except:
                            print 'Could not create attic directory ' + attic_path + "."
                            sys.exit(1)    
                    print "Moving " + file + " to " + attic_file + " ..."
                    move(filepath, attic_file)
                except:
                    print 'Could not move ' + file + " to " + attic_file + "."
                    sys.exit(1)
        print root,"\nDone examining files, trying to remove directory ", root
        numFilesInDir = len(os.listdir(root))
        if numFilesInDir == 0:
            try:
                os.rmdir(root)
            except:
                print "Directory could not be removed. Might still be not empty.\n"
        else:
            print "Directory not empty. It will not be removed."
    
 
print "\n*************************************************"
print " Script \'put_old_products_to_attic.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "*************************************************\n"

# EOF