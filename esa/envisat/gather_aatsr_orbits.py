#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: gather_aatsr_orbits.py

# Gather AATSR orbits from Rolling Archives of Kiruna and ESRIN

import os
from time import localtime, strftime

print "\n********************************************"
print " Script \'gather_aatsr_orbits.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "********************************************\n"

modules_home = '/home/uwe/cronjobs/modules/'
#modules_home = '/uwe/cronjobs/modules/'

fetch_script = modules_home + 'fetch_aatsr_orbits_from_RA.py'

es_nr_call = fetch_script + " ES NR"
os.system(es_nr_call)

ks_nr_call = fetch_script + " KS NR"
os.system(ks_nr_call)

es_toa_call = fetch_script + " ES TOA"
os.system(es_toa_call)

ks_toa_call = fetch_script + " KS TOA"
os.system(ks_toa_call)

print "\n********************************************"
print " Script \'gather_aatsr_orbits.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "********************************************\n"

# EOF
