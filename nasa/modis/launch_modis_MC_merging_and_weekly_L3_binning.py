#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_MC_merging_and_weekly_L3_binning.py

# MC Merging and weekly L3 Processing chain

from os import system
from sys import argv
from time import localtime, strftime

print("\n**********************************************************************")
print(" Script \'launch_modis_MC_merging_and_weekly_L3_binning.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("**********************************************************************\n")

def printUsage():
    print("Usage: launch_modis_MC_merging_and_weekly_L3_binning.py back_day")
    print("where backDay is an integer value specifying the start day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")


argc=len(argv)
if argc < 2:          # the program was called incorrectly
    print("\nToo few parameters passed!")
    printUsage()
    exit(1)

try:
    backDay = int(argv[1])
except TypeError:
    print("backDay parameter must be of type integer!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    exit(1)


modules_home = '/home/uwe/cronjobs/nasa/modis/'

# /home/uwe/cronjobs/merge_netCDF_products.py
merging_script = modules_home + 'merge_modis_netCDF_products.py ' + str(backDay)
system("python "+ merging_script)

#TODO include in processing
#estonia_daily_script = modules_home + 'process_Estonia_daily_modis_mosaicking.py 2'
#os.system(estonia_daily_script)

binning_script = modules_home + 'process_modis_MC_weekly_L3_binning.py '
# /home/uwe/cronjobs/process_modis_MC_weekly_L3_binning.py 'NorthSea' 1
nos_call = binning_script + " NorthSea "  + str(backDay)
system("python "+ nos_call)

# /home/uwe/cronjobs/process_modis_MC_weekly_L3_binning.py 'BalticSea' 1
bas_call = binning_script + " BalticSea " + str(backDay)
system("python "+ bas_call)

#TODO include in processing
# /home/uwe/cronjobs/process_modis_MC_weekly_L3_binning.py 'Estonia' 1
est_call = binning_script + " Estonia " + str(backDay)
system("python "+ est_call)

# be sure that the bin-databases have been emptied:
l3_bin_databases = [\
'/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_northsea.bindb', \
'/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_balticsea.bindb', \
'/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_estonia.bindb']

for item in l3_bin_databases:
    rm_call = 'rm -rf ' + item + '/*'
    #print rm_call
    system(rm_call)

print("\n*********************************************************************")
print(" Script \'launch_modis_MC_merging_and_weekly_L3_binning.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("*********************************************************************\n")

# EOF