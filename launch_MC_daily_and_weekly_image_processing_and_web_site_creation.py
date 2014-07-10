#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_MC_daily_and_weekly_image_processing_and_web_site_creation.py

# creation of images of MC daily and weekly products, syncing with web server 

import os
import sys
from time import localtime, strftime

def printUsage():
    print("Usage: launch_MC_daily_and_weekly_image_processing_and_web_site_creation.py \'back_day\'")
    print("where back_day is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print("\'back_day\' specifier is missing!\n")
        sys.exit(1)
    else:
        try:
            back_day = int(sys.argv[1])
        except:
            print("\back_day must be of type integer!\n")
            sys.exit(1)        
except:
    printUsage()
    print("Error in parameters. Now exiting...")
    sys.exit(1)    

print("\n******************************************************************************************")
print(" Script \'launch_MC_daily_and_weekly_image_processing_and_web_site_creation.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("******************************************************************************************\n")

print("Processing products " + str(back_day) + " days old...")
modules_home = '/home/uwe/cronjobs/nasa/modis/'
#modules_home = '/Volumes/UWE/cronjobs/'

images_src_dir        = '/fs14/EOservices/OutputPool/quicklooks/WAQS-MC-MODIS/'

weekly_png_images_src_dir = images_src_dir + 'weekly_png/'


png_images_web_dir    = '/var/www/www.waqss.de/product_images/'

# /home/uwe/cronjobs/modules/apply_color_palettes_MC_WAQSS2_L3.py 2
weekly_call2 = modules_home + 'apply_color_palettes_modis_MC_WAQSS2_L3.py ' + str(back_day)
os.system("python " + weekly_call2)

# /home/uwe/cronjobs/apply_color_palettes_MC_WAQS_L3.py 2
#sst_call2 = modules_home + 'apply_color_palettes_SST_WAQSS2_L3.py '   + str(back_day)
#os.system("python " + sst_call2)

# rsync -avupogtP --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly_png/ uwe@apache:/local/disk1/webservers/www.waqss.de/static/waqss/product_images/
weekly_png_sync = 'rsync -avuPH --rsh=\"ssh -l uwe\" ' + weekly_png_images_src_dir + ' uwe@10.1.0.2:' + png_images_web_dir
print(weekly_png_sync)
os.system(weekly_png_sync)

print("\n******************************************************************************************")
print(" Script \'launch_MC_daily_and_weekly_image_processing_and_web_site_creation.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("******************************************************************************************\n")

# EOF
