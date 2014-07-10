#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: get_meris_and_modis_netCDF_from_ACRI.py

#Download der Meris L3-Daten vom ACRI-FTP Server

from ftplib import FTP
from os.path import exists
import os
from sys import argv, exit 
from time import localtime, strftime, time

def ensurePathExists(_path):
    if not exists(_path):
        os.makedirs(_path)

def printUsage():
    print "Usage: get_meris_and_modis_netCDF_from_ACRI.py sensor"
    print "where sensor includes:"
    print "\"MERIS\", or \"MODIS\"\n"

try:
    argc=len(argv)
    if argc == 1:          # the program was called without parameters
        print "Sensor specifier is missing!"
        printUsage()
        exit(1)
    else:                   # we have also received parameters
        if argv[1] in ['MERIS', 'MODIS']:
            sensorID = argv[1]
            print "\Downloading " + sensorID + " .nc products..."
        else:               # incorrect parameter
            print "Wrong sensor specifier!"
            printUsage()
            exit(1)
except:
    print "Error in parameters. Now exiting..."
    exit(1)    


print "\n*************************************************************"
print " Script \'get_meris_and_modis_netCDF_from_ACRI.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "*************************************************************\n"

basepath     = '/fs14/EOservices/InputPool/' + sensorID + '/L3_netCDF/'
if sensorID == 'MERIS':
    resID = '/RR'
else:
    resID = ''

dimapDestDir = '/fs14/EOservices/OutputPool/' + sensorID + resID + '/WAQS-MC/daily/'
ensurePathExists(dimapDestDir)

pconvertTool = '/home/uwe/tools/beam-3.5/bin/pconvert.sh'

thetime   = localtime()
_year  = str(thetime[0])
_month = str(thetime[1]).zfill(2)
_day   = str(thetime[2]).zfill(2)
_hour  = str(thetime[3]).zfill(2)
_minute= str(thetime[4]).zfill(2)
_second= str(thetime[5]).zfill(2)
 
datestring = _year + _month + _day + " " + _hour + ":" + _minute + ":" + _second

try:
    ftp = FTP('ftp.fr-acri.com','ftp_BC','coastwatch_baltic')    #login
except:
    print "unable to connect to the ftp-server"
    exit(1)

if sensorID == 'MERIS':
    try:
        meris_chl12_files = ftp.nlst('meris_chl12')                #Liste der files erstellen
       # print meris_chl12_files, '\n\n'
    except:
        print "directory does not exist on the ftp-server"
    
    try:
        meris_spm_files = ftp.nlst('meris_spm') 
        #print meris_spm_files, '\n\n'
    except:
        print "directory does not exist on the ftp-server"
    
    try:
        meris_trans12_files = ftp.nlst('meris_trans12')
        #print meris_trans12_files, '\n\n'
    except:
        print "directory does not exist on the ftp-server"
    
    try:
        meris_ys_files = ftp.nlst('meris_ys')                #Liste der files erstellen 
        #print meris_ys_files, '\n\n'
    except:
        print "directory does not exist on the ftp-server"
    
    nc_files = meris_chl12_files + meris_spm_files + meris_trans12_files + meris_ys_files
   # print '\n\n', nc_files, '\n\n'
else:
    try:
        modis_chla_files = ftp.nlst('modis_chla')                #Liste der files erstellen 
    except:
        print "directory does not exist on the ftp-server"
    
    nc_files = modis_chla_files

    
list_size = len(nc_files)

for a in range(list_size):
    for item in nc_files:
        if not item.endswith('___0000.nc.gz'):
            nc_files.remove(item)

if not len(nc_files):
    print "No files could be located. Now quitting."
    ftp.quit()
    exit(1)

filecounter=0
downloadedbytes=0
starttime=time()
nc_files.sort()
downloaded_files=[]

for ftp_file in nc_files:     

    nc_file = os.path.basename(ftp_file)
    index=nc_file.find('j__')
    date_str=str(nc_file[index+3:index+11])
    
    year=date_str[0:4]
    month=date_str[4:6]
    day=date_str[6:8]

    ncd_gz_file = basepath+ftp_file
    ncd_file    = str(ncd_gz_file[0:len(ncd_gz_file)-3]) # '.gz' abschneiden
    
    dbpath=basepath + "file_db"
    fulldbpath=dbpath + "/" + year + "/" + month +"/" +day + "/"
    dbfile=fulldbpath + nc_file
    print dbfile, exists(dbfile)
    dbcommand="touch " + dbfile
    uncompressCommand = "gunzip -f " + ncd_gz_file
    pconvertCommand = pconvertTool + " -f dim -o " + dimapDestDir + " " + ncd_file + " &"
    
    if not os.path.exists(fulldbpath): # wenn Tag noch nicht existiert
        os.makedirs(fulldbpath, 0777)

    if not os.path.exists(dbfile):
        print "Downloading " + nc_file + " ..." + '\n'
        ftp.retrbinary('RETR '+ftp_file, open(ncd_gz_file, 'wb').write)
        os.system(dbcommand)
        filesize=os.path.getsize(ncd_gz_file)
        print "Uncompressing " + nc_file + " ..." + '\n'
        os.system(uncompressCommand)
        print "Converting " + nc_file + " to DIMAP format..." + '\n'
        os.system(pconvertCommand)
        downloadedbytes+=filesize
        downloaded_files.append(ftp_file)             # erfolgreich geholtes file, logfile waechst mit
        filecounter += 1

ftp.quit()

endtime=time()

elapsed = endtime - starttime
kilos  = downloadedbytes/1024.
megs   = downloadedbytes/1048567.
speed  = kilos/elapsed

logfilename = basepath+"/ftp_get.log"

try:
    logfile = open(logfilename, 'a')
    logfile.write('\nat '+datestring+':\n')
    logfile.write("Downloaded " + str(filecounter) + " files (" + str(megs) +" MB in " + str(elapsed) + " sec. (" + str(speed) + " kB/s):" +'\n')
    for i in range(filecounter):
        logfile.write(downloaded_files[i] + '\n')
    logfile.close()
except IOError:
    print "unable to open the log file"
    exit(1)


print "\n*************************************************************"
print " Script \'get_meris_and_modis_netCDF_from_ACRI.py\' finished.  "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "*************************************************************\n"

#EOF
