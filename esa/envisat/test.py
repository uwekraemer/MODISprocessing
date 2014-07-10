#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: make_daily_IPF_L1b_quicklooks.py

import os
import os.path
import sys
import time

def printUsage ():
    print "Usage: make_daily_IPF_RGB_quicklooks.py region back_day"
    print "where region includes:"
    print "\"NorthSea\",  \"BalticSea or \"Lithuania\"\"\n"
    print "and back_day is an integer value specifying which day to process:"
    print "1 means yesterday, 2 means the day before yesterday, etc."
    print "Maximum value is 32767.\n"

try:
    argc=len(sys.argv)
    if argc < 3:          # the program was called incorrectly
        print "\nToo few parameters passed!"
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if sys.argv[1] in ["NorthSea", "BalticSea", "Lithuania"]:
            # do something
            print "Processing " +str(sys.argv[1]) + " request..."
        else:               # incorrect parameter
            print "Wrong region specifier!"
            printUsage()
            sys.exit(1)
except:
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)    

try:
    back_day = int(sys.argv[2])
except:
    print "back_day parameter must be of type integer!"
    printUsage()
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)

print "\n******************************************************"
print " Script \'make_daily_IPF_L1b_quicklooks.py\' at work... "
print "******************************************************\n"

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

def get_year_from_proc_day(proc_date):
    return proc_date[0:4]

myDate=time.localtime()
proc_day = get_date_string(get_float_day(back_day))
proc_year= get_year_from_proc_day(proc_day)

print proc_day
#sys.exit(1)

# Directories:
srcDir  = '/mnt/hgfs/DISK_E/'+ proc_year + '/06/'
#srcDir  = '/fs14/EOservices/Repositories/MERIS/RR/WAQSrepository/'+ proc_year + '/'
imagesDir = '/fs14/EOservices/OutputPool/quicklooks/WAQS-IPF/daily-RGB/'
hiresImagesDir = imagesDir + 'hires/'
quickLooksDir  = imagesDir + 'quicklooks/'
thumbsDir      = imagesDir + 'thumbs/'

tempProcDir = '/fs14/temp/'

# tools config
l3mosaickingHome   = '/home/uwe/tools/mosaic/'
l3mosaickingScript = l3mosaickingHome + 'mosaic.sh'

pconvertHome = '/home/uwe/tools/pconvert/'
pconvertScript = pconvertHome + 'pconvert.sh'
pconvertConf   = pconvertHome + 'MERIS_L1b_RGB_profile.txt'

imageMagickHome = '/usr/bin/'
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'

label_plate = pconvertHome + 'label_plate.gif'
label_temp  = pconvertHome + 'label_temp.gif'

pixel_size_x = "0.01078"
pixel_size_y = "0.01078"

if sys.argv[1]=="NorthSea":
    regiondestID= '_nos_'
    region = 'North Sea'
    west_lon = "-5.0"           # lon_min
    north_lat = "63.0"          # lat_max
    east_lon = "13.0"           # lon_max
    south_lat = "49.0"          # lat_min
    qlXsize = 354               # quicklook image sizes
    qlYsize = 275
    tnXsize = 118               # thumbnail image sizes
    tnYsize =  92
    landmask_file = pconvertHome + 'nos_landmask.gif'
    l3mosaickingConf   = l3mosaickingHome + 'mosaicIpfNorthSeaSeaDailyRGB.xml'
#elif sys.argv[1]=="Estonia":
#    regiondestID= '_est_'
#    region = 'Estonia'
#    west_lon = "21.702216"           # lon_min
#    north_lat = "60.57032"          # lat_max
#    east_lon = "30.225435"           # lon_max
#    south_lat = "57.058884"          # lat_min
#    qlXsize = 354               # quicklook image sizes
#    qlYsize = 275
#    tnXsize = 118               # thumbnail image sizes
#    tnYsize =  92
#    landmask_file = pconvertHome + 'est_landmask.gif'
#    l3mosaickingConf   = l3mosaickingHome + 'mosaicIpfEstoniaDailyRGB.xml'
elif sys.argv[1]=="Lithuania":
    regiondestID= '_lit_'
    region = 'Lithuania'
    west_lon = "9.0"            # lon_min
    north_lat = "66.0"          # lat_max
    east_lon = "31.0"           # lon_max
    south_lat = "53.0"          # lat_min
    qlXsize = 354               # quicklook image sizes
    qlYsize = 275
    tnXsize = 118               # thumbnail image sizes
    tnYsize =  92
    landmask_file = pconvertHome + 'est_landmask.gif'
    l3mosaickingConf   = l3mosaickingHome + 'mosaicIpfEstoniaDailyRGB.xml'
else:
    regiondestID= '_bas_'
    region = 'Baltic Sea'
    west_lon = "9.0"            # lon_min
    north_lat = "66.0"          # lat_max
    east_lon = "31.0"           # lon_max
    south_lat = "53.0"          # lat_min
    qlXsize = 465              # quicklook image sizes
    qlYsize = 275
    tnXsize = 155              # thumbnail image sizes
    tnYsize =  92
    landmask_file = pconvertHome + 'bas_landmask.gif'
    l3mosaickingConf   = l3mosaickingHome + 'mosaicIpfBalticSeaDailyRGB.xml'

# constant xml-blocks for request
request_init_block =                          '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n'
request_init_block += '<RequestList>\n'
request_init_block += '    <Request type=\"MOSAIC\">\n'
request_init_block += '        <Parameter name=\"west_lon\" value=\"'+west_lon+'\" />\n'
request_init_block += '        <Parameter name=\"north_lat\" value=\"'+north_lat+'\" />\n'
request_init_block += '        <Parameter name=\"east_lon\" value=\"'+east_lon+'\" />\n'
request_init_block += '        <Parameter name=\"south_lat\" value=\"'+south_lat+'\" />\n'
request_init_block += '        <Parameter name=\"projection_name\" value=\"Geographic Lat/Lon\" />\n'
request_init_block += '        <Parameter name=\"projection_parameters\" value=\"\" />\n'
request_init_block += '        <Parameter name=\"pixel_size_x\" value=\"'+pixel_size_x+'\" />\n'
request_init_block += '        <Parameter name=\"pixel_size_y\" value=\"'+pixel_size_y+'\" />\n'
request_init_block += '        <Parameter name=\"orthorectification\" value=\"false\" />\n'
request_init_block += '        <Parameter name=\"orthorectification_dem\" value=\"GETASSE30\" />\n'
request_init_block += '        <Parameter name="radiance_1.expression" value="radiance_1" />\n'
request_init_block += '        <Parameter name="radiance_2.expression" value="radiance_2" />\n'
request_init_block += '        <Parameter name="radiance_3.expression" value="radiance_3" />\n'
request_init_block += '        <Parameter name="radiance_4.expression" value="radiance_4" />\n'
request_init_block += '        <Parameter name="radiance_5.expression" value="radiance_5" />\n'
request_init_block += '        <Parameter name="radiance_6.expression" value="radiance_6" />\n'
request_init_block += '        <Parameter name="radiance_7.expression" value="radiance_7" />\n'
request_init_block += '        <Parameter name="radiance_12.expression" value="radiance_12" />\n'
request_init_block += '        <Parameter name=\"condition_operator\" value=\"OR\" />\n'
request_init_block += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_init_block += '        <Parameter name=\"log_prefix\" value=\"mosaic\" />\n'

input_prefix =                                '        <InputProduct URL=\"file:'
line_delimiter =                                                               '\" />\n'
output_prefix =                               '        <OutputProduct URL=\"file:'

request_closer = "\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n"

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen:
for a in range(list_size):
    for item in src_list:
        if item.startswith('MER_') == False or item.startswith('MER_RR__2P')==True \
        or item.endswith('.N1')    == False or item.find(proc_day) == -1:
            print "Removing " + item + " from list."
            src_list.remove(item)

entry=[]
list_size = len(src_list)
if list_size==0:
    print "Nothing to do here. Now quitting."
    sys.exit(1)

for item in range(list_size):
    entry.append(input_prefix + srcDir + src_list[item] + line_delimiter)

output_filename= tempProcDir + proc_day + regiondestID + "RGB_ipf_1200.dim"
output_block = output_prefix + output_filename

# Requestfile soll noch nicht existieren, bzw. altes loeschen:
if os.path.exists(l3mosaickingConf):
    os.remove(l3mosaickingConf)

# Erst jetzt wird es erzeugt:
requestfile = open(l3mosaickingConf, 'a')
requestfile.write(request_init_block)
for line in range(len(entry)):
    requestfile.write(entry[line])

requestfile.write(output_block)
requestfile.write(request_closer)
requestfile.close()

l3mosaickingCommand = l3mosaickingScript + " " + l3mosaickingConf
print l3mosaickingCommand
print "Processing L3 Mosaic..."
os.system(l3mosaickingCommand)

####################################
# Here we are doing image processing
####################################

# create image of mosaic with pconvert
pconvertCommand = pconvertScript + ' -f jpg -o ' + imagesDir + ' -m off -p ' + pconvertConf  + ' ' +  output_filename
print pconvertCommand + '\n'
os.system(pconvertCommand)

rawImageName              = imagesDir      + proc_day   + regiondestID + 'RGB_ipf_1200.jpg'
hiresImageName            = hiresImagesDir + proc_day   + regiondestID + 'RGB_ipf_1200.jpg'      # e.g. 20060716_nos_RGB_ipf_1200.jpg
currentHiresImageName     = imagesDir + 'current_daily' + regiondestID + 'RGB_ipf_max.jpg'       # e.g. current_daily_nos_RGB_ipf_max.jpg
quicklookImageName        = quickLooksDir  + proc_day   + regiondestID + 'RGB_ipf_1200_ql.jpg'   # e.g. 20060716_nos_RGB_ipf_1200_ql.jpg
currentQuicklookImageName = imagesDir + 'current_daily' + regiondestID + 'RGB_ipf_275.jpg'       # e.g. current_daily_nos_RGB_ipf_275.jpg
thumbnailImageName        = thumbsDir      + proc_day   + regiondestID + 'RGB_ipf_1200_tn.jpg'   # e.g. 20060716_nos_RGB_ipf_1200_tn.jpg

# Now we overlay the landmask
# composite -gravity center -dissolve 25% nos_landmask.gif 20060716_nos_RGB_ipf_1200.jpg 20060716_nos_RGB_ipf_1200.jpg
imCompositeCommand = imComposite + ' -gravity center -dissolve 25% ' + landmask_file + ' ' + rawImageName + '  ' +  rawImageName
os.system(imCompositeCommand)

# Now a little bit of metadata annotation
imAnnotateCommand = imConvert + ' -font /usr/share/fonts/truetype/AT833___.TTF -pointsize 24 -fill white -annotate 0x0+26+37 \'' + proc_day + ', ' + region + '\n(c) Brockmann Consult \' ' + label_plate + ' ' + label_temp
print imAnnotateCommand
os.system(imAnnotateCommand)
imCompositeCommand2 = imComposite + ' -gravity southeast ' + label_temp + ' ' + rawImageName + '  ' +  rawImageName
os.system(imCompositeCommand2)

# now the scaling to quicklooks
imResizeCommand  = imConvert + ' -resize ' + str(qlXsize) + 'x' + str(qlYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  quicklookImageName
os.system(imResizeCommand)

# now the scaling to thumbs
imResizeCommand2 = imConvert + ' -resize ' + str(tnXsize) + 'x' + str(tnYsize) + ' -sharpen 0.25 ' + rawImageName + '  ' +  thumbnailImageName
os.system(imResizeCommand2)

mvCommand = 'mv ' + rawImageName + ' ' + hiresImageName
os.system(mvCommand)

# now we copy the recent quicklook and hires images
copyHiresCommand = 'cp ' + hiresImageName + ' ' + currentHiresImageName
os.system(copyHiresCommand)

copyQuicklookCommand = 'cp ' + quicklookImageName + ' ' + currentQuicklookImageName
os.system(copyQuicklookCommand)

####################################

# Now delete the temporary mosaic:
dataDir=output_filename[0:len(output_filename)-2] + 'ata'
#os.remove(output_filename)
removedirCommand = 'rm -rf ' + dataDir
print removedirCommand + '\n'
#os.system(removedirCommand)

print "\n******************************************************"
print " Script \'make_daily_IPF_L1b_quicklooks.py\' finished.  "
print "******************************************************\n"

# EOF
