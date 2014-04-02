#!/usr/bin/env python
__author__ = 'uwe'

from sys import argv
from os import listdir, makedirs, remove, system
from os.path import basename, exists
from bc.eodata.beam_processing.conf.paths import gptProcessor, UTM_graph_file
from bc.eodata.beam_processing.conf.paths import pconvProcessor, cobios_chl_palette
from bc.eodata.beam_processing.conf.paths import imageMagickComposite, landMaskFile
from nasa.modis.seadas_processing.shared.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list
from nasa.modis.seadas_processing.conf.paths import modisL3_TSMBasePath, modisL3_TSM_UTMPath, modisL3_TSM_UTM_QLPath
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
modisL3_UTMPath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL3_TSM_UTMPath  + _year) + _month) + _day)
modisL3_UTM_QLPath = ensureTrailingSlash(modisL3_TSM_UTM_QLPath  + _year)

for _path in [modisL3_UTMPath, modisL3_UTM_QLPath]:
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
        if not item.startswith('cb_ns_' + back_date) or not item.endswith('.dim'):
            srcList.remove(item)

listSize = exit_on_empty_list(srcList)
srcList.sort()

outputProductPath = modisL3_UTMPath + 'cb_' + _site + '_' + back_date + '_9999_eo_bc.dim'

print(srcList, outputProductPath)

for item in srcList:
    reproj_processingCall = gptProcessor + ' ' + UTM_graph_file + ' -Ssource=' + modisL3_TSMPath + item + ' -Pfile=' + outputProductPath
    system(reproj_processingCall)
    pconv_call = pconvProcessor + ' -f png -b 1 -c ' + cobios_chl_palette + ' -o ' + modisL3_UTM_QLPath + ' ' + outputProductPath
    system(pconv_call)
    oldPngFileName = modisL3_UTM_QLPath + basename(outputProductPath).replace('.dim', '.png')
    newPngFileName = modisL3_UTM_QLPath + basename(outputProductPath).replace('cb_ns_', 'cb_ns_chl_').replace('.dim', '.png')
    imCompositeCommand = imageMagickComposite + ' -gravity center ' + landMaskFile + ' ' + oldPngFileName + ' ' + newPngFileName
    system(imCompositeCommand)
    remove(oldPngFileName)      # not needed anymore
