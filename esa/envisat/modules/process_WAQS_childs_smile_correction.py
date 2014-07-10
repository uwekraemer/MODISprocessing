#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: process_WAQS_childs_smile_correction.py

from os import system, listdir, remove, makedirs
from os.path import exists
from sys import exit
from time import localtime, strftime

print "\n*************************************************************"
print " Script \'process_WAQS_childs_smile_correction.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "*************************************************************\n"

def ensurePathExists(_path):
    if not exists(_path):
        makedirs(_path)

# Verzeichnisse
srcDir = '/fs14/EOservices/InputPool/MERIS/RR/waqs_child_temp/'
destDir = srcDir + 'smile_corrected/'
ensurePathExists(destDir)

# tool config
smile_corr_home   = '/home/uwe/tools/smile_corr/'
smile_corr_script = smile_corr_home + 'meris-smile.sh'
smile_corr_conf   = smile_corr_home + 'smile_corr_request.xml'

request_skeleton_1 =  '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n<RequestList>\n'
request_skeleton_1 += '    <Request type=\"SMILE_CORRECTION\">\n'
request_skeleton_1 += '        <Parameter name=\"output_format\" value=\"BEAM-DIMAP\" />\n'
request_skeleton_1 += '        <Parameter name=\"include_all\" value=\"true\" />\n'
request_skeleton_1 += '        <Parameter name=\"bands\" value=\"radiance_1,radiance_2,radiance_3,radiance_4,radiance_5,radiance_6,radiance_7,radiance_8,radiance_9,radiance_10,radiance_11,radiance_12,radiance_13,radiance_14,radiance_15\" />\n'
request_skeleton_1 += '        <Parameter name=\"log_prefix\" value=\"smile_corr\" />\n'
request_skeleton_1 += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
input_opener       =  '        <InputProduct file=\"'
input_delimiter    = '\" />\n'
output_opener      =  '        <OutputProduct file=\"'
output_delimiter   = '\" format=\"BEAM-DIMAP\" />\n'
request_closer     = '    </Request>\n</RequestList>\n'

# Inputliste holen
src_list = listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 oder Level2 sind:
for a in range(list_size):
    for item in src_list:
        if not item.startswith('MER') or item.startswith('MER_RR__0') or item.startswith('MER_RR__2') or item.endswith('.dim'):
            print "Removing " + item + " from list."
            src_list.remove(item)

list_size = len(src_list)
if not list_size:
    print "Nothing to do here. Now quitting."
    exit(1)

src_list.sort()

# Jetzt geht's los:
for meris_file in src_list:    
    # MER_RR__1PNPDE20051126_053458_000011252042_00463_19555_0425.N1
    # 0         1         2         3         4         5         6
    # 01234567890123456789012345678901234567890123456789012345678901   

    input_filename = srcDir + meris_file
    output_filename= destDir + meris_file[0:len(meris_file)-2] + 'dim'
    if exists(output_filename):
        print "Output product exists already. Continuing..."
        continue
    
    request = request_skeleton_1 + input_opener + input_filename + input_delimiter + output_opener + output_filename + output_delimiter + request_closer

    # Requestfile soll noch nicht existieren:
    if exists(smile_corr_conf):
        remove(smile_corr_conf)
    
    # Erst jetzt wird es erzeugt:
    requestfile = open(smile_corr_conf, 'a')
    requestfile.write(request)
    requestfile.close()

    smile_corr_command = smile_corr_script + " " + smile_corr_conf
    print smile_corr_command
    print "Processing file " + meris_file + " ..."
    system(smile_corr_command)

print "\n************************************************************"
print " Script \'process_WAQS_childs_smile_correction.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "************************************************************\n"

# EOF

