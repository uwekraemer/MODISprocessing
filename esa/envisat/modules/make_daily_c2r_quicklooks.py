__author__ = 'uwe'

from sys import argv,exit
from os import system
from os.path import basename
from time import localtime, mktime

def getDateString(backDays):
    date  = localtime(mktime(localtime())-backDays*86400)
    year  = str(date[0])
    month = str(date[1]).zfill(2)
    day   = str(date[2]).zfill(2)
    return year + month + day

def ensureTrailingSlash(path):
    if not path.endswith('/'):
        return path + '/'
    else:
        return path

def printUsage ():
    print("Usage: make_daily_c2r_quicklooks.py region back_day")
    print("where region includes:")
    print("\"NorthSea\",  \"BalticSea or \"Lithuania\"\"\n")
    print("and back_day is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

def checkParams():
    argc=len(argv)
    if argc < 3:          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        exit(1)
    else:                   # we have also received parameters
        if argv[1] in ["NorthSea", "BalticSea", "Lithuania"] and (int(argv[2]) > -1):
            print("Processing " +str(argv[1]) + " request")
        else:               # incorrect parameter
            print("Wrong region specifier!")
            printUsage()
            exit(1)

checkParams()
parameter = 'tsm'
#TODO introduce parameter argument

region = argv[1]
back_date = getDateString(int(argv[2]))
print("For the date", back_date + "...")

#exit(1)

if region == "Lithuania":
    mosaicTemplate = '/home/uwe/tools/mosaic/corpi_tsm_mosaic.xml'
elif region == "NorthSea":
    mosaicTemplate = '/home/uwe/tools/mosaic/nsea_tsm_mosaic.xml'
elif region == "BalticSea":
    mosaicTemplate = '/home/uwe/tools/mosaic/bsea_tsm_mosaic.xml'

# directories
inputDir         = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-caseR/Level2/'
mosaicTempDir    = '/fs14/temp/'
quicklookBaseDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-caseR/preview-images/'
quicklookDestDir = quicklookBaseDir + ensureTrailingSlash(region) + ensureTrailingSlash(parameter)

# tools config
beamBinDir = '/home/uwe/tools/beam-4.10/bin/'
gptTool   = beamBinDir + 'gpt.sh'
pconvTool = beamBinDir + 'pconvert.sh'
pconvPalette = '/home/uwe/tools/pconvert/color_palettes/BAW_tsm_c2r_palette_FR_RR.cpd'
imageMagickConvert   = '/usr/bin/convert'
imageMagickComposite = '/usr/bin/composite'

def cleanup():
    rmCommand1 = 'rm '    + mosaicTempDir + '*' + back_date + '*.png'   # rm /fs14/temp/*20120312*.png
    rmCommand2 = 'rm '    + mosaicTempDir + '*' + back_date + '*.dim'   # rm /fs14/temp/*20120312*.dim
    rmCommand3 = 'rm -r ' + mosaicTempDir + '*' + back_date + '*.data'  # rm -r /fs14/temp/*20120312*.data
    system(rmCommand1)
    system(rmCommand2)
    system(rmCommand3)

# 1. make mosaic:
# /Applications/beam-4.10/bin/gpt.command -e -c 2G /Volumes/EOservices/Tools/Processing/processors/mosaic/corpi_mosaic_medium.xml -t /testing/corpitest20111016medium.dim /Volumes/ccnrt/Attic/childProducts/MER_FRS_1P/balticsea/MER_FRS_1PNMAP20111016_*
mosaicProductPath = ensureTrailingSlash(mosaicTempDir) + region +'_' + back_date + '_' + parameter + '.dim'
mosaickingCommand = gptTool + ' -e -c 2G ' + mosaicTemplate + ' -t ' + mosaicProductPath + ' ' + ensureTrailingSlash(inputDir) + 'MER_RR_C2R_' + back_date + '_*.dim'
print(mosaickingCommand)
returnValue = system(mosaickingCommand)
if returnValue:
    print("Mosaicking failed! Now exiting...")
    cleanup()
    exit(1)


# 2. make quicklook:
# /Applications/beam-4.10/bin/pconvert.sh -f png -b 1 -c /home/uwe/tools/pconvert/color_palettes/BAW_tsm_c2r_palette_FR_RR.cpd -o /fs14/temp/NorthSea20120226.dim
pconvCommand = pconvTool + ' -f png -b 1 -c ' + pconvPalette + ' -o ' + mosaicTempDir + ' ' + mosaicProductPath
print(pconvCommand)
returnValue = system(pconvCommand)
if returnValue:
    print("pconvert failed! Now exiting...")
    cleanup()
    exit(1)
previewImageName = mosaicProductPath.replace('.dim', '.png')

# 3. make label on a plate:
# convert -font ~/Downloads/AT833___.TTF -pointsize 32 -weight Bold -fill white -annotate 0x0+8+38 '20111026' labelplate.png labelplate_20111016.png
labelPlate = '/home/uwe/tools/pconvert/labels/labelplate_medium.png'
BCfont = '/home/uwe/tools/pconvert/fonts/AT833___.TTF'
labelPlateDate = mosaicTempDir + back_date + '.png'
labellingCommand = imageMagickConvert + ' -font ' + BCfont + ' -pointsize 32 -weight Bold -fill white -annotate 0x0+8+38 ' + back_date + ' ' + labelPlate + ' ' + labelPlateDate
print(labellingCommand)
returnValue = system(labellingCommand)
if returnValue:
    print("labelling step 1 failed! Now exiting...")
    cleanup()
    exit(1)

# 4. put plate on image:
# composite -gravity southeast -dissolve 65% labelplate_20111016.png corpitest20111016.png corpitest20111016.png
labelledPreviewImageName = quicklookDestDir + basename(previewImageName)
compositeCommand = imageMagickComposite + ' -gravity southeast -dissolve 65% ' + labelPlateDate + ' ' + previewImageName + ' ' + labelledPreviewImageName
print(compositeCommand)
returnValue = system(compositeCommand)
if returnValue:
    print("labelling step 2 failed! Now exiting...")

cleanup()

#EOF