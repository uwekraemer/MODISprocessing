#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: compute_overview_image_RGB_daily.py

import os
import os.path
import sys
import time
import math


def printUsage():
    print("Usage: ./compute_overview_image_RGB_daily.py region month")
    print("where region includes:")
    print("NorthSea  or  BalticSea")
    print("where month is expressed as YYYYMM")

try:
    argc=len(sys.argv)
    if (argc < 3):          # the program was called without wrong parameters number
        print("wrong parameter number!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if ((sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea")):
            # do something
            print("Processing " +str(sys.argv[1]) + " request")
        else:               # incorrect parameter
            print("Wrong region specifier!")
            printUsage()
            sys.exit(1)
        month = sys.argv[2]
        print("processing month " + month + "....")

except:
    print("Error in parameters. Now exiting...")
    sys.exit(1)    

print("\n*********************************************************")
print(" Script \'compute_overview_image_RGB_daily.py\' at work... ")
print("*********************************************************\n")

print("computing RGB overview images for " + month)

# basic directories
baseDir        = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/'
srcDir         = baseDir + 'weekly/'
pconvertHome   = '/home/uwe/tools/pconvert/'
pconvertScript = pconvertHome + 'pconvert.sh'
imagesDir      = '/fs14/EOservices/OutputPool/quicklooks/WAQS-IPF/'
hiresImagesDir = imagesDir + 'daily-RGB/hires/'
quickLooksDir  = imagesDir + 'daily-RGB/quicklooks/'
thumbsDir      = imagesDir + 'daily-RGB/thumbs/'
projectsDir    = '/fs14/EOservices/OutputPool/quicklooks/overview_images/'


# Image Magick components
imageMagickHome = '/usr/bin/'
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'
imMontage       = imageMagickHome + 'montage'


if sys.argv[1]=="NorthSea":
    regiondestID= '_nos_'
    qlYsize = 200   # quicklook image sizes
    qlXsizef = qlYsize * 1.28
    qlXsize = math.floor(qlXsizef)  
    gapXsize = 20    # gaps between images
    gapYsize = 5
else:
    regiondestID= '_bas_'
    qlYsize = 200   # quicklook image sizes
    qlXsizef = qlYsize * 1.68
    qlXsize = math.floor(qlXsizef)
    gapXsize = 20    # gaps between images
    gapYsize = 5


# produce overview image for each parameter
gapString = '+' + str(gapXsize) + '+' + str(gapYsize)
qlSizeString = str(qlXsize) + 'x' + str(qlYsize)
    
inputOptionsString = ' -label %f -tile 5 -geometry ' + qlSizeString + ' -geometry ' + gapString + ' -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 8 '
inputFilesString = hiresImagesDir + month + '*' + regiondestID + 'RGB*.jpg'
outputFileString = projectsDir + month + '_RGB' + regiondestID + '.jpg'

montageCommand = imMontage + inputOptionsString + inputFilesString + ' ' + outputFileString
os.system(montageCommand)
    
print("\n*********************************************************")
print(" Script \'compute_overview_image_RGB_daily.py\' finished.  ")
print("*********************************************************\n")

# EOF
