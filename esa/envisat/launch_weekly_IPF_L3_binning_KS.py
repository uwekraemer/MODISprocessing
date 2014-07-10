#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_weekly_IPF_L3_binning.py

# L3 binning of IPF childs

import os
from time import localtime, strftime

print("\n********************************************************")
print(" Script \'launch_weekly_IPF_L3_binning.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("********************************************************\n")

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/Volumes/UWE/cronjobs/'

binning_script = modules_home + 'process_IPF_weekly_L3_binning.py'

# /home/uwe/cronjobs/modules/process_IPF_weekly_L3_binning.py 'BalticSea' 1
bas_call = binning_script + " BalticSea 1"
os.system(bas_call)

bas_call = binning_script + " BalticSea 2"
os.system(bas_call)

bas_call = binning_script + " BalticSea 3"
os.system(bas_call)

bas_call = binning_script + " BalticSea 4"
os.system(bas_call)

bas_call = binning_script + " BalticSea 5"
os.system(bas_call)

bas_call = binning_script + " BalticSea 6"
os.system(bas_call)

# /home/uwe/cronjobs/modules/process_IPF_weekly_L3_binning.py 'NorthSea' 1
nos_call = binning_script + " NorthSea 1"
os.system(nos_call)

nos_call = binning_script + " NorthSea 2"
os.system(nos_call)

nos_call = binning_script + " NorthSea 3"
os.system(nos_call)

nos_call = binning_script + " NorthSea 4"
os.system(nos_call)

nos_call = binning_script + " NorthSea 5"
os.system(nos_call)


# /home/uwe/cronjobs/modules/process_IPF_weekly_L3_binning.py 'UK' 1
#uk_call = binning_script + " UK 1"
#os.system(uk_call)

print("\n********************************************************")
print(" Script \'launch_weekly_IPF_L3_binning.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("********************************************************\n")

#EOF
