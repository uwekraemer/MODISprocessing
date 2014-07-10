#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: launch_wew_WAQS_childs_processing.py

# FUB WeW L2 Processing for Meris child products
# The processing steps are:
# 1) Smile correction of the WAQS childs:         process_WAQS_childs_smile_correction.py
# 2) Processing with the FUB WeW water processor  process_wew_smile_corrected_WAQS_childs.py
#
# In step 1), the smile corrected products are written
# to a dedicated directory. Step 2) picks them from there for
# the L2 step. The input products are discarded thereafter.
# For detailed information, consider the two scripts.


from os import system
from sys import exit
from time import localtime, strftime

print("\n**********************************************************")
print(" Script \'launch_wew_WAQS_childs_processing.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("**********************************************************\n")

modules_home = '/home/uwe/cronjobs/modules/'

smile_corr_script = modules_home + 'process_WAQS_childs_smile_correction.py'
system(smile_corr_script)

water_proc_script = modules_home + 'process_wew_smile_corrected_WAQS_childs.py'
system(water_proc_script)

print("\n*********************************************************")
print(" Script \'launch_wew_WAQS_childs_processing.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("*********************************************************\n")

# EOF