#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_products_on_ftp_for_bsh.py

# Put MC daily-merged and weekly NorthSeaproducts on ftp

import os
from time import localtime, strftime

print "\n****************************************************"
print " Script \'put_products_on_ftp_for_bsh.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************************\n"

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*_bas_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/running_weeklymean/BalticSea/
sync_weekly_mc_bas_prods_call = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*_bas_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/running_weeklymean/BalticSea/'
os.system(sync_weekly_mc_bas_prods_call)
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*_nos_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/running_weeklymean/NorthSea/
sync_weekly_mc_nos_prods_call =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/*_nos_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/running_weeklymean/NorthSea/'
os.system(sync_weekly_mc_nos_prods_call)


# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*_BALTIC_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily/BalticSea/
sync_daily_mc_bas_prods_call =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*_BALTIC_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_MC/BalticSea/'
os.system(sync_daily_mc_bas_prods_call)
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*_NSEA_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily/NorthSea/
sync_daily_mc_nos_prods_call =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/*_NSEA_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_MC/NorthSea/'
os.system(sync_daily_mc_nos_prods_call)


# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/200608*_nos_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_IPF/NorthSea/
sync_daily_ipf_nos_prods_call =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/*_nos_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_IPF/NorthSea/'
os.system(sync_daily_ipf_nos_prods_call)
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/200608*_bas_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_IPF/BalticSea/
sync_daily_ipf_bas_prods_call =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/*_bas_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_IPF/BalticSea/'
os.system(sync_daily_ipf_bas_prods_call)


# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/*_bas_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_FUB/BalticSea/
sync_daily_wew_bas_prods_call =  'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/*_bas_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_FUB/BalticSea/'
os.system(sync_daily_wew_bas_prods_call)
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/*_nos_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_FUB/NorthSea/ 
sync_daily_wew_nos_prods_call = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/*_nos_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/daily_FUB/NorthSea/'
os.system(sync_daily_wew_nos_prods_call)

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/*_sea_sst_aatsr_* uwe@bcftp:/ftp/waqs-bsh/SST/weekly/
sync_weekly_sst_prods_call = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/*_sea_sst_aatsr_* uwe@bcftp:/ftp/waqs-bsh/SST/weekly/'
os.system(sync_weekly_sst_prods_call)


print "\n****************************************************"
print " Script \'put_products_on_ftp_for_bsh.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************************\n"

# EOF
