__author__ = 'carole'

from sys import argv
from os import listdir, makedirs, remove, system
from os.path import basename, exists
from bc.eodata.beam_processing.conf.demarine_conf import gptProcessor, DeMarine_fine_grid_graph_file, DeMarine_coarse_grid_graph_file
from bc.eodata.beam_processing.conf.paths import imageMagickComposite, landMaskFile
from nasa.modis.seadas_processing.shared.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list
from bc.eodata.beam_processing.conf.demarine_paths import modisL3_TSMBasePath, modisL3_TSMDemarine_CoarseGrid_Path, modisL3_TSMDemarine_FineGrid_Path
from nasa.modis.seadas_processing.conf.params import _site

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
print("Processing date " + back_date + " (DOY = " + str(_doy)+ ").")

modisL3_TSMPath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL3_TSMBasePath  + _year) + _month) + _day)

modisL3_DeM_FinePath  = ensureTrailingSlash(modisL3_TSMDemarine_FineGrid_Path  + _year)
modisL3_DeM_CoarsePath  = ensureTrailingSlash(modisL3_TSMDemarine_CoarseGrid_Path  + _year)


for _path in [modisL3_DeM_FinePath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)

for _path in [modisL3_DeM_CoarsePath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)
try:
    srcList = listdir(modisL3_TSMPath)
except OSError:
    print("Cannot open ", modisL3_TSMPath+ "! Now exiting...")
    exit(1)
else:
    listSize = exit_on_empty_list(srcList)
    print(listSize)

# Liste bereinigen:
for a in range(listSize):
    for item in srcList:
        if not item.startswith('MODISA_DeM_' + back_date) or not item.endswith('.dim'):
            srcList.remove(item)
        # if not item.startswith('NorthSea_' + back_date) or not item.endswith('.dim'):
        #     srcList.remove(item)

listSize = exit_on_empty_list(srcList)
srcList.sort()

# outputProductPath = modisL3_ECOHAMPath + 'cb_ns_' + back_date + '_eo_bc_lat_lon_ecoham.dim'
outputProductFinePath = modisL3_DeM_FinePath + 'reprojected_DeMarine_' + back_date + '_fine_grid.dim'
outputProductCoarsePath = modisL3_DeM_CoarsePath + 'reprojected_DeMarine_' + back_date + '_coarse_grid.dim'

print(srcList, outputProductFinePath, outputProductCoarsePath)

for item in srcList:
    reproj_fine_processingCall = gptProcessor + ' ' + DeMarine_fine_grid_graph_file + ' -Ssource=' + modisL3_TSMPath + item + ' -Pfile=' + outputProductFinePath
    system(reproj_fine_processingCall)
    reproj_coarse_processingCall = gptProcessor + ' ' + DeMarine_coarse_grid_graph_file + ' -Ssource=' + modisL3_TSMPath + item + ' -Pfile=' + outputProductCoarsePath
    system(reproj_coarse_processingCall)
    # pconv_call = pconvProcessor + ' -f png -b 1 -c ' + cobios_chl_palette + ' -o ' + modisL3_UTM_QLPath + ' ' + outputProductPath
    # system(pconv_call)
    # oldPngFileName = modisL3_UTM_QLPath + basename(outputProductPath).replace('.dim', '.png')
    # newPngFileName = modisL3_UTM_QLPath + basename(outputProductPath).replace('cb_ns_', 'cb_ns_chl_').replace('.dim', '.png')
    # imCompositeCommand = imageMagickComposite + ' -gravity center ' + landMaskFile + ' ' + oldPngFileName + ' ' + newPngFileName
    # system(imCompositeCommand)
    # remove(oldPngFileName)      # not needed anymore

