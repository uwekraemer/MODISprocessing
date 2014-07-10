#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: apply_color_palettes_MC_WAQS_daily_CORPI.py

#GMES Marcoast, MetOcean Data Service, processing: ACRI, Brockmann Consult
#( c ) images Brockmann Consult
#( c ) MERIS Source data ESA.

import os
import os.path
import sys
import time

def printUsage():
    print "Usage: apply_color_palettes_MC_WAQS_daily_CORPI.py back_day"
    print "where back_day is an integer value specifying which day to process:"
    print "1 means yesterday, 2 means the day before yesterday, etc."
    print "Maximum value is 32767.\n"

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print "\"back_day\" specifier is missing!\n"
        sys.exit(1)
    else:
        if (sys.argv[1] < 1):
            print "\"back_day\" specifier useless!\n"
            sys.exit(1)    
except:
    printUsage()
    print "Error in parameters. Now exiting..."
    sys.exit(1)    

try:
    # last day to be included 
    back_day = int(sys.argv[1])
except:
    print "back_day parameter must be of type integer!"
    printUsage()
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)
        
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

print "\n***********************************************************"
print " Script \'apply_color_palettes_MC_WAQS_daily_CORPI.py\' at work... "
print "***********************************************************\n"

procDay = get_date_string(get_float_day(back_day))
print procDay
#sys.exit(1)

# basic directories
baseDir        = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/'                          # bcserver7
srcDir         = baseDir + 'daily-merged/'
pconvertHome   = '/home/uwe/tools/pconvert/'                                              # bcserver7
pconvertScript = pconvertHome + 'pconvert.sh'                                             # bcserver7
imagesDir      = '/fs14/EOservices/OutputPool/quicklooks/WAQS-MC/daily/'                  # bcserver7
hiresImagesDir = imagesDir

numBands = 1
products = ['chl']
chlBand = '1'

bandNumbers = []
bandNumbers.append(chlBand)

colorPalettesDir = pconvertHome     + 'color_palettes/'
chlPalette       = colorPalettesDir + 'HAB_algal2_40_summer2.cpd'

palettes=[]
palettes.append(chlPalette)

colorLegendsDir  = pconvertHome    + 'color_legends/'
chlLegend        = colorLegendsDir + 'chl_mean_legend_HAB_40_summer2_grey.jpg'

legends=[]
legends.append(chlLegend)

# Image Magick components
imageMagickHome = '/usr/bin/'                # bcserver7
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

logosOverlay     = pconvertHome    + 'BC-ACRI-ESA-MERIS-WAQSS_grey.jpg'

srcList= os.listdir(srcDir)
listSize = len(srcList)

# product names are like:     'L3_ENV_MER_20060814_NSEA_PC_ACR___0000.dim'
for a in range(listSize):
    for item in srcList:
        if item.endswith('.data')==1 or item.find(procDay)==-1 or item.find('BALTIC')==-1:
            srcList.remove(item)

srcList.sort()
 
for item in srcList:
    if item.find('BALTIC')>0:
        _id = 'bas'
        xOffset = 372
        yOffset =   0 
        qlXsize = 465    # quicklook image sizes
        qlYsize = 275
        tnXsize = 155    # thumbnail image sizes
        tnYsize =  92
        xCropSize = 1243
        yCropSize = 1448
        xDestSize = 2041
        yDestSize = 1206
    
    for a in range(numBands):
        pconvertCommand = pconvertScript + ' -b ' + bandNumbers[a] + ' -f jpg -o ' + imagesDir + ' -c ' + palettes[a] + ' ' + srcDir + item 
        print 'Executing: ' + pconvertCommand
        os.system(pconvertCommand)
        
        rawImageName              = imagesDir + item[0:(len(item)-3)] + 'jpg'

        # product names are like:     'L3_ENV_MER_20060814_NSEA_PC_ACR___0000.dim'
        acq_day = item[11:19]
        const_identifier = acq_day + '_' + products[a] + '_' + _id
        hiresImageName            = hiresImagesDir + const_identifier + '_wac_acr_1200.jpg'                             # e.g. 20060129_chl_bas_wac_acr_1200.jpg

        # scale both images to dest size to cover the same pixels as the BC-binned products
        # convert -resize 1669x1299! input.jpg output.jpg.jpg
        imScaleCommand = imConvert + ' -resize ' + str(xDestSize) + 'x' + str(yDestSize) + '! ' + rawImageName + ' ' + rawImageName
        os.system(imScaleCommand)

        # now the legend overlay
        # composite -gravity southeast BC-Logo-72px.jpg 20060508_mosaic.jpg 20060508_mosaic.jpg
        #imOverlayCommand1 = imComposite + ' -gravity southeast ' + legends[a] + ' ' + rawImageName + ' ' + rawImageName
        geometryString0 = '0x0+' + str(1045+xOffset) + '+' + str(1037+yOffset)
        imOverlayCommand0 = imComposite + ' -geometry ' + geometryString0 + ' -quality 90 ' +  legends[a] + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand0)

        # now the land mask overlay
        # composite -gravity center bas_landmask.gif 20060508_mosaic.jpg 20060508_mosaic.jpg
        landmask_file = pconvertHome + _id + '_landmask_mc.gif'            # bcserver7
        imOverlayCommand = imComposite + ' -gravity center -quality 90 ' + landmask_file + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand)


        # now the metadata annotation
        geometryString1 = '0x0+' + str(1127+xOffset) + '+' + str(1024+yOffset)
        imAnnotateCommand = imConvert + ' -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 16 -fill black -annotate ' + geometryString1 + ' \'Daily mean:  ' + procDay + '\' ' + rawImageName + ' ' + rawImageName
        os.system(imAnnotateCommand)
        
        # now the BC Logo overlay
        #geometryString2 = '0x0+' + str(1380+xOffset) + '+' + str(840+yOffset)
        #imOverlayCommand2 = imComposite + ' -geometry ' + geometryString2 + ' ' + logosOverlay + ' ' + rawImageName + ' ' + rawImageName
        imOverlayCommand2 = imComposite + ' -gravity southeast -quality 90 ' + logosOverlay + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand2)
                
        # rename image for next one
        mvCommand = 'mv ' + rawImageName + ' ' + hiresImageName
        os.system(mvCommand)
        
print "\n***********************************************************"
print " Script \'apply_color_palettes_MC_WAQS_daily_CORPI.py\' finished.  "
print "***********************************************************\n"
# EOF
