__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import listdir, makedirs, remove, system

from utils.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list, bzip2CompressFile, bzip2DecompressFile
from nasa.modis.seadas_processing.conf.paths import modisL1A_subBasePath, modisGEO_subBasePath, modisL1B_subBasePath, \
                                                   modisL1B_HKMBasePath, modisL1B_QKMBasePath, modisL1B_OBCBasePath, \
                                                   seadasScriptsDir


def printUsage():
    print 'Usage: create_MODIS_L1B_sub.py date'
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

modisL1A_subPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1A_subBasePath + _year) + _month) + _day)
modisGEO_subPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisGEO_subBasePath + _year) + _month) + _day)

modisL1B_subPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_subBasePath + _year) + _month) + _day)
modisL1B_HKMPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_HKMBasePath + _year) + _month) + _day)
modisL1B_QKMPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_QKMBasePath + _year) + _month) + _day)
modisL1B_OBCPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_OBCBasePath + _year) + _month) + _day)

for _path in [modisL1B_subPath, modisL1B_HKMPath, modisL1B_QKMPath, modisL1B_OBCPath]:
    if not exists(_path):
        print "Making directory: ", _path, " ..."
        makedirs(_path)

try:
    srcList = listdir(modisL1A_subPath)
except OSError:
    print "Cannot open ", modisL1A_subPath+ "! Now exiting..."
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
        if not item.startswith('A' + _year +str(_doy)) or not item.find('.L1A_sub'):
            _remove=True

        if item.endswith('L1A_sub') or item.endswith('L1A_sub.bz2'):
            _remove = False
        else:
            _remove=True

        if _remove:
            srcList.remove(item)

exit_on_empty_list(srcList)
srcList.sort()

# Now processing can start...

modisL1Bscript = seadasScriptsDir + 'modis_L1B.py'
print exists(modisL1Bscript)

def process_modisL1B_sub(l1a_sub_productPath):
    GEO_sub_productPath = l1a_sub_productPath.replace('L1A_sub', 'GEO_sub')
    L1B_sub_productpath = l1a_sub_productPath.replace('L1A_sub', 'L1B_sub')
    HKM_productPath = l1a_sub_productPath.replace('L1A_sub', 'L1B_HKM')
    QKM_productPath = l1a_sub_productPath.replace('L1A_sub', 'L1B_QKM')
    OBC_productPath = l1a_sub_productPath.replace('L1A_sub', 'L1B_OBC')
    processing_call = modisL1Bscript + ' ' + l1a_sub_productPath + ' ' + GEO_sub_productPath + \
                      ' -o ' + L1B_sub_productpath + \
                      ' -k ' + HKM_productPath + \
                      ' -q ' + QKM_productPath + \
                      ' -c ' + OBC_productPath + \
                      ' --del-hkm --del-qkm'

    print "Executing: ", processing_call
    system(processing_call)
    if exists(L1B_sub_productpath):
        return 1    # success
    else:
        return 0

for item in srcList:
    print '\n', item
    zipped = False
    if item.endswith('L1A_sub'):
        zipped = False
        l1a_sub_product = item
    elif item.endswith('L1A_sub.bz2'):
        zipped = True
        l1a_sub_product = item[:-4]

    L1B_sub_file = modisL1B_subPath + l1a_sub_product.replace('L1A_sub', 'L1B_sub')

    if exists(L1B_sub_file):
        print "Output " + L1B_sub_file + " exists already. Skipping."
        continue

    if not zipped:
        print "Processing..."
        unzipped_item = modisL1A_subPath + item
        success = process_modisL1B_sub(l1a_sub_productPath=unzipped_item)
        print success
        _bzip2_success = bzip2CompressFile(unzipped_item, True)
        print _bzip2_success, "Done."
    else:
        zipped_item = modisL1A_subPath + item
        _bunzip_success = bzip2DecompressFile(zipped_item, False)
        print _bunzip_success, "Done."
        if _bunzip_success:
            unzipped_item = modisL1A_subPath + item[:-4]
            success = process_modisL1B_sub(l1a_sub_productPath=unzipped_item)
            print success
            print "Removing " + unzipped_item + "..."
            remove(unzipped_item)
        else:
            print "Decompressing failed! Skipping product ", item, " ..."
            continue

