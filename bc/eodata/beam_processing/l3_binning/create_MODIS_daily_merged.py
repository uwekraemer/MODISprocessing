#!/usr/bin/env python3
__author__ = 'uwe'

from os.path import exists
from os import makedirs, listdir, popen, system
from sys import argv
from time import time
from shutil import move
from nasa.modis.seadas_processing.shared.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list
from nasa.modis.seadas_processing.conf.paths import modisL2_TSMBasePath
from bc.eodata.beam_processing.conf.paths import beam500HomeDir as beamHomeDir, color_palettes_dir, legendsDir, modisDailyBasePath
from bc.eodata.beam_processing.conf.paths import imageMagickComposite as composite, imageMagickMogrify as mogrify
from bc.eodata.beam_processing.conf.paths import veraBoldFont as font

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
    from bc.eodata.beam_processing.conf.paths import nosLandmaskFile as landMaskFile
elif region=='BalticSea':
    regiondestID= '_bas_'
    from bc.eodata.beam_processing.conf.params import bas_polygon as polygon
    from bc.eodata.beam_processing.conf.paths import basLandmaskFile as landMaskFile

if parameters=='wac':
    from bc.eodata.beam_processing.conf.paths import wac_graph_file as graph_file
elif parameters=='sst':
    from bc.eodata.beam_processing.conf.paths import sst_graph_file as graph_file

_year  = back_date[:4]
_month = back_date[4:6]
_day   = back_date[6:]
_doy   = getDOY(_year, _month, _day)
DOY = str(_doy).zfill(3)

_t0 = time()
print("Processing date " + back_date + " (DOY = " + DOY + ")...")

beamBinDir  = beamHomeDir + 'bin/'
gptProcessor = beamBinDir + 'gpt.command'
pconvertProcessor = beamBinDir + 'pconvert.command'

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

processingCall = gptProcessor + ' -e ' + graph_file + ' -PinputProducts=' + srcList + ' -PregionPolygon=' + polygon \
                 + ' -PoutputProduct=' + outputProductPath
# print(processingCall)
# system(processingCall)
_t1 = time()

# Image processing comes here
allBands = ['chl', 'tsm', 'Kd_490', 'sst']

if parameters == 'wac':
    bands = {
        'chl': 3,
        'tsm': 6,
        'Kd_490': 9
    }
else:
    bands = {
        'sst': 3
    }

def getImageSize(imagePath):
    wStr = "identify -format '%w' " + imagePath
    hStr = "identify -format '%h' " + imagePath
    width = popen(wStr).read()
    height= popen(hStr).read()
    return width, height

def getTextPosition(width, height):
    return int(width) - 990, int(height) - 46

for band, index in bands.items():
    print(band, index)
    # image from band
    pconvCall = pconvertProcessor + ' -f png -b ' + str(index) + ' -c ' + color_palettes_dir + band + '.cpd -o ' \
                + modisDailyPath + ' ' + outputProductPath
    pconvImageOutputPath = outputProductPath.replace('dim', 'png')
    bandImageOutputPath = pconvImageOutputPath.replace('wac', band)
    system(pconvCall)
    move(pconvImageOutputPath, bandImageOutputPath)
    # find out image width and height
    # imageWidth, imageHeight = getImageSize(bandImageOutputPath)
    # # land mask overlay
    # landMaskOverlayCmd = composite + ' ' + landMaskFile + ' ' + bandImageOutputPath + ' ' + bandImageOutputPath
    # system(landMaskOverlayCmd)
    # # legend overlay
    # legendFile = legendsDir + band + '_legend.png'
    # legendOverlayCmd = composite + ' -gravity SouthEast ' + legendFile + ' ' + bandImageOutputPath + ' ' + bandImageOutputPath
    # system(legendOverlayCmd)
    # # date annotation
    # txtX, txtY = getTextPosition(imageWidth, imageHeight)
    # annotationCmd = mogrify + ' -draw "text ' + str(txtX) + ',' + str(txtY) + " 'Daily MODISA product: " + back_date + "'\""
    # annotationCmd += ' -font ' + font + ' -pointsize 24 -fill white ' + bandImageOutputPath
    # system(annotationCmd)


_t2 = time()

print('Processing took %5.2f seconds.' % (_t1 - _t0))
print('Image generation took %5.2f seconds.' % (_t2 - _t1))
print('Just a git check...')

#EOF