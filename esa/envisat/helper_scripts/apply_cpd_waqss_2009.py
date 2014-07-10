#!/usr/bin/env python
# -*- coding: latin-1 -*

# this script has been run on frsprocessing server to regenerate 
# RGB PNGs with transparency. I use this script as a reference
# Note: only for MC products. There is also a script for sst (AATSR)

from os import listdir, system
from sys import exit

# basic directories
baseDir        = '/EOservices/InputPool/MERIS/RR_temp/'
srcDir         = baseDir + '2009/'
pconvertHome   = '/opt/beam-4.5.1_01/bin/'
pconvertScript = pconvertHome + 'pconvert.sh'
imagesDir      = srcDir 
hiresImagesDir = imagesDir + 'hires/'
quickLooksDir  = imagesDir + 'quicklooks/'
thumbsDir      = imagesDir + 'thumbs/'

numBands = 4
products = ['chl', 'tsm', 'ys', 'trn']
chlBand = '1'
tsmBand = '4'
ysBand  = '7'
trnBand = '10'
bandNumbers = []
bandNumbers.append(chlBand)
bandNumbers.append(tsmBand)
bandNumbers.append(ysBand)
bandNumbers.append(trnBand)

colorPalettesDir = baseDir + 'color_palettes/'
chlPalette       = colorPalettesDir + 'HAB_algal2_40_summer2008.cpd'
tsmPalette       = colorPalettesDir + 'HAB_tsm_30.cpd'
ysPalette        = colorPalettesDir + 'HAB_ys_5.cpd'
trnPalette       = colorPalettesDir + 'HAB_transparency_35.cpd'

palettes=[]
palettes.append(chlPalette)
palettes.append(tsmPalette)
palettes.append(ysPalette)
palettes.append(trnPalette)

# Image Magick components
imageMagickHome = '/usr/bin/'
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

srcList  = listdir(srcDir)
listSize = len(srcList)

for a in range(listSize):
    for item in srcList:
        if item.endswith('.data') or not item.endswith('.dim') or item.find('_est_')>0:
            print("Removing " + item + " from list.")
            srcList.remove(item)

srcList.sort()
print(srcList)

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
        print('Executing: ' + pconvertCommand)
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
        print(mvCommand)
        system(mvCommand)
        
# EOF