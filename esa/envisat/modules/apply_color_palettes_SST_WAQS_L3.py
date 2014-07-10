#!/usr/bin/env python
# -*- coding: latin-1 -*-
# file: apply_color_palettes_SST_WAQS_L3.py

#GMES Marcoast, MetOcean Data Service, processing: Brockmann Consult
#( c ) images Brockmann Consult
#( c ) AATSR Source data ESA.

import os
import os.path
import sys
import time

def printUsage():
    print("Usage: apply_color_palettes_SST_WAQS_L3.py back_day")
    print("where back_day is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print("\back_day specifier is missing!\n")
        sys.exit(1)
    else:
        if (sys.argv[1] < 1):
            print("\back_day specifier useless!\n")
            sys.exit(1)    
except:
    printUsage()
    print("Error in parameters. Now exiting...")
    sys.exit(1)    

try:
    # last day to be included 
    back_day = int(sys.argv[1])
except:
    print("backDay parameter must be of type integer!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)

print("\n*********************************************************")
print(" Script \'apply_color_palettes_SST_WAQS_L3.py\' at work... ")
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

startDay    = get_date_string(get_float_day(back_day + 6))
endDay      = get_date_string(get_float_day(back_day))
rangeString = startDay + '_' + endDay
print(rangeString)
#sys.exit(1)

# basic directories
baseDir        = '/fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/'                          # bcserver7
srcDir         = baseDir + 'weekly/'
tempDir        = '/fs14/temp/'

imagesDir      = '/fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/'           # bcserver7
hiresImagesDir = imagesDir + 'hires/'
quickLooksDir  = imagesDir + 'quicklooks/'
thumbsDir      = imagesDir + 'thumbs/'

# tools config
pconvertHome   = '/home/uwe/tools/pconvert/'                                              # bcserver7
pconvertTool = pconvertHome + 'pconvert.sh' 

bandArithHome   = '/home/uwe/tools/BandArithBatch/'
bandArithTool   = bandArithHome + 'BandArithBatch.sh'
bandArithParams = 'sst_for_palette \"sst_comb_count == 0 && X == 1 ? 296.16 : (sst_comb_count == 0 && X > 1 ? 271.14 : ( sst_comb_mean < 271.14 ? 271.14 : (sst_comb_mean > 296.16 ? 296.16 : sst_comb_mean)))\"'

numBands = 1
products = ['sst']
sstBand = '7'          # in temporal product (band = "sst_for_palette")

bandNumbers = []
bandNumbers.append(sstBand)

colorPalettesDir = pconvertHome     + 'color_palettes/'
sstPalette       = colorPalettesDir + 'BSH-sst.cpd'

palettes=[]
palettes.append(sstPalette)
colorLegendsDir  = pconvertHome    + 'color_legends/'
sstLegend        = colorLegendsDir + 'BSH-sst_legend.jpg'
legends=[]
legends.append(sstLegend)

logosOverlay     = pconvertHome    + 'BC-ESA-AATSR-WAQSS_grey.jpg'

# Image Magick components
imageMagickHome = '/usr/bin/'                # bcserver7
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

srcList= os.listdir(srcDir)
listSize = len(srcList)

for a in range(listSize):
    for item in srcList:
        if item.endswith('.data')==1 or item.startswith('200')==0 or item.find(rangeString)==-1:
            srcList.remove(item)

srcList.sort()

for item in srcList:
    if item.find('north_sea')>0:
        _id = 'nos'
        xOffset = 0
        yOffset = 93
        qlXsize = 354    # quicklook image sizes
        qlYsize = 275
        tnXsize = 118    # thumbnail image sizes
        tnYsize =  92
    elif item.find('baltic_sea')>0:
        _id = 'bas'
        xOffset = 372
        yOffset =   0 
        qlXsize = 465    # quicklook image sizes
        qlYsize = 275
        tnXsize = 155    # thumbnail image sizes
        tnYsize =  92
    
    inputProduct = srcDir + item
    tempProduct  = tempDir + item
    copyProductToTempDirCommand = 'cp -r ' + srcDir + item[0:len(item)-2] +'* ' + tempDir
    os.system(copyProductToTempDirCommand)
    
    # now we modify the temporal product
    bandArithCommand = bandArithTool + ' ' + inputProduct + ' -d ' + tempProduct  + ' ' + bandArithParams
    os.system(bandArithCommand)
    
    pconvertCommand = pconvertTool + ' -b ' + bandNumbers[0] + ' -f jpg -s 0.0,0.0 -m off -o ' + imagesDir + ' -c ' + palettes[0] + ' ' + tempProduct 
    print('Executing: ' + pconvertCommand)
    os.system(pconvertCommand)
    
    rawImageName              = imagesDir + item[0:(len(item)-3)] + 'jpg'                                          # 20060821_20060827_mc_north_sea_aatsr_l3_1.2km.jpg
    hiresImageName            = hiresImagesDir + rangeString + '_' + products[0] + '_' + _id + '_ipf_1200.jpg'     # 20060508_20060514_sst_bas_ipf_1200.jpg
    quicklookImageName        = quickLooksDir  + rangeString + '_' + products[0] + '_' + _id + '_ipf_1200_ql.jpg'  # 20060508_20060514_sst_bas_ipf_1200_ql.jpg
    thumbnailImageName        = thumbsDir      + rangeString + '_' + products[0] + '_' + _id + '_ipf_1200_tn.jpg'  # 20060508_20060514_sst_bas_ipf_1200_tn.jpg
    currentHiresImageName     = imagesDir + 'current_' + products[0] + '_' + _id +  '_ipf_max.jpg'                 # current_sst_bas_ipf_max.jpg
    currentQuicklookImageName = imagesDir + 'current_' + products[0] + '_' + _id +  '_ipf_275.jpg'                 # current_sst_nos_wac_ipf_275.jpg
    
    # now the land mask overlay
    landmask_file = pconvertHome + _id + '_landmask_sst.gif'            # bcserver7
    imOverlayCommand = imComposite + ' -gravity center -quality 90 ' + landmask_file + ' ' + rawImageName + ' ' + rawImageName
    os.system(imOverlayCommand)
    
    # now the legend overlay
    geometryString0 = '0x0+' + str(1045+xOffset) + '+' + str(1040+yOffset)
    imOverlayCommand0 = imComposite + ' -geometry ' + geometryString0 + ' -quality 90 ' +  legends[0] + ' ' + rawImageName + ' ' + rawImageName
    os.system(imOverlayCommand0)
    
    # now the metadata annotation
    geometryString1 = '0x0+' + str(1053+xOffset) + '+' + str(1027+yOffset)
    imAnnotateCommand = imConvert + ' -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 16 -fill black -annotate ' + geometryString1 + ' \'Weekly mean:  ' + startDay + ' ' +'to ' + endDay + '\' ' + rawImageName + ' ' + rawImageName
    os.system(imAnnotateCommand)
    
    # now the BC Logo overlay
    imOverlayCommand2 = imComposite + ' -gravity southeast -quality 90 ' + logosOverlay + ' ' + rawImageName + ' ' + rawImageName
    os.system(imOverlayCommand2)
            
    # now the scaling to quicklooks
    imResizeCommand  = imConvert + ' -resize ' + str(qlXsize) + 'x' + str(qlYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  quicklookImageName
    os.system(imResizeCommand)
    
    # now the scaling to thumbs
    imResizeCommand2 = imConvert + ' -resize ' + str(tnXsize) + 'x' + str(tnYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  thumbnailImageName
    os.system(imResizeCommand2)
    
    # filenames: 20060521_20060527_bas_wac_ipf_1200.jpg, 20060521_20060527_nos_wac_ipf_1200.jpg
    mvCommand = 'mv ' + rawImageName + ' ' + hiresImageName
    os.system(mvCommand)
    
    # now we copy the recent quicklook and hires images
    copyHiresCommand = 'cp ' + hiresImageName + ' ' + currentHiresImageName
    os.system(copyHiresCommand)
    
    copyQuicklookCommand = 'cp ' + quicklookImageName + ' ' + currentQuicklookImageName
    os.system(copyQuicklookCommand)
    
    # now we can remove the temporal product
    removeTempProductCommand = 'rm -r ' + tempDir + item[0:len(item)-2] +'* '
    os.system(removeTempProductCommand)
    
print("\n*********************************************************")
print(" Script \'apply_color_palettes_SST_WAQS_L3.py\' finished.  ")
print("*********************************************************\n")

# EOF