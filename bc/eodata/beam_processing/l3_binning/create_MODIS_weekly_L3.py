#!/usr/bin/env python3
__author__ = 'uwe'

from os.path import exists
from os import makedirs, system
from sys import argv
from datetime import date
from glob import glob

from utils.utilities import getBackDate, ensureTrailingSlash, exit_on_empty_list
from nasa.modis.seadas_processing.conf.paths import modisL2_TSMBasePath
from bc.eodata.beam_processing.conf.paths import beam500HomeDir as beamHomeDir, modisWeeklyBasePath


def printUsage():
    print("Usage: ", argv[0], "<date> <region> <params>")
    print("where <date> is a string representing the newest date to be included,")
    print("e.g. 20140114 for January 14, 2014.")
    print("and <region> one of 'NorthSea' and 'BalticSea'")
    print("and <params> a parameter describing the product contents,")
    print("i.e. 'wac' for water constituents, and 'sst' for SST.")

if len(argv) != 4:
    printUsage()
    exit(1)

back_date = argv[1]
if len(back_date)!=8:
    print("****************************")
    print("* date parameter malformed *")
    print("****************************")
    printUsage()
    exit(1)

region = argv[2]
if not region in ['NorthSea', 'BalticSea']:
    print("****************************")
    print("* region parameter unknown *")
    print("****************************")
    printUsage()
    exit(1)

parameters = argv[3]
if not parameters in ['wac', 'sst']:
    print("******************************")
    print("* processing parameter wrong *")
    print("******************************")
    printUsage()
    exit(1)

if region=='NorthSea':
    regiondestID= '_nos_'
    from bc.eodata.beam_processing.conf.params import nos_polygon as polygon
elif region=='BalticSea':
    regiondestID= '_bas_'
    from bc.eodata.beam_processing.conf.params import bas_polygon as polygon

if parameters=='wac':
    from bc.eodata.beam_processing.conf.paths import wac_graph_file as graph_file
elif parameters=='sst':
    from bc.eodata.beam_processing.conf.paths import sst_graph_file as graph_file


beamBinDir  = beamHomeDir + 'bin/'
gptProcessor = beamBinDir + 'gpt.sh'

num_days_in_l3 = 7
_year  = int(back_date[:4])
_month = int(back_date[4:6])
_day   = int(back_date[6:])
proc_datetime = date(_year, _month, _day)
delta_days = (date.today() - proc_datetime).days
day_list = [getBackDate(day) for day in range(delta_days, delta_days + num_days_in_l3)]

srcList = []
for item in day_list:
    modisL2_TSMPath = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL2_TSMBasePath  + str(item.year))
                                                              + str(item.month).zfill(2)) + str(item.day).zfill(2))
    srcList += glob(modisL2_TSMPath+'A' + str(item.year) + '*.L2_TSM.dim')

exit_on_empty_list(srcList)
srcList.sort()
srcList = ",".join(srcList)

modisWeeklyPath  = ensureTrailingSlash(ensureTrailingSlash(modisWeeklyBasePath + str(_year)) + str(_month).zfill(2))
dateRangeString = str(day_list[6].year) + str(day_list[6].month).zfill(2) + str(day_list[6].day).zfill(2) + '_' + \
                  str(day_list[0].year) + str(day_list[0].month).zfill(2) + str(day_list[0].day).zfill(2)

outputProductPath = modisWeeklyPath + dateRangeString + regiondestID + parameters + '_bc_mod_1200.dim'

for _path in [modisWeeklyPath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)

processing_call = gptProcessor + ' -e ' + graph_file + ' -PinputProducts=' + srcList + ' -PregionPolygon=' + polygon + ' -PoutputProduct=' + outputProductPath
print("Executing call: ", processing_call, "...")
system(processing_call)

#EOF