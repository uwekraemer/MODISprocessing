#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_MC_WAQS_L3_animations.py

from os import system, listdir
import os.path
import sys
import time

def printUsage():
    print "Usage: process_MC_WAQS_L3_animations.py month"
    print "where month is a integer value specifying which month to process:"
    print "Example: 200601\n"

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print "\nmonth specifier is missing!\n"
        sys.exit(1)
    else:
        if (int(sys.argv[1]) < 2006):
            print "\nmonth specifier useless!\n"
            sys.exit(1)    
except:
    printUsage()
    print "Error in parameters. Now exiting..."
    sys.exit(1)    

try:
    # month to be used 
    month = int(sys.argv[1])
    _month = str(month)
except:
    print "month parameter must be of type integer!"
    printUsage()
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)
        
print "\n******************************************************"
print " Script \'process_MC_WAQS_L3_animations.py\' at work... "
print "******************************************************\n"

products = ['chl', 'ys', 'tsm', 'trn', 'sst']
regions  = ['nos', 'bas']

# basic directories
#baseDir   = '/Volumes/Elephant/Users/uwe/Desktop/temp/marcoast/'                     # bcG5
baseDir   = '/fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/'                  # bcserver7
srcDir    = baseDir + 'quicklooks/'
animationsBaseDir = baseDir + 'animations/'
qlTempDir = animationsBaseDir + 'ql_temp/'
tnTempDir = animationsBaseDir + 'tn_temp/'
qlAnimOutputDir = animationsBaseDir + 'ql_size/'
tnAnimOutputDir = animationsBaseDir + 'tn_size/'

# Image Magick components
#imageMagickHome = '/opt/local/bin/'                # bcG5
imageMagickHome = '/usr/bin/'                # bcserver7
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'
imMogrify       = imageMagickHome + 'mogrify'

srcList= listdir(srcDir)
listSize = len(srcList)

for a in range(listSize):
    for item in srcList:
        if not item.endswith('.jpg') or not item.startswith(_month):
            srcList.remove(item)

srcList.sort()
if len(srcList) == 0:
    print "Nothing to do. Now exiting..."

'''
Now the annotation of the images:
Sample convert-call:
convert -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 18 -fill black -annotate 0x0+250+30 '20060201' <srcDir>/20060201_20060207_chl_nos_wac_acr_1200_ql.jpg /Volumes/Elephant/Users/uwe/Desktop/temp/marcoast/animated/ql_temp/20060201_20060207_chl_nos_wac_acr_1200_ql.jpg
'''

for item in srcList:
    print item
    if item.find('_nos_')>0:
        xOffset = 250
        yOffset =  30
        tnXsize = 118    # thumbnail image sizes
        tnYsize =  92
    elif item.find('_bas_')>0:
        xOffset = 362
        yOffset =  30 
        tnXsize = 155    # thumbnail image sizes
        tnYsize =  92
    startDay = item[0:8]
    rawQlImageName = srcDir + item
    annotatedQlImageName = qlTempDir + item
    annotatedTnImageName = tnTempDir + item
    
    # now the annotation
    geometryString = '0x0+' + str(xOffset) + '+' + str(yOffset)
    imAnnotateCommand = imConvert + ' -font /usr/share/fonts/default/truetype/VeraBd.ttf -pointsize 18 -fill black -annotate ' + geometryString + ' \'' + startDay + '\' ' + rawQlImageName + ' ' + annotatedQlImageName
    system(imAnnotateCommand)
    
    # now the scaling to thumbnails
    imResizeCommand  = imConvert + ' -resize ' + str(tnXsize) + 'x' + str(tnYsize) + ' -sharpen 0.25 ' + annotatedQlImageName + '  ' +  annotatedTnImageName
    system(imResizeCommand)

'''
Now the creation of animated gifs:
Commands:
convert -adjoin -delay 50 <qlTempDir>/200603*chl*nos* <qlAnimOutputDir>/200603_chl_nos_ql.gif
convert -adjoin -delay 50 <tnTempDir>/200603*chl*nos* <tnAnimOutputDir>/200603_chl_nos_tn.gif
convert -adjoin -delay 50 <qlTempDir>/200603*chl*bas* <qlAnimOutputDir>/200603_chl_bas_ql.gif
convert -adjoin -delay 50 <tnTempDir>/200603*chl*bas* <tnAnimOutputDir>/200603_chl_bas_tn.gif
'''
baseAdjoinCommand = 'convert -adjoin -delay 50 -coalesce -layers optimize '

for product in products:
    for region in regions:
        qlAdjoinNosCommand = baseAdjoinCommand + qlTempDir + _month + '*' + product + '*' + region + '* ' + \
                             qlAnimOutputDir +  _month + '_' + product + '_' + region + '_ql.gif'
        tnAdjoinNosCommand = baseAdjoinCommand + tnTempDir + _month + '*' + product + '*' + region + '* ' + \
                             tnAnimOutputDir +  _month + '_' + product + '_' + region + '_tn.gif'
        system(qlAdjoinNosCommand)
        system(tnAdjoinNosCommand)


print "\n******************************************************"
print " Script \'process_MC_WAQS_L3_animations.py\' finished.  "
print "******************************************************\n"

# EOF
