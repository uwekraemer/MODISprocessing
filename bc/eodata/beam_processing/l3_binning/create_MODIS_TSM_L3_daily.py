#!/usr/bin/env python
__author__ = 'uwe'

from nasa.modis.seadas_processing.conf.params import l3_grid_cell_size, _site
if _site == 'NorthSea':
    from nasa.modis.seadas_processing.conf.params import west_lon_large_nsea_l3 as lon_min, east_lon_large_nsea_l3 as lon_max
    from nasa.modis.seadas_processing.conf.params import south_lat_large_nsea_l3 as lat_min, north_lat_large_nsea_l3 as lat_max
elif _site == 'BalticSea':
    from nasa.modis.seadas_processing.conf.params import west_lon_large_bsea_l3 as lon_min, east_lon_large_bsea_l3 as lon_max
    from nasa.modis.seadas_processing.conf.params import south_lat_large_bsea_l3 as lat_min, north_lat_large_bsea_l3 as lat_max

from nasa.modis.seadas_processing.shared.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list
from nasa.modis.seadas_processing.conf.paths import modisL2_TSMBasePath, modisL3_TSMBasePath, beam_410BinDir as beamBinDir, l3binningDir
from os import listdir, makedirs, remove, system
from os.path import exists
from sys import argv, exit
from shutil import rmtree

print(_site, lat_min, lat_max, lon_min, lon_max)
# exit(1)

def printUsage():
    print("Usage: ", argv[0], "<date>")
    print("where date is a string representing the date to process,")
    print("e.g. 20120607 for June 7, 2012.")

if len(argv) != 2:
    printUsage()
    exit(1)

back_date = argv[1]
if len(back_date)!=8:
    print("****************************")
    print("* date parameter malformed *")
    print("****************************")
    printUsage()
    exit(1)

_year  = back_date[:4]
_month = back_date[4:6]
_day   = back_date[6:]
_doy   = getDOY(_year, _month, _day)
DOY = str(_doy).zfill(3)


print("Processing date " + back_date + " (DOY = " + DOY + ").")

modisL2_TSMPath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL2_TSMBasePath  + _year) + _month) + _day)
modisL3_TSMPath  = ensureTrailingSlash(ensureTrailingSlash(modisL3_TSMBasePath  + _year) + _month)

print(modisL2_TSMPath, modisL3_TSMPath)

for _path in [modisL3_TSMPath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)

try:
    srcList = listdir(modisL2_TSMPath)
except OSError:
    print("Cannot open ", modisL2_TSMPath+ "! Now exiting...")
    exit(1)
else:
    listSize = exit_on_empty_list(srcList)
    print(listSize)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        if not item.startswith('A' + _year + DOY) or not item.endswith('.L2_TSM.dim'):
            srcList.remove(item)

listSize = exit_on_empty_list(srcList)
srcList.sort()

# outputProductPath = modisL3_TSMPath + 'cb_' + _site + '_' + back_date + '_eo_bc_lat_lon.dim'
outputProductPath = modisL3_TSMPath + _site + '_' + back_date + '_eo_bc_lat_lon.dim'

l3binningScript = beamBinDir + 'binning.command'
l3binningDatabase = l3binningDir + 'l3_large_' + str(_year) + DOY + '.bindb'
if exists(l3binningDatabase):
    rmtree(l3binningDatabase)
l3binningConf = l3binningDir + 'l3_large_' + str(_year) + DOY + '.conf'

xml_version_tag = '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n'
request_list_opener = '<RequestList>\n'
request_init_block  = '    <Request type=\"BINNING\">\n'
request_init_block += '        <Parameter name=\"process_type\" value=\"init\" />\n'
request_init_block += '        <Parameter name=\"database\" value=\"'+l3binningDatabase+'\" />\n'
request_init_block += '        <Parameter name=\"lat_min\" value=\"' + str(lat_min) +'\" />\n'
request_init_block += '        <Parameter name=\"lat_max\" value=\"' + str(lat_max) +'\" />\n'
request_init_block += '        <Parameter name=\"lon_min\" value=\"' + str(lon_min)  +'\" />\n'
request_init_block += '        <Parameter name=\"lon_max\" value=\"' + str(lon_max)  +'\" />\n'
request_init_block += '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_init_block += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_init_block += '        <Parameter name=\"resampling_type\" value=\"binning\" />\n'
request_init_block += '        <Parameter name=\"grid_cell_size\" value=\"' + str(l3_grid_cell_size) + '\" />\n'
request_init_block += '        <Parameter name=\"band_name.0\" value=\"chlor_a\" />\n'
request_init_block += '        <Parameter name=\"bitmask.0\" value=\"fneq(chlor_a,-32767.0) AND NOT l2_flags.CHLFAIL'
request_init_block += ' AND NOT l2_flags.CHLWARN AND NOT l2_flags.PRODWARN\" />\n'
request_init_block += '        <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n'
request_init_block += '        <Parameter name=\"weight_coefficient.0\" value=\"1.0\" />\n'
request_init_block += '        <Parameter name=\"band_name.1\" value=\"Kd_490\" />\n'
request_init_block += '        <Parameter name=\"bitmask.1\" value=\"fneq(Kd_490, -6.553399834447191)\" />\n'
request_init_block += '        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n'
request_init_block += '        <Parameter name=\"weight_coefficient.1\" value=\"1.0\" />\n'
request_init_block += '        <Parameter name=\"band_name.2\" value=\"tsm_678\" />\n'
request_init_block += '        <Parameter name=\"bitmask.2\" value=\"tsm_678 &gt; 0.0\" />\n'
request_init_block += '        <Parameter name=\"binning_algorithm.2\" value=\"Arithmetic Mean\" />\n'
request_init_block += '        <Parameter name=\"weight_coefficient.2\" value=\"1.0\" />\n'
request_init_block += '        <Parameter name=\"band_name.3\" value=\"KdPAR\" />\n'
request_init_block += '        <Parameter name=\"bitmask.3\" value=\"((fneq(Kd_412_lee,-6.553399834447191) &amp;&amp;'
request_init_block += ' fneq(Kd_443_lee,-6.553399834447191) &amp;&amp; fneq(Kd_469_lee,-6.553399834447191) &amp;&amp;'
request_init_block += ' fneq(Kd_488_lee,-6.553399834447191) &amp;&amp; fneq(Kd_531_lee,-6.553399834447191) &amp;&amp;'
request_init_block += ' fneq(Kd_547_lee,-6.553399834447191) &amp;&amp; fneq(Kd_555_lee,-6.553399834447191) &amp;&amp;'
request_init_block += ' fneq(Kd_645_lee,-6.553399834447191) &amp;&amp; fneq(Kd_667_lee,-6.553399834447191) &amp;&amp;'
request_init_block += ' fneq(Kd_678_lee,-6.553399834447191)))&amp;&amp; !nan(KdPAR)\" />\n'
request_init_block += '        <Parameter name=\"binning_algorithm.3\" value=\"Arithmetic Mean\" />\n'
request_init_block += '        <Parameter name=\"weight_coefficient.3\" value=\"1.0\" />\n'
request_init_block += '    </Request>\n'

request_update_block  = '    <Request type=\"BINNING\">\n'
request_update_block += '        <Parameter name=\"process_type\" value=\"update\" />\n'
request_update_block += '        <Parameter name=\"database\" value=\"'+l3binningDatabase+'\" />\n'
request_update_block += '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_update_block += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'

input_prefix          = '        <InputProduct file=\"'
input_delimiter = '\" />\n'

block_close = '    </Request>'
request_finalize_block  = '    <Request type=\"BINNING\">\n'
request_finalize_block += '        <Parameter name=\"process_type\" value=\"finalize\" />\n'
request_finalize_block += '        <Parameter name=\"database\" value=\"'+l3binningDatabase+'\" />\n'
request_finalize_block += '        <Parameter name=\"delete_db\" value=\"true\" />\n'
request_finalize_block += '        <Parameter name=\"log_prefix\" value=\"l3\" />\n'
request_finalize_block += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
request_finalize_block += '        <Parameter name=\"tailoring\" value=\"false\" />\n'
request_finalize_block += '        <OutputProduct file=\"'
request_closer = '\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n'

# Assembling request XML:
request  = xml_version_tag
request += request_list_opener
request += request_init_block
request += request_update_block

for item in srcList:
    request += input_prefix
    request += modisL2_TSMPath + item
    request += input_delimiter

request += block_close
request += request_finalize_block
request += outputProductPath
request += request_closer

if exists(l3binningConf):
    remove(l3binningConf)

# Jetzt wird das Requestfile erzeugt:

requestfile = open(l3binningConf, 'a')
requestfile.write(request)
requestfile.close()

# Binning starten
l3binningCommand = l3binningScript + " " + l3binningConf
print(l3binningCommand)
print("Processing L3...")
system(l3binningCommand)
