#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_wew_L3_processing.py

# FUB WeW L2 Processing for Meris child products

import os
import sys
from time import localtime, strftime

def printUsage():
    print "Usage: launch_wew_L3_processing.py back_day"
    print "where back_day is an integer value specifying the start day to process:"
    print "1 means yesterday, 2 means the day before yesterday, etc."
    print "Maximum value is 32767.\n"

try:
    argc=len(sys.argv)
    if (argc < 2):          # the program was called incorrectly
        print "\nToo few parameters passed!"
        printUsage()
        sys.exit(1)
except:
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)    

try:
    backDay = sys.argv[1]
except:
    print "back_day parameter must be of type integer!"
    printUsage()
    print "\nError in parameters. Now exiting...\n"
    sys.exit(1)



print "\n********************************************************"
print " Script \'launch_wew_L3_processing.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "********************************************************\n"

modules_home = '/home/uwe/cronjobs/modules/'
l3_script = modules_home + 'process_wew_weekly_L3.py'
# /home/uwe/cronjobs/modules/process_wew_weekly_L3.py NorthSea 1
nos_script = l3_script + ' NorthSea '  + backDay
os.system(nos_script)

# /home/uwe/cronjobs/modules/process_wew_weekly_L3.py BalticSea 1
bas_script = l3_script + ' BalticSea ' + backDay
os.system(bas_script)

# /home/uwe/cronjobs/modules/process_wew_weekly_L3.py UK 1
#uk_script = l3_script + ' UK ' + backDay
#os.system(uk_script)

# /home/uwe/cronjobs/modules/process_wew_weekly_L3.py Estonia 1
est_script = l3_script + ' Estonia ' + backDay
os.system(est_script)

print "\n********************************************************"
print " Script \'launch_wew_L3_processing.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "********************************************************\n"

# EOF