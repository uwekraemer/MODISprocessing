#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_products_on_ftp_for_uniold.py

# Put MC daily-merged and weekly NorthSeaproducts on ftp

import os
from time import localtime, strftime

print("\n****************************************************")
print(" Script \'put_products_on_ftp_for_uniold.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("****************************************************\n")

# rsync -avuPH --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*200609*_NSEA_* uwe@10.1.0.2:/ftp/waqs-uniold/WQ/daily/
sync_daily_prods_call  = 'rsync -avuPH --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*_NSEA_* uwe@10.1.0.2:/ftp/waqs-uniold/WQ/daily/'
os.system(sync_daily_prods_call)

# rsync -avuPH --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*200609*_nos_* uwe@10.1.0.2:/ftp/waqs-uniold/WQ/weekly/
sync_weekly_prods_call = 'rsync -avuPH --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*_nos_* uwe@10.1.0.2:/ftp/waqs-uniold/WQ/weekly/'
os.system(sync_weekly_prods_call)


# rsync -avuPH --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/*_north_sea_aatsr_* uwe@10.1.0.2:/ftp/waqs-uniold/SST/weekly/
sync_weekly_sst_prods_call = 'rsync -avuPH --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/*_north_sea_sst_aatsr_* uwe@10.1.0.2:/ftp/waqs-uniold/SST/weekly/'
os.system(sync_weekly_sst_prods_call)

#rsync -avuPH --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/daily-merged/*_sst_aatsr_1.2km.* uwe@10.1.0.2:/ftp/waqs-uniold/SST/daily/
sync_daily_sst_prods_call = 'rsync -avuPH --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/daily-merged/*_sst_aatsr_1.2km.* uwe@10.1.0.2:/ftp/waqs-uniold/SST/daily/'
os.system(sync_daily_sst_prods_call)

print("\n****************************************************")
print(" Script \'put_products_on_ftp_for_uniold.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("****************************************************\n")

# EOF
