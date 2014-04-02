__author__ = 'uwe'

from os import remove, system
from os.path import exists
from glob import glob
from sys import argv, exit


print("\n********************************************************")
print(" Script \'merge_daily_modis_OC_L3_binning.py\' at work... ")
print("********************************************************\n")


def printUsage():
    print('Usage: merge_daily_modis_OC_L3_binning.py region date')
    print('where region includes:')
    print('\"NorthSea\"  or  \"BalticSea\" or  \"Estonia\"')
    print('and date is a string specifying the day to be processed.')
    print("e.g. 20120510. It has to start with \'20\' and must be exactly 8 characters long.")

def ensureTrailingSlash(path):
    if not path.endswith('/'):
        return path + '/'
    else:
        return path

argc=len(argv)

if argc < 3:          # the program was called incorrectly
    print("\nToo few parameters passed!")
    printUsage()
    exit(1)
else:                   # we have also received parameters
    if argv[1] in ["NorthSea", "BalticSea", "Estonia"]:
            # do something
        print("Processing " +str(argv[1]) + " request...")
    else:               # incorrect parameter
        print("Wrong region specifier!")
        printUsage()
        exit(1)


try:
    thedate = str(argv[2])
except TypeError:
    print("date parameter must be of type string!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    exit(1)

if not len(thedate)==8 or not thedate.startswith('20'):
    print("\ndate parameter unusable.")
    printUsage()
    exit(1)

_year  = thedate[:4]
_month = thedate[4:6]
_day   = thedate[6:8]


l3binningHome   = '/home/uwe/tools/beam-4.10/bin/'
l3binningScript = l3binningHome + 'binning.sh'
l3confHome = '/home/uwe/tools/l3binning/'

baseDir = "/fs14/EOservices/InputPool/MODIS/L2_LAC_OC/"
srcDir = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(baseDir + _year) + _month) + _day)
print(srcDir)


inputfiles = glob(srcDir+"*.L2_LAC_OC.bz2")
inputfiles.sort()
print(inputfiles)

grid_cell_size = '2.0'

if argv[1]=='NorthSea':
    regionSrcID = 'NSEA'
    regiondestID= '_nos_'
    lat_min = '49.0'
    lat_max = '63.0'
    lon_min = '-5.0'
    lon_max = '13.0'
    l3binningConf   = l3confHome + 'l3binningConfMcModisNorthsea.xml'
    l3binningDatabase = '/fs14/EOservices/InputPool/MODIS/L2_LAC_OC/.l3binning/l3_database_mc_modis_northsea.bindb'
elif argv[1]=='Estonia':
    regionSrcID = 'BALTIC'
    regiondestID= '_est_'
    lat_min = '57.058884'
    lat_max = '60.57032'
    lon_min = '21.702216'
    lon_max = '30.225435'
    l3binningConf   = l3confHome + 'l3binningConfMcModisEstonia.xml'
    l3binningDatabase = '/fs14/EOservices/InputPool/MODIS/L2_LAC_OC/.l3binning/l3_database_mc_modis_estonia.bindb'
else:
    regionSrcID = 'BALTIC'
    regiondestID= '_bas_'
    lat_min = '53.0'
    lat_max = '66.0'
    lon_min = '9.0'
    lon_max = '31.0'
    l3binningConf   = l3confHome + 'l3binningConfMcModisBalticSea.xml'
    l3binningDatabase = '/fs14/EOservices/InputPool/MODIS/L2_LAC_OC/.l3binning/l3_database_mc_modis_balticsea.bindb'


outputDir = '/fs14/EOservices/OutputPool/MODIS/L2_LAC_OC/daily_merged/'
output_filename= outputDir + thedate + regiondestID + "wac_mod_2000.dim"

print(output_filename)
#exit(1)

# konstante xml-bausteine fuer request
request_init_block  =  "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
request_init_block  += "<RequestList>\n"
request_init_block  += "    <Request type=\"BINNING\">\n"
request_init_block  += "        <Parameter name=\"process_type\" value=\"init\" />\n"
request_init_block  += "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_init_block  += "        <Parameter name=\"lat_min\" value=\""+lat_min+"\" />\n"
request_init_block  += "        <Parameter name=\"lat_max\" value=\""+lat_max+"\" />\n"
request_init_block  += "        <Parameter name=\"lon_min\" value=\""+lon_min+"\" />\n"
request_init_block  += "        <Parameter name=\"lon_max\" value=\""+lon_max+"\" />\n"
request_init_block  += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_init_block  += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_init_block  += "        <Parameter name=\"resampling_type\" value=\"binning\" />\n"
request_init_block  += "        <Parameter name=\"grid_cell_size\" value=\""+grid_cell_size+"\" />\n"
request_init_block  += "        <Parameter name=\"band_name.0\" value=\"chlor_a\" />\n"
request_init_block  += "        <Parameter name=\"bitmask.0\" value=\"fneq(chlor_a,-32767.0)\" />\n"
request_init_block  += "        <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n"
request_init_block  += "        <Parameter name=\"weight_coefficient.0\" value=\"1.0\" />\n"
request_init_block  += "        <Parameter name=\"band_name.1\" value=\"Kd_490\" />\n"
request_init_block  += "        <Parameter name=\"bitmask.1\" value=\"Kd_490.raw != -32767.0 AND fneq(Kd_490,-6.553399834447191)\" />\n"
request_init_block  += "        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n"
request_init_block  += "        <Parameter name=\"weight_coefficient.1\" value=\"1.0\" />\n"
request_init_block  += "        <Parameter name=\"band_name.2\" value=\"pic\" />\n"
request_init_block  += "        <Parameter name=\"bitmask.2\" value=\"pic.raw != -32767.0 AND fneq( pic,-5.340022187283466E-4)\" />\n"
request_init_block  += "        <Parameter name=\"binning_algorithm.2\" value=\"Arithmetic Mean\" />\n"
request_init_block  += "        <Parameter name=\"weight_coefficient.2\" value=\"1.0\" />\n"
request_init_block  += "        <Parameter name=\"band_name.3\" value=\"poc\" />\n"
request_init_block  += "        <Parameter name=\"bitmask.3\" value=\"poc.raw != -32767.0 AND fneq(poc,-153.4001)\" />\n"
request_init_block  += "        <Parameter name=\"binning_algorithm.3\" value=\"Arithmetic Mean\" />\n"
request_init_block  += "        <Parameter name=\"weight_coefficient.3\" value=\"1.0\" />\n"
request_init_block  += "        <Parameter name=\"band_name.4\" value=\"cdom_index\" />\n"
request_init_block  += "        <Parameter name=\"bitmask.4\" value=\"cdom_index.raw != -32767.0 AND fneq(cdom_index,-0.15339973907975946)\" />\n"
request_init_block  += "        <Parameter name=\"binning_algorithm.4\" value=\"Arithmetic Mean\" />\n"
request_init_block  += "        <Parameter name=\"weight_coefficient.4\" value=\"1.0\" />\n"
request_init_block  += "    </Request>\n"

request_update_block    = "    <Request type=\"BINNING\">\n"
request_update_block   += "        <Parameter name=\"process_type\" value=\"update\" />\n"
request_update_block   += "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_update_block   += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_update_block   += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"

input_prefix =            "        <InputProduct file=\""
input_delimiter =         "\" />\n"
block_close=              "    </Request>\n"

request_finalize_block  = "    <Request type=\"BINNING\">\n"
request_finalize_block += "       <Parameter name=\"process_type\" value=\"finalize\" />\n"
request_finalize_block += "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
request_finalize_block += "        <Parameter name=\"delete_db\" value=\"true\" />\n"
request_finalize_block += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
request_finalize_block += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
request_finalize_block += "        <Parameter name=\"tailoring\" value=\"false\" />\n"
request_finalize_block += "        <OutputProduct file=\""

request_closer =         "\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n"


if exists(l3binningConf):
    remove(l3binningConf)

requestfile = open(l3binningConf, 'a')
requestfile.write(request_init_block)
requestfile.write(request_update_block)

entry=[]
for line in range(len(inputfiles)):
    entry.append(input_prefix + inputfiles[line] + input_delimiter)
    requestfile.write(entry[line])

requestfile.write(block_close)
requestfile.write(request_finalize_block+output_filename)
requestfile.write(request_closer)
requestfile.close()

l3binningCommand = l3binningScript + " " + l3binningConf
print(l3binningCommand)
print("Processing L3...")
system(l3binningCommand)

print("\n*******************************************************")
print(" Script \'merge_daily_modis_OC_L3_binning.py\' finished. ")
print("*******************************************************\n")

# EOF