__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import listdir, makedirs, remove, system

from utils.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list, bzip2CompressFile, bzip2DecompressFile
from nasa.modis.seadas_processing.conf.paths import modisL1A_LACBasePath, modisGEOBasePath, modisL1B_LACBasePath, \
                                                   modisL1B_HKMBasePath, modisL1B_QKMBasePath, modisL1B_OBCBasePath, \
                                                   seadasScriptsDir


def printUsage():
    print 'Usage: create_MODIS_GEO_L1B.py date'
    print 'where date is a string representing the date to process,'
    print 'e.g. 20120607 for June 7, 2012.'


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
modisGEOPath     = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisGEOBasePath     + _year) + _month) + _day)
modisL1B_LACPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_LACBasePath + _year) + _month) + _day)
modisL1B_HKMPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_HKMBasePath + _year) + _month) + _day)
modisL1B_QKMPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_QKMBasePath + _year) + _month) + _day)
modisL1B_OBCPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_OBCBasePath + _year) + _month) + _day)

for _path in [modisGEOPath, modisL1B_LACPath, modisL1B_HKMPath, modisL1B_QKMPath, modisL1B_OBCPath]:
    if not exists(_path):
        print "Making directory: ", _path, " ..."
        makedirs(_path)

try:
    srcList = listdir(modisL1A_LACPath)
except OSError:
    print "Cannot open ", modisL1A_LACPath+ "! Now exiting..."
    exit(1)
else:
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
modisL1Bscript = seadasScriptsDir + 'modis_L1B.py'

def process_modisGEO(l1a_productPath, GEO_productPath):
    processing_call = modisGEOscript + ' ' + l1a_productPath + ' -o ' + GEO_productPath
    print "Executing: ",processing_call
    system(processing_call)
    if exists(GEO_productPath):
        return 1    # success
    else:
        return 0

def process_modisL1B(l1a_productPath):
    GEO_productPath = l1a_productPath.replace('L1A_LAC', 'GEO')
    L1B_productpath = l1a_productPath.replace('L1A_LAC', 'L1B_LAC')
    HKM_productPath = l1a_productPath.replace('L1A_LAC', 'L1B_HKM')
    QKM_productPath = l1a_productPath.replace('L1A_LAC', 'L1B_QKM')
    processing_call = modisL1Bscript + ' ' + l1a_productPath + ' ' + GEO_productPath + \
                      ' -o ' + L1B_productpath + \
                      ' -k ' + HKM_productPath + \
                      ' -q ' + QKM_productPath + \
                      ' --del-hkm --del-qkm'

    print "Executing: ", processing_call
    system(processing_call)
    if exists(L1B_productpath):
        return 1    # success
    else:
        return 0

for item in srcList:
    print '\n', item
    zipped = False
    if item.endswith('L1A_LAC'):
        zipped = False
        l1a_product = item
    elif item.endswith('L1A_LAC.bz2'):
        zipped = True
        l1a_product = item[:-4]

    GEO_file = modisGEOPath + l1a_product.replace('L1A_LAC', 'GEO')
    L1B_file = modisL1B_LACPath + l1a_product.replace('L1A_LAC', 'L1B_LAC')

    if exists(L1B_file):
        print "Output " + L1B_file + " exists already. Skipping."
        continue

    if not zipped:
        print "Processing..."
        unzipped_item = modisL1A_LACPath + item
        _geo_success = process_modisGEO(l1a_productPath=unzipped_item, GEO_productPath=GEO_file)
        print _geo_success
        _l1b_success = process_modisL1B(l1a_productPath=unzipped_item)
        print _l1b_success
        _bzip2_success = bzip2CompressFile(unzipped_item, True)
        print _bzip2_success, "Done."
    else:
        zipped_item = modisL1A_LACPath + item
        _bunzip_success = bzip2DecompressFile(zipped_item, False)
        print _bunzip_success, "Done."
        if _bunzip_success:
            unzipped_item = modisL1A_LACPath + item[:-4]
            _geo_success = process_modisGEO(l1a_productPath=unzipped_item, GEO_productPath=GEO_file)
            print _geo_success
            _l1b_success = process_modisL1B(l1a_productPath=unzipped_item)
            print _l1b_success
            print "Removing " + unzipped_item + "..."
            remove(unzipped_item)
        else:
            print "Decompressing failed! Skipping product ", item, " ..."
            continue
