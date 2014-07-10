#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_IPF_daily_and_weekly_image_processing_and_web_site_creation.py

# creation of images of IPF daily and weekly products, syncing with web server 
# Note: no web pages creation yet.

import os
import sys
from time import localtime, strftime

def printUsage():
    print "Usage: launch_IPF_weekly_image_processing_and_web_site_creation.py \'back_day\'"
    print "where back_day is an integer value specifying which day to process:"
    print "1 means yesterday, 2 means the day before yesterday, etc."
    print "Maximum value is 32767.\n"

try:
    argc=len(sys.argv)
    if (argc == 1):          # the program was called without parameters
        print "\'back_day\' specifier is missing!\n"
        sys.exit(1)
    else:
        try:
            back_day = int(sys.argv[1])
        except:
            print "\back_day must be of type integer!\n"
            sys.exit(1)        
except:
    printUsage()
    print "Error in parameters. Now exiting..."
    sys.exit(1)    

print "\n*******************************************************************************************"
print " Script \'launch_IPF_daily_and_weekly_image_processing_and_web_site_creation.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "*******************************************************************************************\n"

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/Volumes/UWE/cronjobs/'

images_src_dir = '/fs14/EOservices/OutputPool/quicklooks/WAQS-IPF/'
images_web_dir = '/var/www/images/WAQS-IPF/'

# /home/uwe/cronjobs/apply_color_palettes_IPF_WAQS_L3.py 1
weekly_call = modules_home + 'apply_color_palettes_IPF_WAQS_L3.py ' + str(back_day)
os.system(weekly_call)

# /home/uwe/cronjobs/apply_color_palettes_IPF_WAQS_daily.py 1
daily_call = modules_home + 'apply_color_palettes_IPF_WAQS_daily.py ' + str(back_day)

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/quicklooks/ uwe@bcweb:/var/www/images/
image_sync_command = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" '+ images_src_dir +' uwe@bcweb:' + images_web_dir
os.system(image_sync_command)

print "\n*******************************************************************************************"
print " Script \'launch_IPF_daily_and_weekly_image_processing_and_web_site_creation.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "*******************************************************************************************\n"

# EOF