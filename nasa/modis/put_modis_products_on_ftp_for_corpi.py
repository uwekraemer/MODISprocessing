#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_products_on_ftp_for_bsh.py

# zip MC products that are made for the CORPI and put them on ftp

from os import system
from sys import exit
from time import localtime, strftime
from configparser import ConfigParser

print("\n************************************************************")
print(" Script \'put_modis_products_on_ftp_for_corpi.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("************************************************************\n")

sync_mc_daily_prods_call = "rsync -avuPH /fs14/EOservices/OutputPool/MODIS/WAQS-MC/daily-merged/zipped/*_BALTIC_* uwe@10.1.0.2:/ftp/waqs-corpi/MODIS/daily_MC"
system(sync_mc_daily_prods_call)

sync_mc_weekly_prods_call = "rsync -avuPH /fs14/EOservices/OutputPool/MODIS/WAQS-MC/weekly/zipped/*_bas_wac_mod_* uwe@10.1.0.2:/ftp/waqs-corpi/MODIS/running_weeklymean"
system(sync_mc_weekly_prods_call)

sync_mc_weekly_images_call = "rsync -avuPH /fs14/EOservices/OutputPool/quicklooks/WAQS-MC-MODIS/weekly/ uwe@10.1.0.2:/ftp/waqs-corpi/MODIS/running_weeklymean/quicklooks/"
system(sync_mc_weekly_images_call)

print("\n***********************************************************")
print(" Script \'put_modis_products_on_ftp_for_corpi.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("***********************************************************\n")

# EOF