#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: sync_with_DDS.py

import os
import os.path
import sys

def printUsage():
    print "Usage: sync_with_DDS.py archive"
    print "where archive includes:"
    print "\"ES\", \"KS\", or \"DDS\"\n"

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print "Archive specifier is missing!"
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if ((sys.argv[1]=="ES") or (sys.argv[1]=="KS") or (sys.argv[1]=="DDS")):
            print "\nSynchronising " + str(sys.argv[1]) + " products with local archive..."
        else:               # incorrect parameter
            print "Wrong archive specifier!"
            printUsage()
            sys.exit(1)
except:
    print "Error in parameters. Now exiting..."
    sys.exit(1)    

def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)


print "\n**************************************"
print " Script \'sync_with_DDS.py\' at work... "
print "**************************************\n"

baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
dbDir = baseDir + 'productsDB/'
destDir = baseDir + 'DDSdownload/'

if sys.argv[1]=="ES":
    tempDir = baseDir + 'RA_ES_temp/'
elif sys.argv[1]=="KS":
    tempDir = baseDir + 'RA_KS_temp/'
else:
    tempDir = baseDir + 'DDS_temp/'

ensurePathExists(tempDir)
ensurePathExists(destDir)

# Hier sollen vorab evtl. noch vorhandene gezippte Dateien gefunden werden.
# Gibt es welche, wird versucht, sie zu entpacken. Wenn das misslingt, wird das file geloescht.
dirList = os.listdir(tempDir)
numFiles = len(dirList)

for a in range(numFiles):
    for item in dirList:
        if not item.endswith('.gz'):
            dirList.remove(item)

num_zipped = len(dirList)
if num_zipped > 0:
    for item in dirList:
        file = tempDir+item
        print file
        call = 'gunzip ' + file
        try:
            ret=os.system(call)
            if ret==0:
                print 'File ' + file + ' deflated successfully.'
            else:
                 print 'File ' + file + ' could not be deflated. It will be deleted.'
                 os.remove(file)
        except:
            print 'Error occurred.'

# Verzeichnislisting neu einlesen
liste_temp = os.listdir(tempDir)
liste_size = len(liste_temp)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte sind:
for a in range(liste_size):
    for item in liste_temp:
        if item.startswith('MER')==0:
            liste_temp.remove(item)

for meris_file in liste_temp:    
    year=meris_file[14:18]
    month=meris_file[18:20]
    day=meris_file[20:22]
    
# DB:
    dbPath = dbDir + year + "/" + month + "/" + day + "/"
    ensurePathExists(dbPath)
    dbFile = dbPath + meris_file
    dbCommand = "touch " + dbFile
    
# Produkte:
    tempFile = tempDir + meris_file
    destFile = destDir + meris_file
    
    if not os.path.exists(dbPath): # wenn Tag noch nicht existiert
        os.makedirs(dbPath, 0777)
        print "day nicht"
    
    if not os.path.exists(dbFile):  # wenn das file noch nicht existiert und es in den InputPool verschoben werden soll
        print "renaming " + meris_file + " to " + destFile
        os.rename(tempFile, destFile)
        os.system(dbCommand)
    elif os.path.exists(dbFile):
        print "File " + meris_file + " exists already. Deleting..."
        os.remove(tempFile)

print "\n**************************************"
print " Script \'sync_with_DDS.py\' finished. "
print "**************************************\n"

#EOF
