#!/usr/bin/env python
__author__ = 'uwe'

from sys import argv, exit
from os import listdir
from os.path import exists

from nasa.modis.seadas_processing.conf.paths import modisL1A_LACBasePath
from utils.utilities import getDOY, ensureTrailingSlash


def printUsage():
    print("Usage: ", argv[0], "<date>, <print_missing_files>")
    print("where date is a string representing the date to process,")
    print("e.g. 20120607 for June 7, 2012")
    print("and print_missing_files a boolean value (0, or 1)")
    print("specifying whether a list of missing files should be printed.")
    exit(1)

if len(argv) != 3:
    printUsage()

back_date = argv[1]
if len(back_date)!=8:
    print("****************************")
    print("* date parameter malformed *")
    print("****************************")
    printUsage()

if argv[2] == '0':
    print_missing = False
elif argv[2] == '1':
    print_missing = True
else:
    printUsage()

_year  = back_date[:4]
_month = back_date[4:6]
_day   = back_date[6:]
_doy   = getDOY(_year, _month, _day)
DOY = str(_doy).zfill(3)

inputDir = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL1A_LACBasePath  + _year) + _month) + _day)
#print("Processing date " + back_date + " (DOY = " + DOY + ") in " + inputDir + ".")
if exists(inputDir):
    inputList = listdir(inputDir)
else:
    print("-")
    exit(1)
#exit_on_empty_list(inputList)
# print(inputList)

num_missing = 0
for h in range(0,24):
    _hour = str(h).zfill(2)
    for m in range(0, 60, 5):
        _minute = str(m).zfill(2)
        filename = 'A' + _year + DOY + _hour + _minute + '00.L1A_LAC.bz2'
        if filename not in inputList:
            num_missing += 1
            if print_missing:
                print(str(num_missing) + ": " + filename + ' is missing.')

print(back_date + " (DOY=" + DOY + ") Total missing files: " + str(num_missing))
