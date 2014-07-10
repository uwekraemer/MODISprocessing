__author__ = 'uwe'

from sys import argv, exit
from os.path import exists
from os import chdir, getcwd, makedirs, system
from utils.utilities import getBackDate, getBackDOY, ensureTrailingSlash
from datetime import datetime

# DOY etc like in MODIS

sensor = 'VIIRS'

def printUsage():
    print('Usage: get_VIIRS_products_from_NASA_oceandata.py <procLevel> <backDay>')
    print('where prodLevel is one out of [L1, L2], and')
    print('where backDay is a integer number specifying the number of days ')
    print('before today. This script will download the data for that particular day.')

argc = len(argv)
if argc < 3:
    print("Parameter error.")
    printUsage()
    exit(1)

if argv[1] not in ["L1", "L2"]:
    print("Parameter error.")
    printUsage()
else:
    prodLevel = argv[1]

if prodLevel == "L1":
    prodExtension = "A_NPP.tar.bz2"
    from nasa.viirs.seadas_processing.conf.paths import viirsL1A_BasePath as inputPath
else:
    prodExtension = "_NPP_OC.bz2"
    from nasa.viirs.seadas_processing.conf.paths import viirsL2_BasePath as inputPath

try:
    backDay = int(argv[2])
except TypeError:
    print("backDay parameter must be of integer type.")
    printUsage()
    exit(1)

_now = datetime.now()   # start time of computing

_back_date = getBackDate(backDay)
_year  = str(_back_date.year)
_month = str(_back_date.month)
_day   = str(_back_date.day)
DOY    = str(getBackDOY(backDay=backDay, _year=int(_year)))

inputPath += ensureTrailingSlash(str(_year)) + ensureTrailingSlash(str(_month).zfill(2)) + ensureTrailingSlash(str(_day).zfill(2))
if not exists(inputPath):
    makedirs(inputPath)

chdir(inputPath)

min_acq_time = 8    # we start download for 8 o'clock data
max_acq_time = 15   # stop time of acq in our ROI

time_interval = [str(t).zfill(2) for t in range(min_acq_time, max_acq_time)]

print("Downloading products to: " + getcwd())

def wgetProducts():
    wget_cmd  = "wget -nc -S -O - http://oceandata.sci.gsfc.nasa.gov/" + sensor + "/" + prodLevel + "/" + _year + "/" + DOY
    grep_expr = "|grep V" + _year + DOY + hour + "|grep " + prodLevel + prodExtension
    wget_cmd += grep_expr
    wget_cmd += "|wget -N -c --timeout 20 -t 500 --wait=0.5 --random-wait --force-html -i -"
    print(wget_cmd)
    system(wget_cmd)
    return 0

for hour in time_interval:
    wgetProducts()

_then = datetime.now()   # end time of computing
_diff = _then - _now
_days = _diff.days
_secs = _diff.seconds
_hours= _days*24.
print("Time spent: {0} hours, {1} minutes.".format(_hours, _secs*60.))

# wget -nc -S -O - http://oceandata.sci.gsfc.nasa.gov/VIIRS/L1/2014/130 |grep L1A_NPP.tar.bz2
# |wget -N -c --timeout 20 -t 500 --wait=0.5 --random-wait --force-html -i -
# filenames like: V2014130000404.L1A_NPP.tar.bz2

