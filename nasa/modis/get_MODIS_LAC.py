__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import chdir, getcwd, makedirs, system
from datetime import date, timedelta

def printUsage():
    print('Usage: get_MODIS_LAC.py satellite backDay')
    print('where satellite is one out of [AQUA, TERRA], and')
    print('where backDay is a integer number specifying the number of days ')
    print('before today. This script will download the data for that particular day.')


argc = len(argv)
if argc < 3:
    printUsage()
    exit(1)

satellite_name = argv[1]
if satellite_name not in ['AQUA', 'TERRA']:
    print("satellite unsupported.")
    printUsage()
    exit(1)

satellite_code = satellite_name[:1]

try:
    backDay = int(argv[2])
except TypeError:
    print("backDay parameter must be of integer type.")
    printUsage()
    exit(1)



def getDOY(backDay):
    d0 = date(_year-1, 12, 31)
    d1 = date.today() - timedelta(backDay)
    delta=d1-d0
    return delta.days

def getBackDate(backDay):
    _back_date = date.today() - timedelta(backDay)
    return _back_date

_back_date = getBackDate(backDay)
_year  = _back_date.year
_month = _back_date.month
_day   = _back_date.day
DOY = getDOY(backDay)

#print _year, _month, _day, DOY

def ensureTrailingSlash(path):
    if not path.endswith('/'):
        return path + '/'
    else:
        return path


MODIS_products = ['L1A_LAC']
#MODIS_products = ['L1A_LAC', 'L2_LAC_OC', 'L2_LAC_SST']
MODIS_localBaseDir = '/Volumes/fs14/EOservices/InputPool/MODIS' + ensureTrailingSlash(satellite_code)
baseURL = 'http://oceandata.sci.gsfc.nasa.gov/MODIS'+ ensureTrailingSlash(satellite_code)


for productType in MODIS_products:
    destURL = baseURL + ensureTrailingSlash(productType[:2]) + ensureTrailingSlash(str(_year)) + ensureTrailingSlash(str(DOY).zfill(3))
    L2_LAC_localInputDir = MODIS_localBaseDir + ensureTrailingSlash(productType) \
                           + ensureTrailingSlash(str(_year)) \
                           + ensureTrailingSlash(str(_month).zfill(2)) \
                           + ensureTrailingSlash(str(_day).zfill(2))
    if not exists(L2_LAC_localInputDir):
        makedirs(L2_LAC_localInputDir)
    chdir(L2_LAC_localInputDir)
    print(productType, L2_LAC_localInputDir)
    wgetCommand = "/usr/local/bin/wget -nc -S -O - " + destURL + " |grep "+ productType + ".bz2|wget -N --wait=0.5 --random-wait --force-html -i -"
    print("Downloading ", productType, " products to ", getcwd(), ":")
    print(wgetCommand)
    system(wgetCommand)


# wget -nc -S -O - http://oceandata.sci.gsfc.nasa.gov/MODISA/L2/2012/131/ |grep OC|wget -N --wait=0.5 --random-wait --force-html -i -