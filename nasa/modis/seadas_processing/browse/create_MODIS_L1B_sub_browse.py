__author__ = 'uwe'

from sys import argv, exit
from os.path import basename, exists
from os import listdir, makedirs, remove, system

from utils.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list, bzip2DecompressFile
from nasa.modis.seadas_processing.conf.paths import seadasBinDir, imageMagickBinDir, modisGEO_subBasePath, modisL1B_subBasePath, modisBrowseBasePath


def printUsage():
    print 'Usage: create_MODIS_L1B_sub_browse.py date'
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

modisGEO_subPath     = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisGEO_subBasePath + _year) + _month) + _day)
modisL1B_LACPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1B_subBasePath + _year) + _month) + _day)
modisBrowsePath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisBrowseBasePath  + _year) + _month) + _day)

for _path in [modisBrowsePath]:
    if not exists(_path):
        print "Making directory: ", _path, " ..."
        makedirs(_path)

srcList = listdir(modisL1B_LACPath)
listSize = len(srcList)
print listSize

if not listSize:
    print "Nothing to do. Now exiting..."
    exit(1)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        _remove_from_list = False
        if not item.startswith('A' + _year +str(_doy)) or not item.endswith('.L1B_sub'):
            _remove_from_list = True

        if item.endswith('.L1B_sub') or item.endswith('.L1B_sub.bz2'):
            _remove_from_list = False
        else:
            _remove_from_list = True

        if _remove_from_list:
            srcList.remove(item)

exit_on_empty_list(srcList)
srcList.sort()
print srcList


# Now processing can start...


modisBrowseBinary = seadasBinDir + 'l1brsgen'
print exists(modisBrowseBinary)

# $OCSSW_BIN/l1brsgen
# ifile=/FastBuffer/temp/A2009220125000.L1B_LAC.x.hdf
# ofile=/FastBuffer/temp/A2009220125000.ppm
# geofile=/FastBuffer/temp/A2009220125000.GEO.x.hdf
# outmode=2 atmocor=1 subsamp=2 sline=1 eline=-999 spixl=1 epixl=-999


def process_modis_browse(l1b_productPath):
    GEO_productPath = l1b_productPath.replace('L1B_sub', 'GEO_sub')
    browse_product  = basename(l1b_productPath.replace('L1B_sub', 'ppm'))
    browse_productPath = modisBrowsePath + browse_product
    processing_call = modisBrowseBinary + ' ifile=' + l1b_productPath + ' geofile=' + GEO_productPath + \
                      ' ofile=' + browse_productPath + \
                      ' outmode=2 atmocor=1 subsamp=1 sline=1 eline=-999 spixl=1 epixl=-999'

    print "Executing: ", processing_call
    system(processing_call)
    if exists(browse_productPath):
        browse_jpg = browse_productPath.replace('.ppm', '.jpg')
        browse_txt = browse_productPath.replace('.ppm', '.txt')
        im_convert_call = imageMagickBinDir + 'convert -rotate 180 ' + browse_productPath + ' ' + browse_jpg
        print "Converting PPM image to JPEG format and rotating..."
        system(im_convert_call)
        im_ident_call = imageMagickBinDir + 'identify -format "%w %h" ' + browse_jpg + ' > ' + browse_txt
        system(im_ident_call)
        print "Determining image dimensions..."
        remove(browse_productPath)
        return 1    # success
    else:
        return 0

for item in srcList:
    print '\n', item
    zipped = False
    if item.endswith('.L1B_sub'):
        zipped = False
        l1b_product = item
    elif item.endswith('.L1B_sub.bz2'):
        zipped = True
        l1b_product = item[:-4]

    jpg_browse_file = modisL1B_LACPath + l1b_product.replace('L1B_sub', 'jpg')

    if exists(jpg_browse_file):
        print "Output " + jpg_browse_file + " exists already. Skipping."
        continue

    if not zipped:
        print "Processing..."
        unzipped_item = modisL1B_LACPath + item
        success = process_modis_browse(l1b_productPath=unzipped_item)
        print success
#        _bzip2_success = bzip2CompressFile(unzipped_item, removeInput=True)
#        print _bzip2_success, "Done."
    else:
        zipped_item = modisL1B_LACPath + item
        _bunzip_success = bzip2DecompressFile(zipped_item,removeInput=False)
        print _bunzip_success, "Done."
        if _bunzip_success:
            unzipped_item = modisL1B_LACPath + item[:-4]
            success = process_modis_browse(l1b_productPath=unzipped_item)
            print success
            print "Removing " + unzipped_item + "..."
            remove(unzipped_item)
        else:
            print "Decompressing failed! Skipping product ", item, " ..."
            continue

