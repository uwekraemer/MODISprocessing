#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_daily_wew_L3_mosaicking_noflags.py

# L3 Mosaic Processing for WeW L2 products

import os
from time import localtime, strftime

print("\n***************************************************************")
print(" Script \'launch_daily_wew_L3_mosaicking_noflags.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("***************************************************************\n")

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/Volumes/UWE/cronjobs/'

requests = ['NorthSea', 'BalticSea', 'Estonia']
#requests = ['NorthSea', 'BalticSea', 'UK', 'Estonia']
back_day = '1'

the_script   = modules_home + 'merge_daily_wew_L3_mosaicking.py '

for item in requests:
    call = the_script + ' ' + item + ' ' + back_day
    print(call)
    os.system(call)

print("\n***************************************************************")
print(" Script \'launch_daily_wew_L3_mosaicking_noflags.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("***************************************************************\n")

# EOF
