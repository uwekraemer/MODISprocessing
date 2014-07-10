#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_MC_daily_and_weekly_overview_images_assembly.py

# Creation of image overviews using ImageMagick

import os
from time import localtime, strftime

print "\n****************************************************************************"
print " Script \'launch_MC_daily_and_weekly_overview_images_assembly.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************************************************\n"

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/Volumes/UWE/cronjobs/'

mc_weekly_script = modules_home + 'compute_overview_image_MC_weekly_running.py'
# /home/uwe/cronjobs/compute_overview_image_MC_weekly_running.py NorthSea
mc_weekly_nos_call = mc_weekly_script + " NorthSea"
os.system(mc_weekly_nos_call)
# /home/uwe/cronjobs/compute_overview_image_MC_weekly_running.py BalticSea
mc_weekly_bas_call = mc_weekly_script + " BalticSea"
os.system(mc_weekly_bas_call)


mc_daily_script = modules_home + 'compute_overview_image_MC_daily_running.py'
# /home/uwe/cronjobs/compute_overview_image_MC_weekly_running.py NorthSea
mc_daily_nos_call = mc_daily_script + " NorthSea"
os.system(mc_daily_nos_call)
# /home/uwe/cronjobs/compute_overview_image_MC_weekly_running.py BalticSea
mc_daily_bas_call = mc_daily_script + " BalticSea"
os.system(mc_daily_bas_call)


rgb_daily_script = modules_home + 'compute_overview_image_RGB_daily_running.py' 
# /home/uwe/cronjobs/compute_overview_image_RGB_daily_running.py NorthSea
rgb_daily_nos_call = rgb_daily_script + " NorthSea"
os.system(rgb_daily_nos_call)

# /home/uwe/cronjobs/compute_overview_image_RGB_daily_running.py BalticSea;
rgb_daily_bas_call = rgb_daily_script + " BalticSea"
os.system(rgb_daily_bas_call)

print "\n****************************************************************************"
print " Script \'launch_MC_daily_and_weekly_overview_images_assembly.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************************************************\n"

