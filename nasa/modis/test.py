__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import chdir, getcwd, makedirs, system

from utils.utilities import getDOY


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

satellite_code = 'A'

print(_year, _month, _day, _doy)
# exit(1)

def ensureTrailingSlash(path):
    if not path.endswith('/'):
        return path + '/'
    else:
        return path


MODIS_products = ['L1A_LAC']
MODIS_localBaseDir = '/fs14/EOservices/InputPool/MODIS' + ensureTrailingSlash(satellite_code)
baseURL = 'http://oceandata.sci.gsfc.nasa.gov/MODIS'+ ensureTrailingSlash(satellite_code)


for productType in MODIS_products:
    destURL = baseURL + ensureTrailingSlash(productType[:2]) + ensureTrailingSlash(str(_year)) + ensureTrailingSlash(str(_doy).zfill(3))
    L2_LAC_localInputDir = MODIS_localBaseDir + ensureTrailingSlash(productType) \
                           + ensureTrailingSlash(str(_year)) \
                           + ensureTrailingSlash(str(_month).zfill(2)) \
                           + ensureTrailingSlash(str(_day).zfill(2))
    if not exists(L2_LAC_localInputDir):
        makedirs(L2_LAC_localInputDir)
    chdir(L2_LAC_localInputDir)
    print(productType, L2_LAC_localInputDir)
    wgetCommand = "wget --timeout 20 -t 500 -nc -S -O - " + destURL + " |grep "+ productType + ".bz2|wget -N -c --timeout 20 -t 500 --wait=0.5 --random-wait --force-html -i -"
    print("Downloading ", productType, " products to ", getcwd(), ":")
    print(wgetCommand)
    system(wgetCommand)


# wget -nc -S -O - http://oceandata.sci.gsfc.nasa.gov/MODISA/L2/2012/131/ |grep OC|wget -N --wait=0.5 --random-wait --force-html -i -
