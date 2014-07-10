#!/usr/bin/env python
# -*- coding: latin-1 -*
from configparser import ConfigParser
from sys import stdout
from os.path import exists
from os import remove 

baseDir = '/home/uwe/tools/'
configDir  = baseDir + 'config/'

configFilePath = configDir + 'zipDirConfig.ini'
if exists(configFilePath):
    remove(configFilePath)
configFile     = open(configFilePath,'a')

config = ConfigParser()

# set a number of parameters
config.add_section("ematter")
config.set("ematter", "dirs", 6)

config.add_section("srcDirectories")
config.set("srcDirectories", "srcDir0", "/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/")
config.set("srcDirectories", "srcDir1", "/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/monthly/")
config.set("srcDirectories", "srcDir2", "/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily-merged/")
config.set("srcDirectories", "srcDir3", "/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/daily-merged/")
config.set("srcDirectories", "srcDir4", "/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/")
config.set("srcDirectories", "srcDir5", "/fs14/EOservices/OutputPool/AATSR/NR/WAQS-MC/weekly/")

config.add_section("destDirectories")
config.set("destDirectories", "destDir0", "/ftp/waqs-bsh/MERIS-RR/running_weeklymean/")
config.set("destDirectories", "destDir1", "/ftp/waqs-bsh/MERIS-RR/monthly_MC/")
config.set("destDirectories", "destDir2", "/ftp/waqs-bsh/MERIS-RR/daily_IPF/")
config.set("destDirectories", "destDir3", "/ftp/waqs-bsh/MERIS-RR/daily_FUB/")
config.set("destDirectories", "destDir4", "/ftp/waqs-bsh/MERIS-RR/daily_MC/")
config.set("destDirectories", "destDir5", "/ftp/waqs-bsh/SST/")

# write to file
config.write(configFile)
