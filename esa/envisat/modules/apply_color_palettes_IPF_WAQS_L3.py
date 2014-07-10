#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: apply_color_palettes_IPF_WAQS_L3.py

import os
import os.path
import sys
import time

def printUsage():
    print("Usage: apply_color_palettes_IPF_WAQS_L3 backDay")
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

print("\n*********************************************************")
print(" Script \'apply_color_palettes_IPF_WAQS_L3.py\' at work... ")
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

startDay    = get_date_string(get_float_day(back_days + 6))
endDay      = get_date_string(get_float_day(back_days))
rangeString = startDay + '_' + endDay

# basic directories
baseDir        = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/'
srcDir         = baseDir + 'weekly/'
pconvertHome   = '/home/uwe/tools/pconvert/'
pconvertScript = pconvertHome + 'pconvert.sh'
imagesDir      = '/fs14/EOservices/OutputPool/quicklooks/WAQS-IPF/weekly/'
hiresImagesDir = imagesDir + 'hires/'
quickLooksDir  = imagesDir + 'quicklooks/'
thumbsDir      = imagesDir + 'thumbs/'

numBands=3
products = ['chl', 'ys', 'tsm']
chlBand = '1'
ysBand  = '4'
tsmBand = '7'
bandNumbers = []
bandNumbers.append(chlBand)
bandNumbers.append(ysBand)
bandNumbers.append(tsmBand)

colorPalettesDir = pconvertHome     + 'color_palettes/'
chlPalette       = colorPalettesDir + 'HAB_algal2_40_summer2.cpd'
ysPalette        = colorPalettesDir + 'HAB_ys_5.cpd'
tsmPalette       = colorPalettesDir + 'HAB_tsm_30.cpd'
palettes=[]
palettes.append(chlPalette)
palettes.append(ysPalette)
palettes.append(tsmPalette)

colorLegendsDir  = pconvertHome    + 'color_legends/'
chlLegend        = colorLegendsDir + 'chl_mean_legend_HAB_40_summer2_grey.jpg'
ysLegend         = colorLegendsDir + 'ys_mean_legend_HAB_5_grey.jpg'
tsmLegend        = colorLegendsDir + 'tsm_mean_legend_HAB_302_grey.jpg'
legends=[]
legends.append(chlLegend)
legends.append(ysLegend)
legends.append(tsmLegend)

# Image Magick components
imageMagickHome = '/usr/bin/'
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

srcList= os.listdir(srcDir)
listSize = len(srcList)

for a in range(listSize):
    for item in srcList:
        if item.endswith('.data')==1 or item.startswith('200')==0 or item.find(rangeString)==-1:
            print("Removing " + item + " from list.")
            srcList.remove(item)

srcList.sort()
 
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
        pconvertCommand = pconvertScript + ' -b ' + bandNumbers[a] + ' -f jpg -o ' + imagesDir + ' -c ' + palettes[a] + ' ' + srcDir + item 
        print('Executing: ' + pconvertCommand)
        os.system(pconvertCommand)
        
        rawImageName              = imagesDir + item[0:(len(item)-3)] + 'jpg'
        hiresImageName            = hiresImagesDir + item[0:18] + products[a] + item[17:(len(item)-3)] + 'jpg'
        currentHiresImageName     = imagesDir + 'current_' + products[a] + item[17:29] + '_max.jpg'
        quicklookImageName        = quickLooksDir  + item[0:18] + products[a] + item[17:(len(item)-4)] + '_ql.jpg'
        currentQuicklookImageName = imagesDir + 'current_' + products[a] + item[17:29] + '_275.jpg'
        thumbnailImageName        = thumbsDir      + item[0:18] + products[a] + item[17:(len(item)-4)] + '_tn.jpg'
        
        # now the land mask overlay
        # composite -gravity center bas_landmask.gif 20060508_mosaic.jpg 20060508_mosaic.jpg
        landmask_file = pconvertHome + _id + '_landmask.gif'
        imOverlayCommand0 = imComposite + ' -gravity center ' + landmask_file + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand0)

        # now the legend overlay
        # composite -gravity southeast BC-Logo-72px.jpg 20060508_mosaic.jpg 20060508_mosaic.jpg
        imOverlayCommand1 = imComposite + ' -gravity southeast ' + legends[a] + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand1)
        
        # now the metadata annotation
        geometryString = '0x0+' + str(1304+xOffset) + '+' + str(1022+yOffset)
        imAnnotateCommand = imConvert + ' -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 16 -fill black -annotate ' + geometryString + ' \'Weekly mean:  ' + startDay + ' ' +'to ' + endDay + '\' ' + rawImageName + ' ' + rawImageName
        os.system(imAnnotateCommand)
        
        # now the BC Logo overlay
        geometryString2 = '0x0+' + str(1304+xOffset) + '+' + str(912+yOffset)
        imOverlayCommand2 = imComposite + ' -geometry ' + geometryString2 + ' ' + pconvertHome + 'BC-ESA-MERIS_grey.jpg ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand2)
                
        # now the scaling to quicklooks
        imResizeCommand  = imConvert + ' -resize ' + str(qlXsize) + 'x' + str(qlYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  quicklookImageName
        os.system(imResizeCommand)
        
        # now the scaling to thumbs
        imResizeCommand2 = imConvert + ' -resize ' + str(tnXsize) + 'x' + str(tnYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  thumbnailImageName
        os.system(imResizeCommand2)
        
        # filenames: 20060521_20060527_bas_wac_ipf_1200.jpg, 20060521_20060527_nos_wac_ipf_1200.jpg
        mvCommand = 'mv ' + rawImageName + ' ' + hiresImagesDir + item[0:18] + products[a] + item[17:(len(item)-3)] + 'jpg'
        print(mvCommand)
        os.system(mvCommand)
        
        # now we copy the recent quicklook and hires images
        copyHiresCommand = 'cp ' + hiresImageName + ' ' + currentHiresImageName
        os.system(copyHiresCommand)
        
        copyQuicklookCommand = 'cp ' + quicklookImageName + ' ' + currentQuicklookImageName
        os.system(copyQuicklookCommand)

print("\n*********************************************************")
print(" Script \'apply_color_palettes_IPF_WAQS_L3.py\' finished.  ")
print("*********************************************************\n")
# EOF