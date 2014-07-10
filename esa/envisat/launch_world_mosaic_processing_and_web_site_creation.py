#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_world_mosaic_processing_and_web_site_creation.py

# mosaicking of all MERIS orbits of one day, creation of the WAQSS Daily Mosaics web pages

import os
import sys
from time import localtime, strftime

def printUsage():
    print "Usage: launch_world_mosaic_processing_and_web_site_creation.py \'back_day\'"
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

print "\n*****************************************************************************"
print " Script \'launch_world_mosaic_processing_and_web_site_creation.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "*****************************************************************************\n"

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/Volumes/UWE/cronjobs/'

images_src_dir = '/fs14/EOservices/OutputPool/quicklooks/daily_mosaics/'
images_web_dir = '/local/disk1/webservers/www.waqss.de/static/images/daily_mosaics/'

html_src_dir = images_src_dir + 'html/'
html_web_dir = '/local/disk1/webservers/www.waqss.de/htdocs/waqss/mosaics/'

# /home/uwe/cronjobs/make_world_mosaic.py 1
mosaicking_call = modules_home + 'make_world_mosaic.py ' + str(back_day)
os.system(mosaicking_call)

# /home/uwe/cronjobs/make_mosaic_website.py
website_script = modules_home + 'make_mosaic_website.py'
os.system(website_script)

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/quicklooks/daily_mosaics/ uwe@10.1.0.2:/local/disk1/webservers/www.waqss.de/static/images/daily_mosaics/
image_sync_command = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" '+ images_src_dir +' uwe@10.1.0.2:' + images_web_dir
os.system(image_sync_command)

# rsync -avupogtP --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/quicklooks/daily_mosaics/html/ uwe@10.1.0.2:/local/disk1/webservers/www.waqss.de/htdocs/waqss/mosaics/
html_sync_call = 'rsync -avupogtP --rsh=\"ssh -l uwe\" '+ html_src_dir +' uwe@10.1.0.2:'+ html_web_dir
os.system(html_sync_call)

print "\n*****************************************************************************"
print " Script \'launch_world_mosaic_processing_and_web_site_creation.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "*****************************************************************************\n"

# EOF
