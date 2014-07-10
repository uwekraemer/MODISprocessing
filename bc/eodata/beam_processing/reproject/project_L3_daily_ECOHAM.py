#!/usr/bin/env python
__author__ = 'uwe'

from sys import argv
from os import listdir, makedirs, system
from os.path import exists

from bc.eodata.beam_processing.conf.paths import gptProcessor, ECOHAM_graph_file
from utils.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list
from nasa.modis.seadas_processing.conf.paths import modisL3_TSMBasePath, modisL3_ECOHAMBasePath
from nasa.modis.seadas_processing.conf.params import _site


def printUsage():
    print("Usage: ", argv[0], "<date>")
    print("where date is a string representing the date to process,")
    print("e.g. 20120607 for June 7, 2012.")

if len(argv) != 2:
    printUsage()
    exit(1)

back_date = argv[1]
if len(back_date)!=8:
    print("****************************")
    print("* date parameter malformed *")
    print("****************************")
    printUsage()
    exit(1)

_year  = back_date[:4]
_month = back_date[4:6]
_day   = back_date[6:]
_doy   = getDOY(_year, _month, _day)
print("Processing date " + back_date + " (DOY = " + str(_doy)+ ").")

modisL3_TSMPath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL3_TSMBasePath  + _year) + _month) + _day)
modisL3_ECOHAMPath  = ensureTrailingSlash(modisL3_ECOHAMBasePath  + _year)

for _path in [modisL3_TSMPath, modisL3_ECOHAMPath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)

try:
    srcList = listdir(modisL3_TSMPath)
except OSError:
    print("Cannot open ", modisL3_TSMPath+ "! Now exiting...")
    exit(1)
else:
    listSize = exit_on_empty_list(srcList)
    print(listSize)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        if not item.startswith('cb_' + _site + '_' + back_date) or not item.endswith('.dim'):
            srcList.remove(item)

listSize = exit_on_empty_list(srcList)
srcList.sort()

# reprojected L3 products,        Name e.g. cb_ns_20130603_eo_ecoham.dim
outputProductPath = modisL3_ECOHAMPath + 'cb_' + _site + '_' + back_date + '_eo_bc_lat_lon_ecoham.dim'

print(srcList, outputProductPath)

for item in srcList:
    reproj_processingCall = gptProcessor + ' ' + ECOHAM_graph_file + ' -Ssource=' + modisL3_TSMPath + item + ' -Pfile=' + outputProductPath
    system(reproj_processingCall)
