#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: apply_color_palettes_WeW_WAQS_daily.py

import os
import os.path
import sys
import time

def printUsage():
    print "Usage: apply_color_palettes_WeW_WAQS_daily.py back_day"
    print "where back_day is an integer value specifying which day to process:"
    print "1 means yesterday, 2 means the day before yesterday, etc."
    print "Maximum value is 32767.\n"

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print "\back_day specifier is missing!\n"
        sys.exit(1)
    else:
        if (sys.argv[1] < 1):
            print "\back_day specifier useless!\n"
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

print "\n************************************************************"
print " Script \'apply_color_palettes_WeW_WAQS_daily.py\' at work... "
print "************************************************************\n"

procDay = get_date_string(get_float_day(back_day))
print procDay
#sys.exit(1)

# basic directories
baseDir        = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/'                          # bcserver7
#baseDir        = '/Volumes/FS14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/'                   # bcG5
srcDir         = baseDir + 'daily-merged/'
pconvertHome   = '/home/uwe/tools/pconvert/'                                               # bcserver7
#pconvertHome   = '/Volumes/Elephant/Users/uwe/Applications/pconvert/'                       # bcG5
pconvertScript = pconvertHome + 'pconvert.sh'
imagesDir      = '/fs14/EOservices/OutputPool/quicklooks/WAQS-WeW/daily/'                  # bcserver7
#imagesDir      = '/Volumes/FS14/EOservices/OutputPool/quicklooks/WAQS-WeW/daily/'           # bcG5
hiresImagesDir = imagesDir + 'hires/'
quickLooksDir  = imagesDir + 'quicklooks/'
thumbsDir      = imagesDir + 'thumbs/'

numBands = 3
products = ['ys', 'chl', 'tsm']
ysBand  = '1'
chlBand = '2'
tsmBand = '3'

bandNumbers = []
bandNumbers.append(ysBand)
bandNumbers.append(chlBand)
bandNumbers.append(tsmBand)

colorPalettesDir = pconvertHome     + 'color_palettes/'
ysPalette        = colorPalettesDir + 'HAB_ys_5.cpd'
chlPalette       = colorPalettesDir + 'HAB_algal2_40_summer2008.cpd'
tsmPalette       = colorPalettesDir + 'HAB_tsm_30.cpd'

palettes=[]
palettes.append(ysPalette)
palettes.append(chlPalette)
palettes.append(tsmPalette)

colorLegendsDir  = pconvertHome    + 'color_legends/'
ysLegend         = colorLegendsDir + 'ys_mean_legend_HAB_5_grey.jpg'
chlLegend        = colorLegendsDir + 'chl_mean_legend_FUB_60_grey.jpg'
tsmLegend        = colorLegendsDir + 'tsm_mean_legend_HAB_302_grey.jpg'

legends=[]
legends.append(ysLegend)
legends.append(chlLegend)
legends.append(tsmLegend)

logosOverlay     = pconvertHome    + 'BC-ESA-MERIS-FUB-WAQSS_grey.jpg'

# Image Magick components
imageMagickHome = '/usr/bin/'                # bcserver7
#imageMagickHome = '/opt/local/bin/'                # bcG5
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

srcList= os.listdir(srcDir)
listSize = len(srcList)

# product names are like:     '20061003_nos_wac_wew-noflags_1200.dim'
for a in range(listSize):
    for item in srcList:
        if not item.endswith('.dim') or not item.startswith(procDay) or item.find('_uk_') > 0:
            #print "Removing: ", item, " from list."
            srcList.remove(item)

srcList.sort()
listSize = len(srcList)

if listSize == 0:
    print "Nothing to do here. Now quitting."
    sys.exit(1)

for item in srcList:
    if item.find('nos')>0:
        _id = 'nos'
        xOffset = 0
        yOffset = 93
        qlXsize = 354    # quicklook image sizes
        qlYsize = 275
        tnXsize = 118    # thumbnail image sizes
        tnYsize =  92
        xCropSize = 1135
        yCropSize = 1560
        xDestSize = 1669
        yDestSize = 1299
    elif item.find('bas')>0:
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

        # product names are like:     '20061003_nos_wac_wew-noflags_1200.dim'
        acq_day = item[0:8]
        const_identifier = acq_day + '_' + products[a] + '_' + _id
        hiresImageName            = hiresImagesDir + const_identifier + '_wac_wew_1200.jpg'                             # e.g. 20060129_chl_bas_wac_wew_1200.jpg
        currentHiresImageName     = imagesDir + 'current_daily_'   + products[a] + '_' + _id + '_wac_wew_max.jpg'       # e.g. current_daily_chl_bas_wac_wew_max.jpg
        quicklookImageName        = quickLooksDir  + const_identifier + '_wac_wew_1200_ql.jpg'                          # e.g. 20060129_chl_bas_wac_wew_1200_ql.jpg
        currentQuicklookImageName = imagesDir + 'current_daily_'   + products[a] + '_' + _id + '_wac_wew_275.jpg'       # e.g. current_daily_chl_bas_wac_wew_275.jpg
        thumbnailImageName        = thumbsDir      + const_identifier + '_wac_wew_1200_tn.jpg'                          # e.g. 20060129_chl_bas_wac_wew_1200_tn.jpg
        
        # now the land mask overlay
        # composite -gravity center bas_landmask.gif 20060508_mosaic.jpg 20060508_mosaic.jpg
        landmask_file = pconvertHome + _id + '_landmask_mc.gif'            # bcserver7
        imOverlayCommand = imComposite + ' -gravity center -quality 90 ' + landmask_file + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand)

        # now the legend overlay
        # composite -gravity southeast BC-Logo-72px.jpg 20060508_mosaic.jpg 20060508_mosaic.jpg
        #imOverlayCommand1 = imComposite + ' -gravity southeast ' + legends[a] + ' ' + rawImageName + ' ' + rawImageName
        geometryString0 = '0x0+' + str(1045+xOffset) + '+' + str(1037+yOffset)
        imOverlayCommand0 = imComposite + ' -geometry ' + geometryString0 + ' -quality 90 ' +  legends[a] + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand0)
        
        # now the metadata annotation
        geometryString1 = '0x0+' + str(1127+xOffset) + '+' + str(1024+yOffset)
        imAnnotateCommand = imConvert + ' -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 16 -fill black -annotate ' + geometryString1 + ' \'Daily mean:  ' + procDay + '\' ' + rawImageName + ' ' + rawImageName
        os.system(imAnnotateCommand)
        
        # now the BC Logo overlay
        #geometryString2 = '0x0+' + str(1380+xOffset) + '+' + str(840+yOffset)
        #imOverlayCommand2 = imComposite + ' -geometry ' + geometryString2 + ' ' + logosOverlay + ' ' + rawImageName + ' ' + rawImageName
        imOverlayCommand2 = imComposite + ' -gravity southeast -quality 90 ' + logosOverlay + ' ' + rawImageName + ' ' + rawImageName
        os.system(imOverlayCommand2)
                
        # now the scaling to quicklooks
        imResizeCommand  = imConvert + ' -resize ' + str(qlXsize) + 'x' + str(qlYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  quicklookImageName
        os.system(imResizeCommand)
        
        # now the scaling to thumbs
        imResizeCommand2 = imConvert + ' -resize ' + str(tnXsize) + 'x' + str(tnYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  thumbnailImageName
        os.system(imResizeCommand2)
        
        # rename image for next one
        mvCommand = 'mv ' + rawImageName + ' ' + hiresImageName
        os.system(mvCommand)
        
        # now we copy the recent quicklook and hires images
        copyHiresCommand = 'cp ' + hiresImageName + ' ' + currentHiresImageName
        os.system(copyHiresCommand)
        
        copyQuicklookCommand = 'cp ' + quicklookImageName + ' ' + currentQuicklookImageName
        os.system(copyQuicklookCommand)

print "\n************************************************************"
print " Script \'apply_color_palettes_WeW_WAQS_daily.py\' finished.  "
print "************************************************************\n"
# EOF
