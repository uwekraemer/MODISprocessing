#!/usr/bin/env python3

__author__ = 'uwe'

from sys import argv
from os import listdir
from os.path import basename, isfile
from ftplib import FTP, all_errors

from utils.utilities import ensureTrailingSlash, exit_on_empty_list
from nasa.modis.seadas_processing.conf.paths import modisL3_TSM_UTM_QLPath


def printUsage():
    print("Usage: ", argv[0], "<backDay>")
    print("where backDay is a string representing the day for data upload,")
    print("e.g. 20131010")

def findMissingItemsInDestinationList(list1, list2):
    missingItems=[]
    for item in list1:
        if not item in list2:
            # print(item, 'missing.')
            missingItems.append(item)
    return missingItems

def findMissingItemsInSourceList(list1, list2):
    missingItems=[]
    for item in list2:
        if not item in list1:
            # print(item, 'missing.')
            missingItems.append(item)
    return missingItems

if len(argv) != 2:
    printUsage()
    exit(1)

_backdate = argv[1]
if len(_backdate) != 8:
    print("****************************")
    print("* year parameter malformed *")
    print("****************************")
    printUsage()
    exit(1)

_year = _backdate[:4]
print _year
param = 'chl'

modisL3_UTM_QLPath = ensureTrailingSlash(modisL3_TSM_UTM_QLPath  + _year)

srcList = listdir(modisL3_UTM_QLPath)
listSize = len(srcList)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        if not item.startswith('cb_ns_' + param + '_') or not item.find(_backdate) > 1 or not item.endswith('_eo_bc.png'):
            print("Removing " + item + ' from list.')
            srcList.remove(item)

exit_on_empty_list(srcList)
srcList.sort()
print(srcList)


ftpHost = 'data.waterinsight.nl'
ftpUser = 'colbios'
ftpPass = 'C0lbi0sc00p'
dataDir = '/CoBIOS/BC/'

try:
    ftp = FTP(ftpHost, ftpUser, ftpPass)    #login
except all_errors:
    print("unable to connect to the ftp-server")
    exit(1)

try:
    ftpList = ftp.nlst(dataDir)                #Liste der files erstellen
except all_errors:
    print("directory does not exist on the ftp-server")
    exit(1)

# print(ftpList)

dstList = [basename(item) for item in ftpList]
print("Images on destination:", dstList)

missingUploads = findMissingItemsInDestinationList(srcList, dstList)
print("There are " + str(len(missingUploads)) + " items missing:")
print(missingUploads)

# ftp.retrbinary('RETR '+ftp_meris_file, open(real_meris_file, 'wb').write)

for item in missingUploads:
    fileToUpload = modisL3_UTM_QLPath + item
    if isfile(fileToUpload):
        print("Uploading ", fileToUpload + "...")
        ftp.storbinary('STOR ' + dataDir + item, open(fileToUpload, 'rb'))
    else:
        continue

ftp.quit()
