#!/usr/bin/env python3
__author__ = 'uwe'

from os.path import exists
from os import makedirs, listdir, system
from sys import argv
from nasa.modis.seadas_processing.shared.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list
from nasa.modis.seadas_processing.conf.paths import modisL2_TSMBasePath
from bc.eodata.beam_processing.conf.paths import beam500HomeDir as beamHomeDir, modisDailyBasePath

def printUsage():
    print("Usage: ", argv[0], "<date> <region> <params>")
    print("where date is a string representing the date to process,")
    print("e.g. 20140114 for January 14, 2014.")
    print("and <region> one of 'NorthSea' and 'BalticSea'")
    print("and <params> a parameter describing the product contents,")
    print("i.e. 'wac' for water constituents, and 'sst' for SST.")

if len(argv) != 4:
    printUsage()
    exit(1)

back_date = argv[1]
if len(back_date)!=8:
    print("****************************")
    print("* date parameter malformed *")
    print("****************************")
    printUsage()
    exit(1)

region = argv[2]
if not region in ['NorthSea', 'BalticSea']:
    print("****************************")
    print("* region parameter unknown *")
    print("****************************")
    printUsage()
    exit(1)

parameters = argv[3]
if not parameters in ['wac', 'sst']:
    print("******************************")
    print("* processing parameter wrong *")
    print("******************************")
    printUsage()
    exit(1)

if region=='NorthSea':
    regiondestID= '_nos_'
    from bc.eodata.beam_processing.conf.params import nos_polygon as polygon
elif region=='BalticSea':
    regiondestID= '_bas_'
    from bc.eodata.beam_processing.conf.params import bas_polygon as polygon

if parameters=='wac':
    from bc.eodata.beam_processing.conf.paths import wac_graph_file as graph_file
elif parameters=='sst':
    from bc.eodata.beam_processing.conf.paths import sst_graph_file as graph_file

_year  = back_date[:4]
_month = back_date[4:6]
_day   = back_date[6:]
_doy   = getDOY(_year, _month, _day)
DOY = str(_doy).zfill(3)

print("Processing date " + back_date + " (DOY = " + DOY + ")...")

beamBinDir  = beamHomeDir + 'bin/'
gptProcessor = beamBinDir + 'gpt.sh'                       # bcserver7 (deployment)
#gptProcessor = '/Applications/beam-5.0/bin/gpt.command'     # bcmacpro1 (development)
modisL2_TSMPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL2_TSMBasePath  + _year) + _month) + _day)
modisDailyPath  = ensureTrailingSlash(ensureTrailingSlash(modisDailyBasePath + _year) + _month)

for _path in [modisDailyPath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)

try:
    srcList = listdir(modisL2_TSMPath)
except OSError:
    print("Cannot open ", modisL2_TSMPath+ "! Now exiting...")
    exit(1)
else:
    listSize = exit_on_empty_list(srcList)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        if not item.startswith('A' + _year + DOY) or not item.endswith('.L2_TSM.dim'):
            srcList.remove(item)

exit_on_empty_list(srcList)
srcList.sort()
srcList = ",".join([modisL2_TSMPath + path for path in srcList])

outputProductPath = modisDailyPath + back_date + regiondestID + parameters + '_mod_1200.dim'
#print(srcList, outputProductPath, polygon)

processing_call = gptProcessor + ' -e ' + graph_file + ' -PinputProducts=' + srcList + ' -PregionPolygon=' + polygon + ' -PoutputProduct=' + outputProductPath
print("Executing call: ", processing_call)
system(processing_call)