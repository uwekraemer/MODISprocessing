#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_MC_merging_and_weekly_L3_binning.py

# MC Merging and weekly L3 Processing chain

import os
from time import localtime, strftime

print "\n****************************************************************"
print " Script \'launch_MC_merging_and_weekly_L3_binning.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************************************\n"

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/Volumes/UWE/cronjobs/'

# /home/uwe/cronjobs/merge_netCDF_products.py
merging_script = modules_home + 'merge_netCDF_products.py'
os.system(merging_script)

estonia_daily_script = modules_home + 'process_Estonia_daily_mosaicking.py 2'
os.system(estonia_daily_script)

binning_script = modules_home + 'process_MC_weekly_L3_binning.py '
# /home/uwe/cronjobs/process_MC_weekly_L3_binning.py 'NorthSea' 1
nos_call = binning_script + " NorthSea "  + '2'
os.system(nos_call)

# /home/uwe/cronjobs/process_MC_weekly_L3_binning.py 'BalticSea' 1
bas_call = binning_script + " BalticSea " + '2' 
os.system(bas_call)

# /home/uwe/cronjobs/process_MC_weekly_L3_binning.py 'Estonia' 1
est_call = binning_script + " Estonia " + '2' 
os.system(est_call)

# be sure that the bin-databases have been emptied:
l3_bin_databases = [\
'/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_northsea.bindb', \
'/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_estonia.bindb', \
'/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_balticsea.bindb']

for item in l3_bin_databases:
    rm_call = 'rm -rf ' + item + '/*'
    #print rm_call
    os.system(rm_call)

print "\n****************************************************************"
print " Script \'launch_MC_merging_and_weekly_L3_binning.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************************************\n"

# EOF