#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_IPF_daily_RGB_image_creation.py

# creation of RGB images of IPF L1b products

import os
import sys
from time import localtime, strftime

def printUsage():
    print("Usage: launch_IPF_daily_RGB_image_creation.py \'back_day\'")
    print("where back_day is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

try:
    argc=len(sys.argv)
    if argc == 1:          # the program was called without parameters
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

print("\n************************************************************")
print(" Script \'launch_IPF_daily_RGB_image_creation.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("************************************************************\n")

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/Volumes/UWE/cronjobs/'

the_script = modules_home + 'make_daily_IPF_L1b_quicklooks.py'

bas_call = the_script + " BalticSea " + str(back_day)
os.system(bas_call)
#nos_call = the_script + " NorthSea " + str(back_day)
#os.system(nos_call)


print("\n************************************************************")
print(" Script \'launch_IPF_daily_RGB_image_creation.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("************************************************************\n")

# EOF
