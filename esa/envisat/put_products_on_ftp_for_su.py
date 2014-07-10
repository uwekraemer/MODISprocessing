#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_products_on_ftp_for_bsh.py

# zip MC products that are made for the BSH and put them on ftp

from os import system
from sys import exit
from time import localtime, strftime
from ConfigParser import ConfigParser

print "\n***************************************************"
print " Script \'put_products_on_ftp_for_su.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "***************************************************\n"

modules_home = '/home/uwe/cronjobs/modules/'
#zipping_script = modules_home + 'zip_dimap_files.py'

sync_ipf_daily_images_call = "rsync -avuPH /fs14/EOservices/OutputPool/quicklooks/WAQS-IPF/daily-RGB/hires/*bas*.jpg uwe@10.1.0.2:/ftp/waqs-su/MERIS-RR/daily_IPF/quicklooks/"
system(sync_ipf_daily_images_call)

sync_sst_daily_prods_call = "rsync -avuPH /fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/daily-merged/*_baltic_sea_sst_aatsr_* uwe@10.1.0.2:/ftp/waqs-su/SST/"
system(sync_sst_daily_prods_call)

print "\n**************************************************"
print " Script \'put_products_on_ftp_for_su.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "**************************************************\n"

# EOF