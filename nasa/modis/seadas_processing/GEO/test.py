__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import listdir, makedirs, remove, system

from utils.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list
from nasa.modis.seadas_processing.conf.paths import modisL1A_LACBasePath, modisGEOBasePath, seadasScriptsDir

#from bz2 import compress, decompress

def printUsage():
    print 'Usage: create_MODIS_GEO.py date'
    print 'where date is a string representing the date to process,'
    print 'e.g. 20120607 for May 7, 2012.'


argc = len(argv)
if argc < 2:
    printUsage()
    exit(1)

_date  = str(argv[1])
_year  = _date[:4]
_month = _date[4:6]
_day   = _date[6:]
_doy   = getDOY(_year, _month, _day)

print _year, _month, _day, _doy

modisL1A_LACPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1A_LACBasePath + _year) + _month) + _day)
modisGEOPath     = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisGEOBasePath + _year) + _month) + _day)

srcList = listdir(modisL1A_LACPath)
listSize = len(srcList)
print listSize

if not listSize:
    print "Nothing to do. Now exiting..."
    exit(1)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        _remove = False
        if not item.startswith('A' + _year +str(_doy)) or not item.find('.L1A_LAC'):
            _remove=True

        if item.endswith('L1A_LAC') or item.endswith('L1A_LAC.bz2'):
            _remove = False
        else:
            _remove=True

        if _remove:
            srcList.remove(item)

exit_on_empty_list(srcList)
srcList.sort()

# Now processing can start...

if not exists(modisGEOPath):
    makedirs(modisGEOPath)

modisGEOscript = seadasScriptsDir + 'modis_GEO.py'
print exists(modisGEOscript)

def process_modisGEO(l1a_productPath, GEO_productPath):
    processing_call = modisGEOscript + ' ' + l1a_productPath + ' -o ' + GEO_productPath
    print processing_call
    return system(processing_call)

for item in srcList:
    print '\n', item
    zipped = False
    if item.endswith('L1A_LAC'):
        zipped = False
        GEO_file = modisGEOPath + item.replace('L1A_LAC', 'GEO')
    elif item.endswith('L1A_LAC.bz2'):
        zipped = True
        GEO_file = modisGEOPath + item[:-4].replace('L1A_LAC', 'GEO')

    if exists(GEO_file):
        print "Output " + GEO_file + " exists already. Skipping."
        continue


    if not zipped:
        print "Processing..."
        unzipped_item = modisL1A_LACPath + item
        success = process_modisGEO(l1a_productPath=unzipped_item, GEO_productPath=GEO_file)
        print success
        print "Compressing " + unzipped_item + " ..."
        bz_cmd = 'bzip2 -f ' + unzipped_item
        system(bz_cmd)
        print "Done."
    else:
        zipped_item = modisL1A_LACPath + item
        bunzip_cmd = 'bunzip2 -k ' + zipped_item
        print "Decompressing " + zipped_item + " ..."
        bunzip_success=system(bunzip_cmd)
        print bunzip_success
        print "Done."
        if not bunzip_success:
            unzipped_item = modisL1A_LACPath + item[:-4]
            success = process_modisGEO(l1a_productPath=unzipped_item, GEO_productPath=GEO_file)
            print success
            print "Removing " + unzipped_item + "..."
            remove(unzipped_item)
        else:
            print "Decompressing failed! Skipping product ", item, " ..."
            continue

