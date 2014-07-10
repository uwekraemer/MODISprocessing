#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: compute_overview_image_RGB_daily_running.py

import os
import os.path
import sys
import time
import math

#computes monthly overview of images produced from daily L1 RGB daily merged

def printUsage():
    print "Usage: ./compute_overview_image_RGB_daily_running.py region"
    print "where region includes:"
    print "NorthSea  or  BalticSea"

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without wrong parameters number
        print "wrong parameter number!"
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if ((sys.argv[1]=="NorthSea") or (sys.argv[1]=="BalticSea")):
            # do something
            print "Processing " +str(sys.argv[1]) + " request"
        else:               # incorrect parameter
            print "Wrong region specifier!"
            printUsage()
            sys.exit(1)

except:
    print "Error in parameters. Now exiting..."
    sys.exit(1)    

print "\n*****************************************************************"
print " Script \'compute_overview_image_RGB_daily_running.py\' at work... "
print "*****************************************************************\n"

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
    return year + month

# last day to be included 
back_days = 0
month      = get_date_string(get_float_day(back_days))

print "computing RGB overview images for " + month

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

print "\n*****************************************************************"
print " Script \'compute_overview_image_RGB_daily_running.py\' finished.  "
print "*****************************************************************\n"

# EOF