#!/usr/bin/env python
# -*- coding: latin-1 -*

# this script has been run on frsprocessing server to regenerate 
# RGB PNGs with transparency. I use this script as a reference
# Note: only for SST. There is also a script for MC (MERIS)


from os import listdir, system
from sys import exit

# basic directories
baseDir        = '/EOservices/InputPool/AATSR/NR_temp/'
srcDir         = baseDir + '2009/'
pconvertHome   = '/opt/beam-4.5.1_01/bin/'
pconvertScript = pconvertHome + 'pconvert.sh'

imagesDir      = srcDir 
hiresImagesDir = imagesDir + 'hires/'
quickLooksDir  = imagesDir + 'quicklooks/'
thumbsDir      = imagesDir + 'thumbs/'

numBands = 1
products = ['sst']
sstBand = '1'          # band = "sst_comb_mean"

bandNumbers = []
bandNumbers.append(sstBand)

colorPalettesDir = baseDir + 'color_palettes/'
sstPalette       = colorPalettesDir + 'BSH-sst.cpd'

palettes=[]
palettes.append(sstPalette)

# Image Magick components
imageMagickHome = '/usr/bin/'
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

srcList  = listdir(srcDir)
listSize = len(srcList)

for a in range(listSize):
    for item in srcList:
        if item.endswith('.data') or not item.endswith('.dim'):
            print("Removing " + item + " from list.")
            srcList.remove(item)

srcList.sort()
print(srcList)

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
    
    for a in range(numBands):
        pconvertCommand = pconvertScript + ' -b ' + bandNumbers[a] + ' -f png -o ' + srcDir + ' -c ' + palettes[a] + ' ' + srcDir + item 
        print('Executing: ' + pconvertCommand)
        system(pconvertCommand)
        
        rawImageName              = imagesDir + item[0:(len(item)-3)] + 'png'                                          # 20060821_20060827_mc_north_sea_aatsr_l3_1.2km.jpg
        hiresImageName            = hiresImagesDir + item[0:18] + products[a] + '_' + _id + '_ipf_1200.png'     # 20060508_20060514_sst_bas_ipf_1200.jpg
        quicklookImageName        = quickLooksDir  + item[0:18] + products[a] + '_' + _id + '_ipf_1200_ql.png'  # 20060508_20060514_sst_bas_ipf_1200_ql.jpg
        thumbnailImageName        = thumbsDir      + item[0:18] + products[a] + '_' + _id + '_ipf_1200_tn.png'  # 20060508_20060514_sst_bas_ipf_1200_tn.jpg

        #
        
        # now the scaling to quicklooks
        imResizeCommand  = imConvert + ' -resize ' + str(qlXsize) + 'x' + str(qlYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  quicklookImageName
        system(imResizeCommand)
        
        # now the scaling to thumbs
        imResizeCommand2 = imConvert + ' -resize ' + str(tnXsize) + 'x' + str(tnYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  thumbnailImageName
        system(imResizeCommand2)
        
        # filenames: 20060521_20060527_bas_wac_ipf_1200.jpg, 20060521_20060527_nos_wac_ipf_1200.jpg
        mvCommand = 'mv ' + rawImageName + ' ' + hiresImageName
        print(mvCommand)
        system(mvCommand)
        
# EOF