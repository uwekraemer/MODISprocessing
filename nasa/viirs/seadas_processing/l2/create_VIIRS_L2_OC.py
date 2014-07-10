__author__ = 'uwe'

from glob import glob
from sys import argv, exit
from os import chdir, makedirs, system
from os.path import exists, basename
from shutil import rmtree
from utils.utilities import getDOY, ensurePathExists, ensureTrailingSlash, exit_on_empty_list, bzip2DecompressFile
from nasa.viirs.seadas_processing.conf.paths import viirsL1A_BasePath, viirsL2_BasePath, seadasBinDir, seadasScriptsDir
from nasa.viirs.seadas_processing.conf.params import l2gen_io_params, l2gen_suite_params, l2gen_l2_params, l2gen_anc_params

def printUsage():
    print 'Usage: create_MODIS_L2_OC.py date'
    print 'where date is a string representing the date to process,'
    print 'e.g. 20120507 for May 7, 2012.'


argc = len(argv)
if argc < 2:
    printUsage()
    exit(1)

_date  = str(argv[1])
_year  = _date[:4]
_month = _date[4:6]
_day   = _date[6:]
_doy   = getDOY(_year, _month, _day)

viirsL1_Path = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(viirsL1A_BasePath + _year) + _month) + _day)
viirsL2_Path = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(viirsL2_BasePath  + _year) + _month) + _day)
if not exists(viirsL2_Path):
    makedirs(viirsL2_Path)

try:
    srcPathList=glob(viirsL1_Path + 'V' + _year + str(_doy) + '*tar.bz2')
except OSError:
    print("Cannot open ", viirsL1_Path + "! Now exiting...")
    exit(1)
else:
    exit_on_empty_list(srcPathList)

srcList=[basename(item) for item in srcPathList]
srcList.sort()
del srcPathList

# Now processing can start...

l2genBinary  = seadasBinDir + 'l2gen'
getancScript = seadasScriptsDir + 'getanc.py'

print l2genBinary, "Exists="+str(exists(l2genBinary)), getancScript, "Exists="+str(exists(getancScript))

def process_VIIRS_L2_OC(viirsL1_ProductArchive, forceReprocess):
    print("Processing", viirsL1_ProductArchive, "...")
    viirsL2_Product = viirsL1_ProductArchive[:22].replace('L1A_NPP', 'L2_NPP')  # V2014159100026.L2_NPP
    viirsL2_ProductPath = viirsL2_Path + viirsL2_Product
    if exists(viirsL2_ProductPath):
        if not forceReprocess:
            print("Output L2 product exists already. Continuing...")
            return True
    chdir(viirsL1_Path)
    tempPath = viirsL1_Path + ensureTrailingSlash('temp')
    if exists(tempPath):
        rmtree(tempPath)
    ensurePathExists(tempPath)
    untarCommand = "tar -C '" + tempPath + "' -xjf " + viirsL1_ProductArchive
    system(untarCommand)

    viirsL1File = glob(tempPath + 'SVM01_npp_d' + _date + '*_obpg_ops.h5')[0]   # SVM01_npp_d20140608_t1000270_e1001511_b13535_obpg_ops.h5
    viirsGEOFile = viirsL1File.replace('SVM01', 'GMTCO')                        # GMTCO_npp_d20140608_t1000270_e1001511_b13535_obpg_ops.h5
    system("python " + getancScript + " " + viirsL1File)
    viirsAncFile = viirsL1_Path + basename(viirsL1File) + '.anc'                # SVM01_npp_d20140608_t1000270_e1001511_b13535_obpg_ops.h5.anc
    with open(viirsAncFile, 'r') as anc:
        ancillary_info = anc.readlines()
    print(viirsL1File, viirsGEOFile, viirsL2_ProductPath)

    par_file_path = viirsL2_ProductPath + '.par'
    with open(par_file_path, 'w') as par_file:
        par_file.write(l2gen_io_params)
        par_file.write('ifile=' + viirsL1File + '\n')
        par_file.write('geofile=' + viirsGEOFile + '\n')
        par_file.write('ofile=' + viirsL2_ProductPath+'\n\n')
        par_file.write(l2gen_suite_params + '\n')
        par_file.write(l2gen_l2_params + '\n')
        par_file.write(l2gen_anc_params)
        par_file.writelines(ancillary_info)

    processing_call = l2genBinary + ' par=' + par_file_path
    system(processing_call)

    if exists(viirsL2_ProductPath):
        rmtree(tempPath)
        return True    # success
    else:
        return False

for productArchive in srcList:
    retVal = process_VIIRS_L2_OC(productArchive, forceReprocess=False)
    # exit(1)