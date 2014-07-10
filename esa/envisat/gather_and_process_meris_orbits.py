#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: gather_and_process_meris_orbits.py

# Processing chain for Meris Orbits

from os import system
from sys import argv, exit
from time import localtime, strftime

def printUsage():
    print "Usage: gather_and_process_meris_orbits.py \'source\'"
    print "where \'source\' includes:"
    print "\"ES\", \"KS\" or \"DDS\"\n"

try:
    argc=len(argv)
    if argc == 1:          # the program was called without parameters
        print "Source specifier is missing!"
        printUsage()
        exit(1)
    else:
        product_source = argv[1]                   # we have also received parameters
        if product_source in ["ES", "KS", "DDS"]:
            print "\nProcessing MERIS orbits from " + product_source + "..."
        else:               # incorrect parameter
            print "Wrong source specifier!"
            printUsage()
            exit(1)
except:
    print "Error in parameters. Now exiting..."
    exit(1)    

print "\n********************************************************"
print " Script \'gather_and_process_meris_orbits.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "********************************************************\n"

launchers_home = '/home/uwe/cronjobs/'
modules_home = launchers_home + 'modules/'

# /home/uwe/cronjobs/modules/fetch_meris_orbits_from_RA.py 'KS'
if product_source in ["ES", "KS"]:
    fetch_script = 'python ' + modules_home + 'fetch_meris_orbits_from_RA.py ' + product_source
else:
    fetch_script = 'python ' + modules_home + 'fetch_DDS_orbits_from_bcftp.py '
system(fetch_script)

# /home/uwe/cronjobs/modules/sync_with_DDS.py 'KS'
sync_script = 'python ' + modules_home + 'sync_with_DDS.py ' + product_source
system(sync_script)

# /home/uwe/cronjobs/modules/make_WAQS_MERIS_childs.py
childgen_script = 'python ' + modules_home + 'make_WAQS_MERIS_childs.py'
system(childgen_script)

# /home/uwe/cronjobs/modules/make_WAQS_MERIS_childs_Estonia.py
estonia_childgen_script = 'python ' + modules_home + 'make_WAQS_MERIS_childs_Estonia.py'
system(estonia_childgen_script)

# /home/uwe/cronjobs/modules/convert_estonia_L1b_to_DIMAP.py
estonia_convert_script = 'python ' + modules_home + 'convert_estonia_L1b_to_DIMAP.py'
system(estonia_convert_script)

# /home/uwe/cronjobs/modules/make_CalVal_MERIS_childs.py
calval_childgen_script = 'python ' + modules_home + 'make_CalVal_MERIS_childs.py'
system(calval_childgen_script)

# put smile corr here
smile_corr_script = 'python ' + modules_home + 'process_WAQS_childs_smile_correction.py'
system(smile_corr_script)

# put c2r here
c2r_script = 'python ' + modules_home + 'process_case2R_WAQS_childs.py'
system(c2r_script)

# 20080501: replaces modules/process_wew_WAQS_childs.py:
# script launches smile corr + wew water processing + removes smile corrected input products afterwards!
# /home/uwe/cronjobs/launch_wew_WAQS_childs_processing.py
#wew_l2_script = launchers_home + 'launch_wew_WAQS_childs_processing.py'
#system(wew_l2_script)
# launcher script performs smile corr again, although it has been run before!
# not necessary, so, just run the wew script:
wew_water_proc_script = 'python ' + modules_home + 'process_wew_smile_corrected_WAQS_childs.py'
system(wew_water_proc_script)

# /home/uwe/cronjobs/modules/process_IPF_WAQS_childs.py
ipf_child_script = 'python ' + modules_home + 'process_IPF_WAQS_childs.py'
system(ipf_child_script)

# /home/uwe/cronjobs/modules/merge_daily_IPF_L3_mosaicking.py 'BalticSea'
ipf_daily_bas_merging_script = 'python ' + modules_home + 'merge_daily_IPF_L3_mosaicking.py \'BalticSea\' 1'
system(ipf_daily_bas_merging_script)

# /home/uwe/cronjobs/modules/merge_daily_IPF_L3_mosaicking.py 'NorthSea'
ipf_daily_nos_merging_script = 'python ' + modules_home + 'merge_daily_IPF_L3_mosaicking.py \'NorthSea\' 1'
system(ipf_daily_nos_merging_script)

# /home/uwe/cronjobs/modules/merge_daily_IPF_L3_mosaicking.py 'UK'
#ipf_daily_uk_merging_script = modules_home + 'merge_daily_IPF_L3_mosaicking.py \'UK\' 1'
#system(ipf_daily_uk_merging_script)

# /home/uwe/cronjobs/modules/merge_daily_IPF_L3_mosaicking.py 'Estonia'
ipf_daily_est_merging_script = 'python ' + modules_home + 'merge_daily_IPF_L3_mosaicking.py \'Estonia\' 1'
system(ipf_daily_est_merging_script)

# /home/uwe/cronjobs/modules/register_WAQS_childs.py
register_child_script = 'python ' + modules_home + 'register_WAQS_childs.py'
system(register_child_script)

calval_register_script = 'python ' + modules_home + "register_CalVal_childs.py MERIS RR"
system(calval_register_script)

# /home/uwe/cronjobs/modules/register_DDS_orbits.py
register_orbits_script = 'python ' + modules_home + 'register_DDS_orbits.py'
system(register_orbits_script)

print "\n********************************************************"
print " Script \'gather_and_process_meris_orbits.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "********************************************************\n"

# EOF