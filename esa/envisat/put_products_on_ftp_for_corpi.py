#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_products_on_ftp_for_bsh.py

# zip MC products that are made for the CORPI and put them on ftp

from os import system
from sys import exit
from time import localtime, strftime
from configparser import ConfigParser

print("\n******************************************************")
print(" Script \'put_products_on_ftp_for_corpi.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("******************************************************\n")

modules_home = '/home/uwe/cronjobs/modules/'
zipping_script = modules_home + 'zip_dimap_files.py'

sync_ipf_daily_images_call = "rsync -avuPH /fs14/EOservices/OutputPool/quicklooks/WAQS-IPF/daily-RGB/hires/ uwe@10.1.0.2:/ftp/waqs-corpi/MERIS-RR/daily_IPF/quicklooks/"
system(sync_ipf_daily_images_call)

sync_mc_daily_prods_call = "rsync -avuPH /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*_BALTIC_* uwe@10.1.0.2:/ftp/waqs-corpi/MERIS-RR/daily_MC"
system(sync_mc_daily_prods_call)

sync_mc_daily_images_call = "rsync -avuPH /fs14/EOservices/OutputPool/quicklooks/WAQS-MC/daily/ uwe@10.1.0.2:/ftp/waqs-corpi/MERIS-RR/daily_MC/quicklooks/"
system(sync_mc_daily_images_call)

sync_mc_weekly_prods_call = "rsync -avuPH /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*_bas_wac_acr_* uwe@10.1.0.2:/ftp/waqs-corpi/MERIS-RR/running_weeklymean"
system(sync_mc_weekly_prods_call)

sync_mc_weekly_images_call = "rsync -avuPH /fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/ uwe@10.1.0.2:/ftp/waqs-corpi/MERIS-RR/running_weeklymean/quicklooks/"
system(sync_mc_weekly_images_call)

sync_sst_daily_prods_call = "rsync -avuPH /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/daily-merged/*_baltic_sea_sst_aatsr_* uwe@10.1.0.2:/ftp/waqs-corpi/SST/daily_merged"
system(sync_sst_daily_prods_call)

sync_sst_weekly_prods_call = "rsync -avuPH /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/zipped/*_baltic_sea_sst_aatsr_* uwe@10.1.0.2:/ftp/waqs-corpi/SST/running_weeklymean"
system(sync_sst_weekly_prods_call)


print("\n***************************************************")
print(" Script \'put_products_on_ftp_for_bsh.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("***************************************************\n")

# EOF