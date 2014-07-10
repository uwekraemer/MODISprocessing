#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_products_on_ftp_for_estonia.py

# Put MC daily-merged and weekly Estonia products on ftp

import os
from time import localtime, strftime

print("\n****************************************************")
print(" Script \'put_products_on_ftp_for_estonia.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("****************************************************\n")

# MC products...
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/*_est_* uwe@10.1.0.2:/ftp/waqs-to/monthly_MC/
sync_command_monthly_mc = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/*_est_* uwe@10.1.0.2:/ftp/waqs-to/monthly_MC/'
os.system(sync_command_monthly_mc)

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*_est_* uwe@10.1.0.2:/ftp/waqs-to/weekly_MC/
sync_command_weekly_mc =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*_est_* uwe@10.1.0.2:/ftp/waqs-to/weekly_MC/'
os.system(sync_command_weekly_mc)

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*_ESTONIA_* uwe@10.1.0.2:/ftp/waqs-to/daily_MC/
sync_command_daily_mc =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*_ESTONIA_* uwe@10.1.0.2:/ftp/waqs-to/daily_MC/'
os.system(sync_command_daily_mc)

# IPF products...
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/weekly/*_est_* uwe@10.1.0.2:/ftp/waqs-to/weekly_IPF/
sync_command_weekly_ipf =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/weekly/*_est_* uwe@10.1.0.2:/ftp/waqs-to/weekly_IPF/'
os.system(sync_command_weekly_ipf)

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/*_est_* uwe@10.1.0.2:/ftp/waqs-to/daily_IPF/
sync_command_daily_ipf =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/*_est_* uwe@10.1.0.2:/ftp/waqs-to/daily_IPF/'
os.system(sync_command_daily_ipf)

# FUB products...
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/weekly/*_est_* uwe@10.1.0.2:/ftp/waqs-to/weekly_FUB/
sync_command_weekly_fub =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/Level3/*_estonia_* uwe@10.1.0.2:/ftp/waqs-to/weekly_FUB/'
os.system(sync_command_weekly_fub)

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/*_est_* uwe@10.1.0.2:/ftp/waqs-to/daily_FUB/ 
sync_command_daily_fub = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/*_est_* uwe@10.1.0.2:/ftp/waqs-to/daily_FUB/'
os.system(sync_command_daily_fub)

# L1b products...
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/L1b-Estonia/MER_RR__1* uwe@10.1.0.2:/ftp/waqs-to/daily_L1b/
sync_command_daily_l1b =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/L1b-Estonia/MER_RR__1* uwe@10.1.0.2:/ftp/waqs-to/daily_L1b/'
os.system(sync_command_daily_l1b)

print("\n****************************************************")
print(" Script \'put_products_on_ftp_for_estonia.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("****************************************************\n")

# EOF