#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_products_on_ftp_for_bsh.py

# zip MC products that are made for the BSH and put them on ftp

from os import system
from sys import exit
from time import localtime, strftime
from configparser import ConfigParser

print("\n************************************************************")
print(" Script \'zip_and_put_products_on_ftp_for_bsh.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("************************************************************\n")

modules_home = '/home/uwe/cronjobs/esa/envisat/modules/'
zipping_script = modules_home + 'zip_dimap_files.py'
rsync_header_string = 'rsync -avuPH --ignore-existing --rsh=\"ssh -l uwe\" '

configDir  ='/home/uwe/tools/config/'
configFilePath = configDir + 'zipDirConfig.ini'
config = ConfigParser()
config.read(configFilePath)

num_dirs  = int(config.get("meta", "dirs"))
src_dirs  = []
dest_dirs = []
for dir_index in range(num_dirs):
    src_dirs.append(config.get("srcDirectories", "srcDir"+ str(dir_index)))
    src_dirs[dir_index] += "zipped/"
    dest_dirs.append(config.get("destDirectories", "destDir"+ str(dir_index)))

#===============================================================================
# src_dirs = ['/fs14/EOservices/OutputPool/MODIS/WAQS-MC/weekly/', \
#            '/fs14/EOservices/OutputPool/MODIS/WAQS-MC/daily-merged/']
# 
# dest_dirs = ['/data/bcserver8/ftp/waqs-bsh/MODIS/running_weeklymean/', 
#              '/data/bcserver8/ftp/waqs-bsh/MODIS/daily_MC/']
#===============================================================================

dir_index = 0
zip_call = zipping_script + ' ' + str(dir_index)
system(zip_call)
bas_sync_call = rsync_header_string + src_dirs[dir_index] + '*_bas_* uwe@10.1.0.2:' + dest_dirs[dir_index] + 'BalticSea/'
print(bas_sync_call)
system(bas_sync_call)
nos_sync_call = rsync_header_string + src_dirs[dir_index] + '*_nos_* uwe@10.1.0.2:' + dest_dirs[dir_index] + 'NorthSea/'
print(nos_sync_call)
system(nos_sync_call)

dir_index = 1
# For MC daily-merged we have differing names:
zip_call = zipping_script + ' ' + str(dir_index)
system(zip_call)
sync_daily_mc_bas_prods_call =  rsync_header_string + src_dirs[dir_index] + '*_BALTIC_* uwe@10.1.0.2:' + dest_dirs[dir_index] + 'BalticSea/'
print(sync_daily_mc_bas_prods_call)
system(sync_daily_mc_bas_prods_call)
sync_daily_mc_nos_prods_call =  rsync_header_string + src_dirs[dir_index] + '*_NSEA_* uwe@10.1.0.2:' + dest_dirs[dir_index] + 'NorthSea/'
print(sync_daily_mc_nos_prods_call)
system(sync_daily_mc_nos_prods_call)


print("\n***********************************************************")
print(" Script \'zip_and_put_products_on_ftp_for_bsh.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("***********************************************************\n")

# EOF