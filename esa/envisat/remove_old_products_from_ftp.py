#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: remove_old_waqs_products_from_ftp.py

#############################################################
# This script is dedicated to run on ftp.brockmann-consult.de
#############################################################
# Delete products if they are older than a specified amount of days

from os import listdir, remove, rmdir, walk
from os.path import join,split,getsize,getmtime
from time import time, localtime, strftime, ctime
from shutil import copy2, move

backdays = 32       # file age in days

now = time()

print("\n**********************************************************")
print(" Script \'remove_old_waqs_products_from_ftp.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("**********************************************************\n")

# These directories are being scanned for older files
sourceDirectories = ['/ftp/waqs-bsh/daily/',
                     '/ftp/waqs-bsh/daily_IPF/',
                     '/ftp/waqs-bsh/daily_FUB/',
                     '/ftp/waqs-bsh/running_weeklymean/',
                     '/ftp/waqs-uniold/WQ/'
                     ]

# The loop runs over all subdirectories of all items in the 'sourceDirectories' list.
# If the time of last modification of a file is older than the above specified amount
# of days, the file will be deleted.
#
for item in sourceDirectories:
    for root, dirs, files in walk(item, topdown=False):
        for file in files:
            filepath = join(root,file)
            filetime = getmtime(filepath)
            fileage = (now - filetime)/86400
            if fileage > backdays:
                print(filepath, " is " + "%d" % (fileage) + " days old and will be deleted.")
                remove(filepath)
        print(root,"\nDone examining files, trying to remove directory ", root)
        numFilesInDir = len(listdir(root))
        if numFilesInDir == 0:
            try:
                rmdir(root)
            except:
                print("Directory could not be removed. Might still be not empty.\n")
        else:
            print("Directory not empty. It will not be removed.")
    
 
print("\n*********************************************************")
print(" Script \'remove_old_waqs_products_from_ftp.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("*********************************************************\n")

# EOF

