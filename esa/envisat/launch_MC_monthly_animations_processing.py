#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_MC_monthly_animations_processing.py

from os import system
from time import localtime, strftime

print("\n****************************************************************")
print(" Script \'launch_MC_monthly_animations_processing.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("****************************************************************\n")

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


modules_home = '/home/uwe/cronjobs/modules/'
processing_command = modules_home + 'process_MC_WAQS_L3_animations.py '  + last_month_date

print(processing_command)
system(processing_command)

# rsync -avupogtP --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/animations/ uwe@bcweb:/var/www/images/WAQS-MC/weekly/animations/
rsync_animations_command = 'rsync -avupogtP --rsh=\"ssh -l uwe\"  /fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/animations/ uwe@bcweb:/var/www/images/WAQS-MC/weekly/animations/'
system(rsync_animations_command)
# rsync -avupogtP --rsh="ssh -l uwe" /fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/animations/html/ uwe@bcweb:/var/www/waqss/wac_mc/weekly/animations/html/
rsync_html_command = 'rsync -avupogtP --rsh=\"ssh -l uwe\"  /fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/animations/html/ uwe@bcweb:/var/www/waqss/wac_mc/weekly/animations/html/'
system(rsync_html_command)


print("\n***************************************************************")
print(" Script \'launch_MC_monthly_animations_processing.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("***************************************************************\n")

#EOF
