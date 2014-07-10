#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: apply_color_palettes_MC_WAQSS2_L3.py

#GMES Marcoast, MetOcean Data Service, processing: ACRI, Brockmann Consult
#( c ) images Brockmann Consult
#( c ) MERIS Source data ESA.

# This script shall replace the 'apply_color_palettes_MC_WAQS_L3' module

from os import system, listdir
from sys import exit, argv
from time import mktime, localtime

def printUsage():
    print "Usage: apply_color_palettes_MC_WAQSS2_L3 backDay"
    print "where backDay is an integer value specifying which day to process:"
    print "1 means yesterday, 2 means the day before yesterday, etc."
    print "Maximum value is 32767.\n"

try:
    argc=len(argv)
    if (argc == 1):          # the program was called without parameters
        print "\nbackDay specifier is missing!\n"
        exit(1)
    else:
        if (argv[1] < 1):
            print "\nbackDay specifier useless!\n"
            exit(1)    
except:
    printUsage()
    print "Error in parameters. Now exiting..."
    exit(1)    

try:
    # last day to be included 
    back_days = int(argv[1])
except:
    print "backDay parameter must be of type integer!"
    printUsage()
    print "\nError in parameters. Now exiting...\n"
    exit(1)
        
print "\n**********************************************************"
print " Script \'apply_color_palettes_MC_WAQSS2_L3.py\' at work... "
print "**********************************************************\n"

myDate = localtime()

# Some helper functions:
def get_float_day(day):
    secs_per_day  = 24*60*60
    return mktime(myDate)-day*secs_per_day

def get_date_string(float_day):
    date  = localtime(float_day)
    year  = str(date[0])
    month = str(date[1])
    day   = str(date[2])
    if date[1] <10:
        month = "0" + str(date[1])
    if date[2] <10:
        day   = "0" + str(date[2])
    return year + month + day

startDay    = get_date_string(get_float_day(back_days + 6))
endDay      = get_date_string(get_float_day(back_days))
rangeString = startDay + '_' + endDay
print rangeString
#exit(1)

# basic directories
baseDir        = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/'                          # bcserver7
srcDir         = baseDir + 'weekly/'
pconvertHome   = '/home/uwe/tools/beam-4.5.1_01/bin/'
pconvertScript = pconvertHome + 'pconvert.sh'
imagesDir      = '/fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly_png/'             # bcserver7
hiresImagesDir = imagesDir + 'hires/'
quickLooksDir  = imagesDir + 'quicklooks/'
thumbsDir      = imagesDir + 'thumbs/'

numBands = 4
products = ['chl', 'tsm', 'ys', 'trn']
chlBand = '1'
tsmBand = '4'
ysBand  = '7'
trnBand = '10'

bandNumbers = [chlBand, tsmBand, ysBand, trnBand]

colorPalettesDir = '/home/uwe/tools/pconvert/color_palettes/'
chlPalette       = colorPalettesDir + 'HAB_algal2_40_summer2008.cpd'
tsmPalette       = colorPalettesDir + 'HAB_tsm_30.cpd'
ysPalette        = colorPalettesDir + 'HAB_ys_5.cpd'
trnPalette       = colorPalettesDir + 'HAB_transparency_35.cpd'

palettes= [chlPalette, tsmPalette, ysPalette, trnPalette]

colorLegendsDir  = pconvertHome    + 'color_legends/'
chlLegend        = colorLegendsDir + 'chl_mean_legend_HAB_40_summer2_grey.jpg'
tsmLegend        = colorLegendsDir + 'tsm_mean_legend_HAB_302_grey.jpg'
ysLegend         = colorLegendsDir + 'ys_mean_legend_HAB_5_grey.jpg'
trnLegend        = colorLegendsDir + 'trn_mean_legend_HAB_35_grey.jpg'

legends= [chlLegend, tsmLegend, ysLegend, trnLegend]

# Image Magick components
imageMagickHome = '/usr/bin/'                # bcserver7
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

srcList= listdir(srcDir)
listSize = len(srcList)

for a in range(listSize):
    for item in srcList:
        if item.endswith('.data')==1 or item.startswith('20')==0 or item.find(rangeString)==-1:
            srcList.remove(item)

srcList.sort()
if not len(srcList):
    print "Nothing to do. Now exiting..."

for item in srcList:
    if item.find('nos')>0:
        _id = 'nos'
        xOffset = 0
        yOffset = 93
        qlXsize = 354    # quicklook image sizes
        qlYsize = 275
        tnXsize = 118    # thumbnail image sizes
        tnYsize =  92
    elif item.find('bas')>0:
        _id = 'bas'
        xOffset = 372
        yOffset =   0 
        qlXsize = 465    # quicklook image sizes
        qlYsize = 275
        tnXsize = 155    # thumbnail image sizes
        tnYsize =  92
    
    for a in range(numBands):
        pconvertCommand = pconvertScript + ' -b ' + bandNumbers[a] + ' -f png -o ' + srcDir + ' -c ' + palettes[a] + ' ' + srcDir + item 
        print 'Executing: ' + pconvertCommand
        system(pconvertCommand)
        
        rawImageName              = srcDir + item[0:(len(item)-3)] + 'png'
        hiresImageName            = hiresImagesDir + item[0:18] + products[a] + item[17:(len(item)-3)] + 'png'
        quicklookImageName        = quickLooksDir  + item[0:18] + products[a] + item[17:(len(item)-4)] + '_ql.png'
        thumbnailImageName        = thumbsDir      + item[0:18] + products[a] + item[17:(len(item)-4)] + '_tn.png'
        
        # now the scaling to quicklooks
        imResizeCommand  = imConvert + ' -resize ' + str(qlXsize) + 'x' + str(qlYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  quicklookImageName
        system(imResizeCommand)
        
        # now the scaling to thumbs
        imResizeCommand2 = imConvert + ' -resize ' + str(tnXsize) + 'x' + str(tnYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  thumbnailImageName
        system(imResizeCommand2)
        
        # filenames: 20060521_20060527_bas_wac_ipf_1200.jpg, 20060521_20060527_nos_wac_ipf_1200.jpg
        mvCommand = 'mv ' + rawImageName + ' ' + hiresImagesDir + item[0:18] + products[a] + item[17:(len(item)-3)] + 'png'
        print mvCommand
        system(mvCommand)

print "\n**********************************************************"
print " Script \'apply_color_palettes_MC_WAQSS2_L3.py\' finished.  "
print "**********************************************************\n"

# EOF
