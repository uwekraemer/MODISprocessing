#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: apply_color_palettes_MC_WAQS_weekly_corpi.py

#GMES Marcoast, MetOcean Data Service, processing: ACRI, Brockmann Consult
#( c ) images Brockmann Consult
#( c ) MERIS Source data ESA.

import os
import os.path
import sys
import time

def printUsage():
    print("Usage: apply_color_palettes_MC_WAQS_weekly_corpi backDay")
    print("where backDay is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print("\nbackDay specifier is missing!\n")
        sys.exit(1)
    else:
        if (sys.argv[1] < 1):
            print("\nbackDay specifier useless!\n")
            sys.exit(1)    
except:
    printUsage()
    print("Error in parameters. Now exiting...")
    sys.exit(1)    

try:
    # last day to be included 
    back_days = int(sys.argv[1])
except:
    print("backDay parameter must be of type integer!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)
        
print("\n********************************************************")
print(" Script \'apply_color_palettes_MC_WAQS_weekly_corpi.py\' at work... ")
print("********************************************************\n")

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

startDay    = get_date_string(get_float_day(back_days + 6))
endDay      = get_date_string(get_float_day(back_days))
rangeString = startDay + '_' + endDay
print(rangeString)
#sys.exit(1)

# basic directories
baseDir        = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/'                          # bcserver7
srcDir         = baseDir + 'weekly/'
pconvertHome   = '/home/uwe/tools/pconvert/'                                              # bcserver7
pconvertScript = pconvertHome + 'pconvert.sh'                                             # bcserver7
imagesDir      = '/fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/'                 # bcserver7
hiresImagesDir = imagesDir

numBands = 1
products = ['chl']
chlBand = '1'

bandNumbers = []
bandNumbers.append(chlBand)

colorPalettesDir = pconvertHome     + 'color_palettes/'
chlPalette       = colorPalettesDir + 'HAB_algal2_40_summer2008.cpd'

palettes=[]
palettes.append(chlPalette)

colorLegendsDir  = pconvertHome    + 'color_legends/'
chlLegend        = colorLegendsDir + 'chl_mean_legend_HAB_40_summer2_grey.jpg'

logosOverlay     = pconvertHome    + 'BC-ACRI-ESA-MERIS-WAQSS_grey.jpg'

legends=[]
legends.append(chlLegend)

# Image Magick components
imageMagickHome = '/usr/bin/'                # bcserver7
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

srcList= os.listdir(srcDir)
listSize = len(srcList)

for a in range(listSize):
    for item in srcList:
        if item.endswith('.data')==True or item.find('_bas_')==-1 or item.find(rangeString)==-1:
            srcList.remove(item)

srcList.sort()
if len(srcList) == 0:
    print("Nothing to do. Now exiting...")

for item in srcList:
    if item.find('bas')>0:
        _id = 'bas'
        xOffset = 372
        yOffset =   0 
        qlXsize = 465    # quicklook image sizes
        qlYsize = 275
        tnXsize = 155    # thumbnail image sizes
        tnYsize =  92
    
    for a in range(numBands):
        pconvertCommand = pconvertScript + ' -b ' + bandNumbers[a] + ' -f jpg -s 0.0,0.0 -m off -o ' + imagesDir + ' -c ' + palettes[a] + ' ' + srcDir + item 
        print('Executing: ' + pconvertCommand)
        os.system(pconvertCommand)
        
        rawImageName              = imagesDir + item[0:(len(item)-3)] + 'jpg'
        hiresImageName            = hiresImagesDir + item[0:18] + products[a] + item[17:(len(item)-3)] + 'jpg'

        # now the land mask overlay
        # composite -gravity center bas_landmask.gif 20060508_mosaic.jpg 20060508_mosaic.jpg
        landmask_file = pconvertHome + _id + '_landmask.gif'            # bcserver7
        imOverlayCommand = imComposite + ' -gravity center -quality 90 ' + landmask_file + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand)

        # now the legend overlay
        # composite -gravity southeast BC-Logo-72px.jpg 20060508_mosaic.jpg 20060508_mosaic.jpg
        #imOverlayCommand1 = imComposite + ' -gravity southeast ' + legends[a] + ' ' + rawImageName + ' ' + rawImageName
        geometryString0 = '0x0+' + str(1045+xOffset) + '+' + str(1037+yOffset)
        imOverlayCommand0 = imComposite + ' -geometry ' + geometryString0 + ' -quality 90 ' +  legends[a] + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand0)
        
        # now the metadata annotation
        geometryString1 = '0x0+' + str(1045+xOffset) + '+' + str(1024+yOffset)
        imAnnotateCommand = imConvert + ' -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 16 -fill black -annotate ' + geometryString1 + ' \'Weekly mean:  ' + startDay + ' ' +'to ' + endDay + '\' ' + rawImageName + ' ' + rawImageName
        os.system(imAnnotateCommand)
        
        # now the BC Logo overlay
        #geometryString2 = '0x0+' + str(1380+xOffset) + '+' + str(840+yOffset)
        #imOverlayCommand2 = imComposite + ' -geometry ' + geometryString2 + ' ' + logosOverlay + ' ' + rawImageName + ' ' + rawImageName
        imOverlayCommand2 = imComposite + ' -gravity southeast -quality 90 ' + logosOverlay + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand2)
                  
        # filenames: 20060521_20060527_bas_wac_ipf_1200.jpg, 20060521_20060527_nos_wac_ipf_1200.jpg
        mvCommand = 'mv ' + rawImageName + ' ' + hiresImagesDir + item[0:18] + products[a] + item[17:(len(item)-3)] + 'jpg'
        os.system(mvCommand)
        
print("\n********************************************************")
print(" Script \'apply_color_palettes_MC_WAQS_weekly_corpi.py\' finished.  ")
print("********************************************************\n")

# EOF
