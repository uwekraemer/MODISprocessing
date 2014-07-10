#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: put_products_on_ftp_for_baw.py
# created: 20120330, 13:45

from os import system
from time import localtime, strftime

print "\n****************************************************"
print " Script \'put_products_on_ftp_for_baw.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************************\n"

sync_daily_tsm_images_call = "rsync -avuPH /fs14/EOservices/OutputPool/MERIS/RR/WAQS-caseR/preview-images/NorthSea/tsm/ uwe@10.1.0.2:/data/bcserver8/ftp/waqs-baw/MERIS-RR/daily_tsm_png/"
system(sync_daily_tsm_images_call)

print "\n***************************************************"
print " Script \'put_products_on_ftp_for_baw.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "***************************************************\n"

# EOF