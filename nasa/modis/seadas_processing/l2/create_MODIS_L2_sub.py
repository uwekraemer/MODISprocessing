__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import chdir, listdir, makedirs, remove, system

from utils.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list, bzip2DecompressFile
from nasa.modis.seadas_processing.conf.paths import modisL1B_subBasePath, modisGEO_subBasePath, modisL2_subBasePath, seadasScriptsDir, seadasBinDir
from nasa.modis.seadas_processing.conf.params import l2gen_const_params


def printUsage():
    print 'Usage: create_MODIS_L2_sub.py date'
    print 'where date is a string representing the date to process,'
    print 'e.g. 20120507 for May 7, 2012.'


argc = len(argv)
if argc < 2:
    printUsage()
    exit(1)

_date  = str(argv[1])
_year  = _date[:4]
_month = _date[4:6]
_day   = _date[6:]
_doy   = getDOY(_year, _month, _day)


modisL1B_subPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_subBasePath + _year) + _month) + _day)
modisGEO_subPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisGEO_subBasePath + _year) + _month) + _day)
modisL2_subPath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL2_subBasePath  + _year) + _month) + _day)

print _year, _month, _day, _doy
print l2gen_const_params
print modisL1B_subPath, modisGEO_subPath, modisL2_subPath

for _path in [modisL2_subPath]:
    if not exists(_path):
        print "Making directory: ", _path, " ..."
        makedirs(_path)

try:
    srcList = listdir(modisL1B_subPath)
except OSError:
    print "Cannot open ", modisL1B_subPath+ "! Now exiting..."
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
        if not item.startswith('A' + _year +str(_doy)) or not item.find('.L1B_sub'):
            _remove=True

        if item.endswith('L1B_sub') or item.endswith('L1B_sub.bz2'):
            _remove = False
        else:
            _remove=True

        if _remove:
            srcList.remove(item)

exit_on_empty_list(srcList)
srcList.sort()

print srcList

# Now processing can start...

modisL2Binary = seadasBinDir + 'l2gen'
getancScript  = seadasScriptsDir + 'getanc.py'

print modisL2Binary, exists(modisL2Binary), getancScript, exists(getancScript)

def process_modisL2_sub(l1b_sub_productPath):
    GEO_sub_productPath = l1b_sub_productPath.replace('L1B_sub', 'GEO_sub')
    L2_sub_productpath1  = l1b_sub_productPath.replace('InputPool', 'OutputPool').replace('L1B_sub', 'L2_sub')
    ancfile_path = l1b_sub_productPath + '.anc'

    chdir(modisL1B_subPath)
    system(getancScript + " " + l1b_sub_productPath)
    if not exists(ancfile_path):
        print "getanc.py call failed. No information about ancillary data available. Skipping processing of product..."
        return False
    else:
        print "\ngetanc.py retrieved ancillary info successfully!\n"

    ancfile = open(ancfile_path, 'r')
    ancillary_info = ancfile.readlines()
    ancfile.close()

    par_file_path = L2_sub_productpath1 + '.par'
    par_file = open(par_file_path, 'w')
    par_file.write('ifile='+l1b_sub_productPath+'\n')
    par_file.write('geofile='+GEO_sub_productPath+'\n')
    par_file.write('ofile1='+L2_sub_productpath1+'\n')
    #par_file.write('ofile2='+L2_sub_productpath2+'\n')
    par_file.write(l2gen_const_params)
    par_file.writelines(ancillary_info)
    par_file.close()
    print par_file_path

    processing_call = modisL2Binary + ' par=' + par_file_path

    print "Executing: ", processing_call
    system(processing_call)
    if exists(L2_sub_productpath1): # and exists(L2_sub_productpath2):
        return True    # success
    else:
        return False

for item in srcList:
    zipped = False
    if item.endswith('L1B_sub'):
        zipped = False
        l1b_sub_product = item
    elif item.endswith('L1B_sub.bz2'):
        zipped = True
        l1b_sub_product = item[:-4]

    L2_sub_file = modisL2_subPath + l1b_sub_product.replace('L1B_sub', 'L2_sub')

    if exists(L2_sub_file):
        print "Output " + L2_sub_file + " exists already. Skipping."
        continue
    else:
        print "Processing product " + l1b_sub_product
    
    if not zipped:
        print "Processing..."
        unzipped_item = modisL1B_subPath + item
        success = process_modisL2_sub(l1b_sub_productPath=unzipped_item)
        print success
#        _bzip2_success = bzip2CompressFile(unzipped_item, True)
#        print _bzip2_success, "Done."
    else:
        zipped_item = modisL1B_subPath + item
        _bunzip_success = bzip2DecompressFile(zipped_item, False)
        print _bunzip_success, "Done."
        if _bunzip_success:
            unzipped_item = modisL1B_subPath + item[:-4]
            success = process_modisL2_sub(l1b_sub_productPath=unzipped_item)
            print success
            print "Removing " + unzipped_item + "..."
            remove(unzipped_item)
        else:
            print "Decompressing failed! Skipping product ", item, " ..."
            continue

