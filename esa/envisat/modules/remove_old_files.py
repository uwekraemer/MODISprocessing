#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: remove_old_files.py
# Delete products if they are older than a specified amount of days

from os import listdir, remove, rmdir, walk
from os.path import join,split,getsize,getmtime
from time import time, localtime, strftime, ctime

print("\n*****************************************")
print(" Script \'remove_old_files.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("*****************************************\n")

backdays = 5       # file age in days
now = time()

# These directories are being scanned for older files
sourceDirectories = ['/fs14/EOservices/InputPool/AATSR/NR/RA_temp/',
                     '/fs14/EOservices/InputPool/AATSR/TOA/RA_temp/'
                     ]

# The loop runs over all subdirectories of all items in the 'sourceDirectories' list.
# If the time of last modification of a file is older than the above specified amount
# of days, the file will be deleted.

for item in sourceDirectories:
    for root, dirs, files in walk(item, topdown=False):
        for file in files:
            filepath = join(root,file)
            filetime = getmtime(filepath)
            fileage = (now - filetime)/86400
            if fileage >= backdays:
                print(filepath, " is " + "%d" % (fileage) + " days old and will be deleted.")
                remove(filepath)

print("\n****************************************")
print(" Script \'remove_old_files.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("****************************************\n")

# EOF
