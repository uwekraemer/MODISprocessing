#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_aatsr_orbits_processing.py

# creation and L3 binning of IPF childs

from os import system
from time import localtime, strftime

print("\n*******************************************************")
print(" Script \'launch_aatsr_orbits_processing.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("*******************************************************\n")

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/Volumes/UWE/cronjobs/'

# /home/uwe/cronjobs/modules/make_WAQS_AATSR_childs.py <type>
nr_childgen_script = modules_home + 'make_AATSR_childs.py NR'
system(nr_childgen_script)

# /home/uwe/cronjobs/modules/merge_daily_AATSR_L3_mosaicking.py <region> <back_day>
nr_mosaicking_nos_script = modules_home + 'merge_daily_AATSR_L3_mosaicking.py NorthSea 1'
nr_mosaicking_bas_script = modules_home + 'merge_daily_AATSR_L3_mosaicking.py BalticSea 1'
system(nr_mosaicking_nos_script)
system(nr_mosaicking_bas_script)

toa_childgen_script = modules_home + 'make_AATSR_childs.py TOA'
system(toa_childgen_script)

nr_calval_register_script = modules_home + "register_CalVal_childs.py AATSR NR"
system(nr_calval_register_script)

toa_calval_register_script = modules_home + "register_CalVal_childs.py AATSR TOA"
system(toa_calval_register_script)

remove_old_orbits_script = modules_home + "remove_old_files.py"
system(remove_old_orbits_script)

processing_script = modules_home + 'process_AATSR_childs_L3_flux.py'
l3_nos_script = processing_script + " NorthSea"
system(l3_nos_script)

l3_bas_script = processing_script + " BalticSea"
system(l3_bas_script)

print("\n*******************************************************")
print(" Script \'launch_aatsr_orbits_processing.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("*******************************************************\n")

# EOF
