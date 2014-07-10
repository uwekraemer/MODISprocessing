#!/usr/bin/env python
# file: process_case2R_WAQS_childs.py

import os
import os.path
import sys
import time

def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

thetime   = time.localtime()
year_str  = str(thetime[0]) + "/"

# Verzeichnisse
baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
srcDir  = baseDir + 'waqs_child_temp/smile_corrected/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-caseR/Level2/'
ensurePathExists(destDir)

# tool config
c2rHome   = '/home/uwe/tools/case2R/'
c2rPropertyFile = c2rHome+ 'auxdata/1.3.2/default-parameters-20080515-BAW.txt'
c2rConf   = c2rHome + 'c2rConf.xml'

beam46_home = '/home/uwe/tools/beam-4.6/'
beam46_bindir = beam46_home + 'bin/'
c2rScript = beam46_bindir + 'c2r.sh'

# Neues Requestfile:
request_header =  '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n<RequestList>\n'
request_header += '    <Request type=\"MERISC2R\">\n'
request_header += '        <Parameter name=\"output_format\" value=\"BEAM-DIMAP\" />\n'
request_header += '        <Parameter name=\"log_prefix\" value=\"merisc2r\" />\n'
request_header += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_header += '        <Parameter name="property_file" value="' + c2rPropertyFile + '" />\n'
request_header += '        <InputProduct file=\"'
input_delimiter  =                              '\" />\n'
output_beginning =  '        <OutputProduct file=\"'
output_delimiter =  '\" format=\"BEAM-DIMAP\" />\n'
request_closer   =  '    </Request>\n</RequestList>\n'

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte im DIMAP-Format sind:
for a in range(list_size):
    for item in src_list:
        if not item.startswith('MER') or not item.endswith('.dim'):
            src_list.remove(item)

if not len(src_list):
    print("Nothing to do. Exiting...")
    sys.exit(1)

src_list.sort()
print("Input products: ", src_list)

# Jetzt geht's los:
for meris_file in src_list:

    # MER_RR__1PNPDE20051126_053458_000011252042_00463_19555_0425.N1
    # 0         1         2         3         4         5         6
    # 01234567890123456789012345678901234567890123456789012345678901

    #year  = meris_file[14:18]
    #month = meris_file[18:20]
    #day   = meris_file[20:22]

    acquisition_time = meris_file[14:29]
    duration = meris_file[30:42]
    orbit = meris_file[49:54]

    input_filename = srcDir + meris_file
    output_filename= destDir + 'MER_RR_C2R_' + acquisition_time + "_" + duration + '_' + orbit + ".dim"
    request = request_header + input_filename + input_delimiter + output_beginning + output_filename + output_delimiter + request_closer

    # Requestfile soll noch nicht existieren, bzw. altes loeschen:
    if os.path.exists(c2rConf):
        os.remove(c2rConf)

    # Erst jetzt wird es erzeugt:
    requestfile = open(c2rConf, 'a')
    requestfile.write(request)
    requestfile.close()

    c2rCommand = c2rScript + " " + c2rConf
    print(c2rCommand)
    print("Processing file " + meris_file + " ...")
    os.system(c2rCommand)

#!/usr/bin/env python
# file: process_case2R_WAQS_childs.py

import os
import os.path
import sys
import time

thetime   = time.localtime()
year_str  = str(thetime[0]) + "/"

# Verzeichnisse
baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
srcDir  = baseDir + 'waqs_child_temp/smile_corrected/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-caseR/Level2/'

# tool config
c2rHome   = '/home/uwe/tools/case2R/'
c2rPropertyFile = c2rHome+ 'auxdata/1.3.2/default-parameters-20080515-BAW.txt'
c2rConf   = c2rHome + 'c2rConf.xml'

beam46_home = '/home/uwe/tools/beam-4.6/'
beam46_bindir = beam46_home + 'bin/'
c2rScript = beam46_bindir + 'c2r.sh'

# Neues Requestfile:
request_header =  '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n<RequestList>\n'
request_header += '    <Request type=\"MERISC2R\">\n'
request_header += '        <Parameter name=\"output_format\" value=\"BEAM-DIMAP\" />\n'
request_header += '        <Parameter name=\"log_prefix\" value=\"merisc2r\" />\n'
request_header += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_header += '        <Parameter name="property_file" value="' + c2rPropertyFile + '" />\n'
request_header += '        <InputProduct file=\"'
input_delimiter  =                              '\" />\n'
output_beginning =  '        <OutputProduct file=\"'
output_delimiter =  '\" format=\"BEAM-DIMAP\" />\n'
request_closer   =  '    </Request>\n</RequestList>\n'

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-Produkte im DIMAP-Format sind:
for a in range(list_size):
    for item in src_list:
        if not item.startswith('MER') or not item.endswith('.dim'):
            src_list.remove(item)

# Jetzt geht's los:
for meris_file in src_list:

    # MER_RR__1PNPDE20051126_053458_000011252042_00463_19555_0425.N1
    # 0         1         2         3         4         5         6
    # 01234567890123456789012345678901234567890123456789012345678901

    #year  = meris_file[14:18]
    #month = meris_file[18:20]
    #day   = meris_file[20:22]

    acquisition_time = meris_file[14:29]
    duration = meris_file[30:42]
    orbit = meris_file[49:54]

    input_filename = srcDir + meris_file
    output_filename= destDir + 'MER_RR_C2R_' + acquisition_time + "_" + duration + '_' + orbit + ".dim"
    if os.path.exists(output_filename):
        print("Output product exists already. Continuing...")
        continue
    
    request = request_header + input_filename + input_delimiter + output_beginning + output_filename + output_delimiter + request_closer

    # Requestfile soll noch nicht existieren, bzw. altes loeschen:
    if os.path.exists(c2rConf):
        os.remove(c2rConf)

    # Erst jetzt wird es erzeugt:
    requestfile = open(c2rConf, 'a')
    requestfile.write(request)
    requestfile.close()

    c2rCommand = c2rScript + " " + c2rConf
    print(c2rCommand)
    print("Processing file " + meris_file + " ...")
    os.system(c2rCommand)

