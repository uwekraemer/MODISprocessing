#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: compute_overview_image_IPF_daily.py

import os
import os.path
import sys
import time
import math

def printUsage():
    print("Usage: ./compute_overview_image_MC_weekly.py region product month")
    print("where region includes:")
    print("NorthSea  or  BalticSea")
    print("where product is choice of")
    print("chl, tsm, ys or trn")
    print("where month is expressed as YYYYMM")
    

try:
    argc=len(sys.argv)
    if (argc < 4):          # the program was called without wrong parameters number
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
        if ((sys.argv[2]=="chl") or (sys.argv[2]=="tsm") or (sys.argv[2]=="ys") or (sys.argv[2]=="trn")):
            product = sys.argv[2]
            print("Processing image overview for "  + product)
        else:
            print("Wrong product specifier!")
            printUsage()
            sys.exit(1)
        month = sys.argv[3]
        print("processing month " + month + "....")

except:
    print("Error in parameters. Now exiting...")
    sys.exit(1)    

print("\n*********************************************************")
print(" Script \'compute_overview_image_IPF_daily.py\' at work... ")
print("*********************************************************\n")

myDate = time.localtime()

# Some helper functions:
def get_float_day(day):
    secs_per_day  = 24*60*60
    return time.mktime(myDate)-day*secs_per_day

def get_date_string(float_day):
    date  = time.localtime(float_day)
    year  = str(date[0])
    month = str(date[1])
    day   = str(date[2])
    if date[1] <10:
        month = "0" + str(date[1])
    if date[2] <10:
        day   = "0" + str(date[2])
    return year + month + day

# basic directories
baseDir        = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/'
srcDir         = baseDir + 'weekly/'
pconvertHome   = '/home/uwe/tools/pconvert/'
pconvertScript = pconvertHome + 'pconvert.sh'
imagesDir      = '/fs14/EOservices/OutputPool/quicklooks/WAQS-IPF/'
hiresImagesDir = imagesDir + 'daily/hires/'
quickLooksDir  = imagesDir + 'quicklooks/'
thumbsDir      = imagesDir + 'thumbs/'
projectsDir    = '/fs1/projects/ongoing/marcoast/Service-WQ/images_overview/'

# Image Magick components
imageMagickHome = '/usr/bin/'
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'
imMontage       = imageMagickHome + 'montage'

if sys.argv[1]=="NorthSea":
    regiondestID= '_nos_'
    qlYsize = 100   # quicklook image sizes
    qlXsizef = qlYsize * 1.28
    qlXsize = math.floor(qlXsizef)  
    gapXsize = 5    # gaps between images
    gapYsize = 5
else:
    regiondestID= '_bas_'
    qlYsize = 100   # quicklook image sizes
    qlXsizef = qlYsize * 1.68
    qlXsize = math.floor(qlXsizef)
    gapXsize = 5    # gaps between images
    gapYsize = 5


inputFilesString = hiresImagesDir + month + '*' + product + regiondestID + '*.jpg'
outputFileString = projectsDir + month + '_' + product + regiondestID + 'daily_IPF.jpg'

montageCommand = imMontage + ' -label %f -tile 7 -geometry 170x100 -geometry +5+5 -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 8 ' + inputFilesString + ' ' + outputFileString

print(montageCommand)
os.system(montageCommand)

print("\n*********************************************************")
print(" Script \'compute_overview_image_IPF_daily.py\' finished.  ")
print("*********************************************************\n")

# EOF