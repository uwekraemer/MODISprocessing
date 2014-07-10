__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import listdir, makedirs, remove, system

from utils.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list, bzip2CompressFile, bzip2DecompressFile
from nasa.modis.seadas_processing.conf.paths import modisL2_subBasePath, modisL2_TSMBasePath
from bc.eodata.beam_processing.conf.paths import gptProcessor, TSM_graph_file


def printUsage():
    print('Usage: create_MODIS_TSM.py date')
    print('where date is a string representing the date to process,')
    print('e.g. 20120507 for May 7, 2012.')


argc = len(argv)
if argc < 2:
    printUsage()
    exit(1)

_date  = str(argv[1])
_year  = _date[:4]
_month = _date[4:6]
_day   = _date[6:]
_doy   = getDOY(_year, _month, _day)


modisL2_subPath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL2_subBasePath  + _year) + _month) + _day)
modisL2_TSMPath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL2_TSMBasePath  + _year) + _month) + _day)

print(_year, _month, _day, _doy)
print(modisL2_subPath, modisL2_TSMPath)

for _path in [modisL2_TSMPath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)

try:
    srcList = listdir(modisL2_subPath)
except OSError:
    print("Cannot open ", modisL2_subPath+ "! Now exiting...")
    exit(1)
else:
    listSize = len(srcList)
    print(listSize)


if not listSize:
    print("Nothing to do. Now exiting...")
    exit(1)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        _remove = False
        if not item.startswith('A' + _year +str(_doy)) or not item.find('.L2_sub'):
            _remove=True

        if item.endswith('L2_sub') or item.endswith('L2_sub.bz2'):
            _remove = False
        else:
            _remove=True

        if _remove:
            srcList.remove(item)

exit_on_empty_list(srcList)
srcList.sort()

print(srcList)
#exit(1)
# Now processing can start...

gpt = gptProcessor


def process_modisL2_TSM(l2_sub_productPath, L2_TSM_productpath):
    #/Applications/beam-4.10/bin/gpt.command /FastBuffer/tsm_computation/MODIS_TSMBandMerge.xml
    # -SsourceProduct=/Volumes/Oliphant/EOData/MODISA/L2_LAC/2010/01/01/A2010001110000.L2_LAC.x.hdf
    # -t /Volumes/Oliphant/EOData/MODISA/L2_TSM/2010/01/01/A2010001110000.L2_LAC.dim

    processing_call = gpt + ' ' + TSM_graph_file + ' -SsourceProduct=' + l2_sub_productPath + ' -t ' + L2_TSM_productpath

    print("Executing: ", processing_call)
    system(processing_call)
    if exists(L2_TSM_productpath):
        return True    # success
    else:
        return False

for item in srcList:
    zipped = False
    if item.endswith('L2_sub'):
        zipped = False
        l2_sub_product = item
    elif item.endswith('L2_sub.bz2'):
        zipped = True
        l2_sub_product = item[:-4]

    L2_TSM_file = modisL2_TSMPath + l2_sub_product.replace('L2_sub', 'L2_TSM') + '.dim'

    if exists(L2_TSM_file):
        print("Output " + L2_TSM_file + " exists already. Skipping.")
        continue
    else:
        print("Processing product " + l2_sub_product)
    
    if not zipped:
        print("Processing...")
        unzipped_item = modisL2_subPath + item
        success = process_modisL2_TSM(l2_sub_productPath=unzipped_item, L2_TSM_productpath=L2_TSM_file)
        print("Success: " + str(success))
        _bzip2_success = bzip2CompressFile(unzipped_item, True)
        print(_bzip2_success, "Done.")
    else:
        zipped_item = modisL2_subPath + item
        _bunzip_success = bzip2DecompressFile(zipped_item, False)
        print(_bunzip_success, "Done.")
        if _bunzip_success:
            unzipped_item = modisL2_subPath + item[:-4]
            success = process_modisL2_TSM(l2_sub_productPath=unzipped_item, L2_TSM_productpath=L2_TSM_file)
            print("Success: "+ str(success))
            print("Removing " + unzipped_item + "...")
            remove(unzipped_item)
        else:
            print("Decompressing failed! Skipping product ", item, " ...")
            continue

