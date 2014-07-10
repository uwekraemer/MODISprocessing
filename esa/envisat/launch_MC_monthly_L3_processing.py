#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_MC_monthly_L3_processing.py

import os
from sys import exit
from time import localtime, strftime

print "\n********************************************************"
print " Script \'launch_MC_monthly_L3_processing.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "********************************************************\n"

# /home/uwe/cronjobs/process_MC_monthly_L3_binning.py region month

today = localtime()

if today[1] > 1 and today[1] <= 12:
    last_month = today[1]-1
    if last_month < 10:
        month = "0" + str(last_month)
    else:
        month = str(last_month)
    last_month_date = (str(today[0]) + month)
elif today[1] == 1:
    last_month_date = (str(today[0]-1), '12')

launch_command_nos = '/home/uwe/cronjobs/modules/process_MC_monthly_L3_binning.py \'NorthSea\' '  + last_month_date
launch_command_bas = '/home/uwe/cronjobs/modules/process_MC_monthly_L3_binning.py \'BalticSea\' ' + last_month_date
launch_command_est = '/home/uwe/cronjobs/modules/process_MC_monthly_L3_binning.py \'Estonia\' ' + last_month_date

print launch_command_nos
os.system(launch_command_nos)
print launch_command_bas
os.system(launch_command_bas)
print launch_command_est
os.system(launch_command_est)

# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/*_nos_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/monthlymean/NorthSea/
#sync_command_nos = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/*_nos_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/monthlymean/NorthSea/'
#os.system(sync_command_nos)
# rsync -avupogtP --delete --delete-after --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/*_bas_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/monthlymean/BalticSea/
#sync_command_bas = 'rsync -avupogtP --delete --delete-after --rsh=\"ssh -l uwe\" /fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/*_bas_* uwe@bcftp:/ftp/waqs-bsh/MERIS-RR/monthlymean/BalticSea/'
#os.system(sync_command_bas)

print "\n********************************************************"
print " Script \'launch_MC_monthly_L3_processing.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "********************************************************\n"

#EOF
