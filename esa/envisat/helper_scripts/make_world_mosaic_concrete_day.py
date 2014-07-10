#!/usr/bin/env python
# -*- coding: latin-1 -*-
# file: make_world_mosaic_concrete_day.py

import os
import os.path
import sys
import time

def printUsage():
    print("Usage: make_world_mosaic_concrete_day.py date")
    print("where date is a string value specifying which day to process:")
    print("e.g. 20070715.\n")

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print("\nDate specifier is missing!\n")
        sys.exit(1)
    else:
        arrival_day = sys.argv[1]
except:
    printUsage()
    print("Error in parameters. Now exiting...\n")
    sys.exit(1)    

print("\n*******************************************************")
print(" Script \'make_world_mosaic_concrete_day.py\' at work... ")
print("*******************************************************\n")

_year = arrival_day[0:4]
_month = arrival_day[4:6]

# Directories
baseDir = '/fs14/EOservices/Repositories/MERIS/RR/DDSrepository/'
srcDir  = baseDir + _year + '/' + _month+ '/'
tempProcDir = '/fs14/temp/'
mosaicsBaseDir = '/fs14/EOservices/OutputPool/quicklooks/daily_mosaics/'
rawImagesDir = mosaicsBaseDir + _year + '/' + _month + '/'     # must exist
if not os.path.exists(rawImagesDir):
    print("Creating directory: " + rawImagesDir)
    os.makedirs(rawImagesDir, 0o777)
webImagesDir  = mosaicsBaseDir + 'web_images/'
thumbsDestDir = mosaicsBaseDir + 'thumbs/'
iconsDestDir  = mosaicsBaseDir + 'icons/'

# File names for output
dimap_output_filename = tempProcDir   + arrival_day+ '_mosaic.dim'       # mosaic dimap
ql_output_filename    = rawImagesDir  + arrival_day+ '_mosaic.jpg'       # image without watermark and text
web_output_filename   = webImagesDir  + arrival_day+ '_mosaic_cr.jpg'    # for web: hires image with watermarks and text 
tn_output_filename    = thumbsDestDir + arrival_day+ '_mosaic_small.jpg' # for web: 10% scaled images 
icn_output_filename   = iconsDestDir  + arrival_day+ '_mosaic_icon.jpg'  # for web:  5% scaled images

# tools config
mosaicHome   = '/home/uwe/tools/mosaic/'
mosaicScript = mosaicHome + 'mosaic.sh'
mosaicConf   = mosaicHome + 'requests/world_mosaic_' + arrival_day + '.xml'

pconvertHome = '/home/uwe/tools/pconvert/'
pconvertScript = pconvertHome + 'pconvert.sh'
pconvertConf   = pconvertHome + 'MERIS_L1b_RGB_profile.txt'

imageMagickHome = '/usr/bin/'
imConvert       = imageMagickHome + 'convert'
imComposite     = imageMagickHome + 'composite'

# Map boundaries and resolution
west_lon = "-180.0"
north_lat = "90.0"
east_lon = "180.0"
south_lat = "-90.0"
pixel_size_x = "0.06666667"
pixel_size_y = "0.06666667"

# konstant xml-blocks for request
request_const_block =  "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
request_const_block += "<RequestList>\n"
request_const_block += "    <Request type=\"MOSAIC\">\n"
request_const_block += "        <Parameter name=\"west_lon\" value=\"" + west_lon+ "\" />\n"
request_const_block += "        <Parameter name=\"north_lat\" value=\""+ north_lat +"\" />\n"
request_const_block += "        <Parameter name=\"east_lon\" value=\""+east_lon+"\" />\n"
request_const_block += "        <Parameter name=\"south_lat\" value=\""+south_lat+"\" />\n"
request_const_block += "        <Parameter name=\"projection_name\" value=\"Geographic Lat/Lon\" />\n"
request_const_block += "        <Parameter name=\"projection_parameters\" value=\"\" />\n"
request_const_block += "        <Parameter name=\"pixel_size_x\" value=\""+pixel_size_x+"\" />\n"
request_const_block += "        <Parameter name=\"pixel_size_y\" value=\""+pixel_size_y+"\" />\n"
request_const_block += "        <Parameter name=\"orthorectification\" value=\"false\" />\n"
request_const_block += "        <Parameter name=\"orthorectification_dem\" value=\"GETASSE30\" />\n"
request_const_block += "        <Parameter name=\"radiance_1.expression\" value=\"radiance_1\" />\n"
request_const_block += "        <Parameter name=\"radiance_2.expression\" value=\"radiance_2\" />\n"
request_const_block += "        <Parameter name=\"radiance_3.expression\" value=\"radiance_3\" />\n"
request_const_block += "        <Parameter name=\"radiance_4.expression\" value=\"radiance_4\" />\n"
request_const_block += "        <Parameter name=\"radiance_5.expression\" value=\"radiance_5\" />\n"
request_const_block += "        <Parameter name=\"radiance_6.expression\" value=\"radiance_6\" />\n"
request_const_block += "        <Parameter name=\"radiance_7.expression\" value=\"radiance_7\" />\n"
request_const_block += "        <Parameter name=\"radiance_12.expression\" value=\"radiance_12\" />\n"
request_const_block += "        <Parameter name=\"condition_operator\" value=\"OR\" />\n"
request_const_block += "        <Parameter name=\"variable_0.expression\" value=\"not l1_flags.INVALID\" />\n"
request_const_block += "        <Parameter name=\"variable_0.condition\" value=\"true\" />\n"
request_const_block += "        <Parameter name=\"variable_0.output\" value=\"false\" />\n"
request_const_block += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_const_block += "        <Parameter name=\"log_prefix\" value=\"mosaic\" />\n"
input_prefix   =       "        <InputProduct URL=\"file:"
line_delimiter =       "\" />\n"
output_prefix  =       "        <OutputProduct URL=\"file:"
block_close    =       "    </Request>\n"
request_closer =       "\" format=\"BEAM-DIMAP\" />\n"
request_closer +=      "    </Request>\n"
request_closer +=      "</RequestList>\n"

# Fetch listing of input directory
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Remove non-MERIS and Level2 products from list:
for a in range(list_size):
    for item in src_list:
        if item.startswith('MER_')==0 or item.startswith('MER_RR__2P')==1:
            print("Removing " + item + " from list.")
            src_list.remove(item)

list_size = len(src_list)

if list_size == 0:
    print("Nothing to do here. Now quitting.")
    sys.exit(1)

# Copy all products from arrival day to final processing list
proc_list  = {}
proc_count = 0
orbits = []

for item in src_list:
    if item.find(arrival_day)>0:
        print(arrival_day+" found in "+ item)
        print("Adding ", item, "to proc_list")
        proc_list[proc_count]=item
        orbit = item[49:54]
        print("Orbit " + orbit)
        orbits.append(int(orbit))
        proc_count=proc_count+1

orbits.sort()
print(orbits)

num_orbits = len(orbits) 

orbit_range = ', Orbits '+ str(orbits[0]) + ' - ' + str(orbits[num_orbits - 1]) + ' '

entry={}
for item in proc_list:
    entry[item] = input_prefix + srcDir + proc_list[item] + line_delimiter

# Remove request file if it exists:
if os.path.exists(mosaicConf):
    os.remove(mosaicConf)

# Create request file now
requestfile = open(mosaicConf, 'a')
requestfile.write(request_const_block)
for line in range(len(entry)):
    requestfile.write(entry[line])

requestfile.write(output_prefix + dimap_output_filename + request_closer)
requestfile.close()

# Invoke mosaic processor
mosaicCommand = mosaicScript + " " + mosaicConf
print(mosaicCommand + '\n')
print("Mosaicking...")
os.system(mosaicCommand)

# create image of mosaic with pconvert
pconvertCommand = pconvertScript + ' -f jpg -o ' + rawImagesDir + ' -m off -p ' + pconvertConf + ' -W 5400 ' +  dimap_output_filename
print(pconvertCommand + '\n')
os.system(pconvertCommand)

# Annotate the copyright with ImageMagick:
# convert -font /usr/share/fonts/truetype/AT833___.TTF -pointsize 36 -stroke black -fill DarkOliveGreen3 -annotate 0x0+20+100 'u"©" 2006 Brockmann Consult' 20060508_mosaic.jpg 20060508_mosaic.jpg
#imAnnotateCommand = imConvert + ' -font /usr/share/fonts/truetype/AT833___.TTF -pointsize 36 -stroke black -fill black -annotate 0x0+20+100 \'© ' + _year + ' Brockmann Consult\' ' + ql_output_filename + ' ' + web_output_filename
imAnnotateCommand = imConvert + ' -font /usr/share/fonts/truetype/AT833___.TTF -pointsize 36 -stroke white -fill white -annotate 0x0+20+100 \'© ' + _year + ' Brockmann Consult\' ' + ql_output_filename + ' ' + web_output_filename
print(imAnnotateCommand + '\n')
os.system(imAnnotateCommand)

# Annotate also the acquisition date and orbits
# convert -font /usr/share/fonts/truetype/AT833___.TTF -pointsize 36 -stroke white -fill white -annotate 0x0+20+2675 'Acquisition date: 20060508, Orbits 12345 - 12349' 20060508_mosaic_test.jpg 20060508_mosaic_test.jpg
imAnnotateCommand2 = imConvert + ' -font /usr/share/fonts/truetype/AT833___.TTF -pointsize 36 -stroke white -fill white -annotate 0x0+20+2675 \'Acquisition date:  ' + arrival_day + orbit_range +'\' ' + web_output_filename + ' ' + web_output_filename
print(imAnnotateCommand2 + '\n')
os.system(imAnnotateCommand2)

# Overlay BC-Logo with ImageMagick:
# composite -gravity southeast BC-Logo-72px.jpg 20060508_mosaic.jpg 20060508_mosaic.jpg
imCompositeCommand = imComposite +' -gravity southeast ' + pconvertHome + 'BC-Logo-72px.jpg' + ' ' + web_output_filename + ' ' + web_output_filename
print(imCompositeCommand + '\n')
os.system(imCompositeCommand)

# Hide BC-Logo inside the composite (stegano option, here important the offset: 137).
imCompositeCommand2 = imComposite +' -stegano 137 ' + pconvertHome + 'BC-Logo-72px.jpg' + ' ' + web_output_filename + ' ' + web_output_filename
print(imCompositeCommand2 + '\n')
os.system(imCompositeCommand2)

# Create thumbnail with ImageMagick:
# convert -resize 810x405 20060506_mosaic.jpg 20060506_mosaic_small.jpg
imResizeCommand = imConvert + ' -resize 810x405 -sharpen 0.25 ' + web_output_filename + '  ' +  tn_output_filename
print(imResizeCommand + '\n')
os.system(imResizeCommand)

# Create icon with ImageMagick:
# convert -resize 810x405 20060506_mosaic.jpg 20060506_mosaic_small.jpg
imResizeCommand2 = imConvert + ' -resize 270x135 ' + web_output_filename + '  ' +  icn_output_filename
print(imResizeCommand2 + '\n')
os.system(imResizeCommand2)

# Now delete the temporary mosaic:
dataDir=dimap_output_filename[0:len(dimap_output_filename)-2] + 'ata'
os.remove(dimap_output_filename)
removedirCommand = 'rm -rf ' + dataDir
print(removedirCommand + '\n')
os.system(removedirCommand)

print("\n******************************************************")
print(" Script \'make_world_mosaic_concrete_day.py\' finished. ")
print("******************************************************\n")

# EOF
