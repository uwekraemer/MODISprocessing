#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: fetch_DDS_orbits_from_bcftp.py

# _download der Meris RR-Daten vom BC FTP Server

from ftplib import FTP
from os.path import basename, exists
from os import system, listdir
from sys import exit
from time import localtime

try:
    ftp = FTP('10.1.0.2','uwe','2fast4u')    #login
except:
    print "unable to connect to the ftp-server"
    exit(1)

try:
    meris_files = ftp.nlst('MERISdata')                #Liste der files erstellen
except:
    print "directory does not exist on the ftp-server"
    exit(1)

print meris_files

print "\n****************************************************"
print " Script \'fetch_DDS_orbits_from_bcftp.py\' at work... "
print "****************************************************\n"

initialPath = '/fs14/EOservices/InputPool/MERIS/RR/'
basepath = initialPath + 'DDS_temp/'
dbDir    = initialPath + 'productsDB/'

thetime= localtime()
_year  = str(thetime[0])
_month = str(thetime[1])
_day   = str(thetime[2])
_hour  = str(thetime[3])
_minute= str(thetime[4])
_second= str(thetime[5])

if thetime[1] < 10:
    _month = "0"+ _month

if thetime[2] < 10:
    _day = "0"+ _day

datestring = _year + _month + _day + " " + _hour + ":" + _minute + ":" + _second

logfilename = basepath+"ftp_get.log"

try:
    logfile = open(logfilename, 'a')
    logfile.write('\n'+datestring+'\n')
except:
    print "unable to open the log file"
    exit(1)


for ftp_meris_file in meris_files:
    _download = 0
    meris_file = basename(ftp_meris_file)
    real_meris_file = basepath + meris_file

    year       = meris_file[14:18]
    month      = meris_file[18:20]
    day        = meris_file[20:22]
    type       = meris_file[:9]
    uniqueName = meris_file[:54]

    if   type == 'MER_RR__0':
        _download = 0
        _delete   = 1
    elif type == 'MER_RR__1':
        _download = 1
        _delete   = 0
    elif type == 'MER_RR__2':
        _download = 1
        _delete   = 0
    elif type == 'MER_RRC_2':
        _download = 0
        _delete   = 1
    elif type == 'MER_RRV_2':
        _download = 0
        _delete   = 1
    elif type == 'MER_RR__B':
        _download = 0
        _delete   = 1
    elif type == 'MER_FRS_1':   # it is important to let FRS products on the ftp server for the FRS processing server
        _download = 0
        _delete   = 0
    elif type == 'MER_FRS_2':
        _download = 0
        _delete   = 0

    dbPath = dbDir + year + "/" + month + "/" + day + "/"

    if exists(dbPath):
        dbPathList = listdir(dbPath)
        if _download == 1:
            for dbPathEntry in dbPathList:
                stamp = basename(dbPathEntry)[:54]
                if stamp == uniqueName:
                    print uniqueName + " has been found in the productsDB. No download necessary."
                    _download *= 0
                    _delete = 1
    else:
        _download *= 1    # new date; don't change _download flag (redundant, just for readability)

    uncompress = False

    if _download:
        if meris_file.startswith('MER_'):
            if meris_file.endswith('.gz'):
                uncompress_type="gunzip -f"      # force extraction, even if file exists
                uncompress = True
            elif meris_file.endswith('.zip'):
                uncompress_type="unzip -o"       # overwrite if file exists
                uncompress = True
            print "Downloading " + meris_file + " ..." + '\n'
            ftp.retrbinary('RETR '+ftp_meris_file, open(real_meris_file, 'wb').write)
            print meris_file + " stored successfully. Deleting remote file." + '\n'
            logfile.write(meris_file+'\n')
            ftp.delete(ftp_meris_file)

            if uncompress:
                uncompressCommand = uncompress_type + " " + real_meris_file
                print "uncompressing " + real_meris_file + ":"
                print uncompressCommand
                system(uncompressCommand)
    else:
        if not _delete:
            # do nothing, it might be MER_FRS !
            print meris_file + " will be kept. Doing nothing." + '\n'
            continue
        else:                        # don't delete partial files; they start with the date!
            print meris_file + " will be deleted."
            print "Deleting "+ meris_file + " on ftp server..."  # we also delete now the duplicated ones!
            ftp.delete(ftp_meris_file)

ftp.quit()
logfile.close()

print "\n****************************************************"
print " Script \'fetch_DDS_orbits_from_bcftp.py\' finished.  "
print "****************************************************\n"

#EOF
