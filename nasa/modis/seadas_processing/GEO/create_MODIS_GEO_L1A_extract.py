__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import listdir, makedirs, remove, system
from nasa.modis.seadas_processing.shared.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list, bzip2CompressFile, bzip2DecompressFile
from nasa.modis.seadas_processing.conf.paths import modisL1A_LACBasePath, modisGEOBasePath, modisL1A_subBasePath, modisGEO_subBasePath, seadasScriptsDir
from nasa.modis.seadas_processing.conf.params import west_lon_nsea_bsea as west_lon, east_lon_nsea_bsea as east_lon, south_lat_nsea_bsea as south_lat, north_lat_nsea_bsea as north_lat


def printUsage():
    print('Usage: create_MODIS_GEO_L1B.py date')
    print('where date is a string representing the date to process,')
    print('e.g. 20120607 for May 7, 2012.')


argc = len(argv)
if argc < 2:
    printUsage()
    exit(1)

_date  = str(argv[1])
_year  = _date[:4]
_month = _date[4:6]
_day   = _date[6:]
_doy   = getDOY(_year, _month, _day)

unzipped_extension = '.L1A_LAC.x.hdf'
zipped_extension = unzipped_extension + '.bz2'

print(_year, _month, _day, _doy)

modisL1A_LACPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1A_LACBasePath + _year) + _month) + _day)
modisL1A_subPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1A_subBasePath + _year) + _month) + _day)
modisGEOPath     = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisGEOBasePath     + _year) + _month) + _day)
modisGEO_subPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisGEO_subBasePath + _year) + _month) + _day)

for _path in [modisL1A_subPath, modisGEOPath, modisGEO_subPath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)

srcList = listdir(modisL1A_LACPath)
listSize = len(srcList)
print(listSize)

if not listSize:
    print("Nothing to do. Now exiting...")
    exit(1)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        _remove = False
        if not item.startswith('A' + _year +str(_doy)) or not item.find(unzipped_extension):
            _remove=True

        if item.endswith(unzipped_extension) or item.endswith(zipped_extension):
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

modisGEOscript        = seadasScriptsDir + 'modis_GEO.py'
modisL1AextractScript = seadasScriptsDir + 'modis_L1A_extract.py'

def process_modisGEO(l1a_productPath, GEO_productPath):
    processing_call = modisGEOscript + ' ' + l1a_productPath + ' -o ' + GEO_productPath
    print("Executing: ",processing_call)
    system(processing_call)
    if exists(GEO_productPath):
        return 1    # success
    else:
        return 0

def process_modisL1A_extract(l1a_productPath):
    GEO_productPath = l1a_productPath.replace('L1A_LAC', 'GEO')
    GEO_sub_productPath = l1a_productPath.replace('L1A_LAC', 'GEO_sub')
    L1A_sub_productpath = l1a_productPath.replace('L1A_LAC', 'L1A_sub')
    processing_call = modisL1AextractScript + ' ' + l1a_productPath + ' -g ' + GEO_productPath + \
                      ' -w ' + str(west_lon) + \
                      ' -s ' + str(south_lat) + \
                      ' -e ' + str(east_lon) + \
                      ' -n ' + str(north_lat) + \
                      ' -o ' + L1A_sub_productpath + \
                      ' --extract_geo='+GEO_sub_productPath

    print("Executing: ", processing_call)
    system(processing_call)
    if exists(L1A_sub_productpath):
        return 1    # success
    else:
        return 0


#unix cmd = $SEADAS/run/scripts/modis_L1A_extract.py /fs14/EOservices/InputPool/MODISA/L1A_LAC/2012/05/30/A2012151003000.L1A_LAC
#           -g /fs14/EOservices/InputPool/MODISA/GEO/2012/05/30/A2012151003000.GEO
#           -w -15.0000 -s 47.0000 -e 12.0000 -n 64.0000
#           -o /fs14/EOservices/InputPool/MODISA/L1A_LAC/2012/05/30/A2012151003000.L1A_sub
#           --extract_geo=/fs14/EOservices/InputPool/MODISA/L1A_LAC/2012/05/30/A2012151003000.GEO_sub


for item in srcList:
    print('\n', item)
    zipped  = False
    _process = _process_GEO = False
    if item.endswith(unzipped_extension):
        zipped = False
        l1a_product = item
    elif item.endswith(zipped_extension):
        zipped = True
        l1a_product = item[:-4]
    acq_time = item[8:15]
    if acq_time > '050000' and acq_time < '220000':
        _process = True
    if _process:
        GEO_file = modisGEOPath + l1a_product.replace('L1A_LAC', 'GEO')
        L1A_sub_file = modisL1A_subPath + l1a_product.replace('L1A_LAC', 'L1B_sub')

        if exists(L1A_sub_file):                                            # all products ready
            print("Output " + L1A_sub_file + " exists already. Skipping.")
            continue
        if exists(GEO_file):                                                # only GEO file ready
            print("Output " + GEO_file + " exists already. Skipping.")
            _process_GEO = False
        else:
            _process_GEO = True

        if not zipped:
            print("Processing...")
            unzipped_item = modisL1A_LACPath + item
            if _process_GEO:
                _geo_success = process_modisGEO(l1a_productPath=unzipped_item, GEO_productPath=GEO_file)
                print(_geo_success)
            _l1a_sub_success = process_modisL1A_extract(l1a_productPath=unzipped_item)
            print(_l1a_sub_success)
#            _bzip2_success = bzip2CompressFile(unzipped_item, True)
#            print _bzip2_success, "Done."
        else:
            zipped_item = modisL1A_LACPath + item
            _bunzip_success = bzip2DecompressFile(zipped_item, False)
            print(_bunzip_success, "Done.")
            if _bunzip_success:
                unzipped_item = modisL1A_LACPath + item[:-4]
                if _process_GEO:
                    _geo_success = process_modisGEO(l1a_productPath=unzipped_item, GEO_productPath=GEO_file)
                    print(_geo_success)
                _l1a_sub_success = process_modisL1A_extract(l1a_productPath=unzipped_item)
                print(_l1a_sub_success)
                print("Removing " + unzipped_item + "...")
                remove(unzipped_item)
            else:
                print("Decompressing failed! Skipping product ", item, " ...")
                continue
    else:
        print("Night product. Skipping...")


