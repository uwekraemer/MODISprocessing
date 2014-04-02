__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import chdir, getcwd, makedirs, system
from datetime import date, timedelta

def printUsage():
    print('Usage: get_MODISA_LAC.py backDay')
    print('where backDay is a integer number specifying the number of days ')
    print('before today. This script will download the data for that particular day.')


argc = len(argv)
if argc < 2:
    printUsage()
    exit(1)

try:
    backDay = int(argv[1])
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

print(_year, _month, _day, DOY)

def ensureTrailingSlash(path):
    if not path.endswith('/'):
        return path + '/'
    else:
        return path


#L2_LAC_products = ['L2_LAC_OC.', 'L2_LAC_SST.', 'L2_LAC_SST4.']
MODIS_A_products = ['L1A_LAC', 'L2_LAC_OC', 'L2_LAC_SST']#, 'L2_LAC_SST4']
MODIS_A_localBaseDir = '/fs14/EOservices/InputPool/MODISA/'
baseURL = 'http://oceandata.sci.gsfc.nasa.gov/MODISA/'


for productType in MODIS_A_products:
    destURL = baseURL + ensureTrailingSlash(productType[:2]) + ensureTrailingSlash(str(_year)) + ensureTrailingSlash(str(DOY))
    L2_LAC_localInputDir = MODIS_A_localBaseDir + ensureTrailingSlash(productType) \
                           + ensureTrailingSlash(str(_year)) \
                           + ensureTrailingSlash(str(_month).zfill(2)) \
                           + ensureTrailingSlash(str(_day).zfill(2))
    if not exists(L2_LAC_localInputDir):
        makedirs(L2_LAC_localInputDir)
    chdir(L2_LAC_localInputDir)
    print(productType, L2_LAC_localInputDir)
    wgetCommand = "wget -nc -S -O - " + destURL + " |grep "+ productType + ".bz2|wget -N --wait=0.5 --random-wait --force-html -i -"
    print("Downloading ", productType, " products to ", getcwd(), ":")
    print(wgetCommand)
    system(wgetCommand)


# wget -nc -S -O - http://oceandata.sci.gsfc.nasa.gov/MODISA/L2/2012/131/ |grep OC|wget -N --wait=0.5 --random-wait --force-html -i -