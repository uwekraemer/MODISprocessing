#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: fetch_meris_orbits_from_RA.py

# Download der Meris Orbits

from ftplib import FTP
from os.path import basename, exists, getsize
from os import system, listdir, makedirs
from sys import argv, exit
from time import time, localtime

def printUsage():
    print "Usage: fetch_meris_orbits_from_RA.py server"
    print "where server includes:"
    print "\"ES\", or \"KS\"\n"

try:
    argc=len(argv)
    if (argc == 1):          # the program was called without parameters
        print "Archive specifier is missing!"
        printUsage()
        exit(1)
    else:                   # we have also received parameters
        if (argv[1] in ['ES', 'KS']):
            sourceID = argv[1]
            print "\nSynchronising " + sourceID + " products with local archive..."
        else:               # incorrect parameter
            print "Wrong archive specifier!"
            printUsage()
            exit(1)
except:
    print "Error in parameters. Now exiting..."
    exit(1)    

def ensurePathExists(_path):
    if not exists(_path):
        makedirs(_path)


print "\n***************************************************"
print " Script \'fetch_meris_orbits_from_RA.py\' at work... "
print "***************************************************\n"

baseDir ='/fs14/EOservices/InputPool/MERIS/RR/'
dbDir   = '/fs14/EOservices/InputPool/MERIS/RR/productsDB/'

if sourceID =="ES":
    tempDir = baseDir + 'RA_ES_temp/'
    server  = 'oa-es.eo.esa.int'
    user    = 'merusr'
    passwd  = 'mer12sys'
elif sourceID =="KS":
    tempDir = baseDir + 'RA_KS_temp/'
    server  = 'oa-ks.eo.esa.int'
    user    = 'merusr'
    passwd  = 'mer12sys'

ensurePathExists(baseDir)
ensurePathExists(dbDir)
ensurePathExists(tempDir)

try:
    ftp = FTP(server, user, passwd)    #login
except:
    print "unable to connect to the ftp-server"
    exit(1)

try:
    meris_files = ftp.nlst()                #Liste der files erstellen 
except:
    print "directory does not exist on the ftp-server"
    exit(1)

thetime   = localtime()
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

logfilename = tempDir + "ftp_get.log"

try:
    logfile = open(logfilename, 'a')
    logfile.write('\n'+datestring+'\n')
except:
    print "unable to open the log file"
    exit(1)

filecounter=0
downloadedbytes=0
starttime = time()

for ftp_meris_file in meris_files: 
    
    download=0
    
    meris_file = basename(ftp_meris_file)
    
    # MER_RR__2PNPDE20051126_053458_000011252042_00463_19555_0425.N1.gz
    # 0         1         2         3         4         5         6
    # 012345678901234567890123456789012345678901234567890123456789012345   
    
    year=meris_file[14:18]
    month=meris_file[18:20]
    day=meris_file[20:22]
    type =meris_file[4:9]
    uniqueName = meris_file[0:54]
    
    if   (type.find('RR__0')==0):
        download = 0
    elif (type.find('RR__1')==0):
        download = 1
    elif (type.find('RR__2')==0):
        download = 1
    elif (type.find('RRC_2')==0):
        download = 0
    elif (type.find('RRV_2')==0):
        download = 0
    elif (type.find('RR__B')==0):
        download = 0
    elif (type.find('LRC_2')==0):
        download = 0
    elif (type.find('LRV_2')==0):
        download = 0
    
    dbPath = dbDir + year + "/" + month + "/" + day + "/"
    
    if exists(dbPath):
        dbPathList = listdir(dbPath)
        if download == 1:
            for dbPathEntry in dbPathList:
                stamp = basename(dbPathEntry)[0:54]
                if stamp == uniqueName:
                    print uniqueName + " has been found in the productsDB. No download necessary."
                    download *= 0
    else:
        makedirs(dbPath)
        download *= 1    # new date; don't change download flag (redundant, just for readability)
    
    uncompress = False    
    # download flag might have been set to 0 now
    if download == 1: 
        if (meris_file.endswith('.gz')):
            uncompress_type="gunzip -f"      # force extraction, even if file exists
            uncompress = True
        elif (meris_file.endswith('.tgz')):
            uncompress_type="tar -xzf --overwrite"       # overwrite if file exists
            uncompress = True
        elif (meris_file.endswith('.zip')):
            uncompress_type="unzip -o"       # overwrite if file exists
            uncompress = True
        elif (meris_file.endswith('.N1')):
            uncompress_type="none"
        
        dbFile = dbPath + meris_file[0:62]    
        dbCommand="touch " + dbFile
        temp_meris_file = tempDir + meris_file
        
        if uncompress == True:
            uncompressCommand = uncompress_type + " " + temp_meris_file
                
        if not exists(dbFile) and download==1:  # wenn das file noch nicht existiert und es geladen werden soll
            print "Downloading " + meris_file + " ..." + '\n'

           # replaced by expeimental wget
           # ftp.retrbinary('RETR '+ftp_meris_file, open(temp_meris_file, 'wb').write)

            wgetCmd = "wget \"ftp://"+server+"/"+ftp_meris_file+"\" -O \""+temp_meris_file+"\" --timeout 120 -c --user \""+user+"\" --password \""+passwd+"\""
            status = system(wgetCmd)

            if status == 0:
                #system(dbCommand)                     # darf nicht ausgefuehrt werden, weil 'sync_with_DDS.py' die (scheinbar schon vorhandenen) Produkte sonst sofort loescht!!
                filesize = getsize(temp_meris_file)
                if uncompress == True:
                    system(uncompressCommand)
                downloadedbytes=downloadedbytes+filesize
                logfile.write(dbFile+'\n')             # erfolgreich geholtes file, logfile waechst mit
                filecounter += 1
            elif status == 130:
		print "Interupted"
                break
            elif status == 143:
		print "Terminated"
                break
            elif status == 137:
		print "Killed"
                break
            else:
                print "ERROR todo: handle by removing, renaming, etc. so it will try again later"
    else:   # download == 0
        continue

ftp.quit()

endtime = time()

elapsed = endtime - starttime
kilos=downloadedbytes/1024.
megs=downloadedbytes/1048567.
speed=kilos/elapsed
logfile.write("Downloaded " + str(filecounter) + " files (" + str(megs) +" MB in " + str(elapsed) + " sec. (" + str(speed) + " kB/s)." +'\n')

print "\n***************************************************"
print " Script \'fetch_meris_orbits_from_RA.py\' at work... "
print "***************************************************\n"

# EOF

