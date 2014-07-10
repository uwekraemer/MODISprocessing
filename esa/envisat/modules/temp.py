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

modules_home = '/home/uwe/cronjobs/modules/'
zipping_script = modules_home + 'zip_dimap_files.py'
rsync_header_string = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" '

configDir  ='/home/uwe/tools/config/'

configFilePath = configDir + 'zipDirConfig.ini'
config = ConfigParser()
config.read(configFilePath)

num_dirs  = int(config.get("ematter", "dirs"))
src_dirs  = []
dest_dirs = []
for dir_index in range(num_dirs):
    src_dirs.append(config.get("srcDirectories", "srcDir"+ str(dir_index)))
    src_dirs[dir_index] += "zipped/"
    dest_dirs.append(config.get("destDirectories", "destDir"+ str(dir_index)))

#===============================================================================
# src_dirs = ['/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/zipped/', \
#            '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/zipped/', \
#            '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/zipped/', \
#            '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/zipped/', \
#            '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/zipped/', \
#            '/fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/zipped/' ]
# 
# dest_dirs= ['/ftp/waqs-bsh/running_weeklymean/', \
#            '/ftp/waqs-bsh/monthlymean/', \
#            '/ftp/waqs-bsh/daily_IPF/',\
#            '/ftp/waqs-bsh/daily_FUB/',\
#            '/ftp/waqs-bsh/daily/',\
#            '/ftp/waqs-bsh/SST/' ]
#===============================================================================

for dir_index in range(4):
    # we now call the zipping script with the directory index:
    zip_call = zipping_script + ' ' + str(dir_index)
    system(zip_call)
    bas_sync_call = rsync_header_string + src_dirs[dir_index] + '*_bas_* uwe@bcftp:' + dest_dirs[dir_index] + 'BalticSea/'
    print(bas_sync_call)
    system(bas_sync_call)
    nos_sync_call = rsync_header_string + src_dirs[dir_index] + '*_nos_* uwe@bcftp:' + dest_dirs[dir_index] + 'NorthSea/'
    print(nos_sync_call)
    system(nos_sync_call)

dir_index = 4
# For MC daily-merged we have differing names:
zip_call = zipping_script + ' ' + str(dir_index)
system(zip_call)
sync_daily_mc_bas_prods_call =  rsync_header_string + src_dirs[dir_index] + '*_BALTIC_* uwe@bcftp:' + dest_dirs[dir_index] + 'BalticSea/'
print(sync_daily_mc_bas_prods_call)
system(sync_daily_mc_bas_prods_call)
sync_daily_mc_nos_prods_call =  rsync_header_string + src_dirs[dir_index] + '*_NSEA_* uwe@bcftp:' + dest_dirs[dir_index] + 'NorthSea/'
print(sync_daily_mc_nos_prods_call)
system(sync_daily_mc_nos_prods_call)

dir_index = 5
# For SST we have also differing names: 
zip_call = zipping_script + ' ' + str(dir_index)
system(zip_call)
sync_weekly_bas_sst_prods_call = rsync_header_string + src_dirs[dir_index] + '*_baltic_sea_sst_aatsr_* uwe@bcftp:' + dest_dirs[dir_index] + 'BalticSea/'
print(sync_weekly_bas_sst_prods_call)
system(sync_weekly_bas_sst_prods_call)
sync_weekly_nos_sst_prods_call = rsync_header_string + src_dirs[dir_index] + '*_north_sea_sst_aatsr_* uwe@bcftp:' + dest_dirs[dir_index] + 'NorthSea/'
print(sync_weekly_nos_sst_prods_call)
system(sync_weekly_bas_sst_prods_call)

print("\n***********************************************************")
print(" Script \'zip_and_put_products_on_ftp_for_bsh.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("***********************************************************\n")

# EOF