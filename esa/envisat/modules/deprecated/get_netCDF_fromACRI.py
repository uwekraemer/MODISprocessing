#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: get_netCDF_fromACRI.py

#Download der Meris L3-Daten vom ACRI-FTP Server

from ftplib import FTP
import os.path
import os
import sys
from time import localtime, strftime, time

print("\n********************************************")
print(" Script \'get_netCDF_fromACRI.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("********************************************\n")

basepath='/fs14/EOservices/InputPool/MERIS/L3_netCDF/'
pconvertTool='/home/uwe/tools/beam-3.5/bin/pconvert'
dimapDestDir='/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily/'

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

logfilename = basepath+"/ftp_get.log"

try:
    logfile = open(logfilename, 'a')
    logfile.write('\nat '+datestring+':\n')
except:
    print("unable to open the log file")
    sys.exit(1)

try:
    ftp = FTP('ftp.fr-acri.com','BC','coastwatch_baltic')    #login
except:
    print("unable to connect to the ftp-server")
    sys.exit(1)

try:
    meris_chl12_files = ftp.nlst('meris_chl12')                #Liste der files erstellen 
except:
    print("directory does not exist on the ftp-server")

try:
    meris_spm_files = ftp.nlst('meris_spm') 
except:
    print("directory does not exist on the ftp-server")

try:
    meris_trans12_files = ftp.nlst('meris_trans12')
except:
    print("directory does not exist on the ftp-server")

try:
    meris_ys_files = ftp.nlst('meris_ys')                #Liste der files erstellen 
except:
    print("directory does not exist on the ftp-server")

meris_files = meris_chl12_files + meris_spm_files + meris_trans12_files + meris_ys_files

list_size = len(meris_files)

for a in range(list_size):
    for item in meris_files:
        if not item.endswith('___0000.nc.gz'):
            meris_files.remove(item)

if len(meris_files) == 0:
    print("No files could be located. Now quitting.")
    ftp.quit()
    sys.exit(1)

filecounter=0
downloadedbytes=0
starttime=time()

for ftp_meris_file in meris_files:     

    meris_file = os.path.basename(ftp_meris_file)
    index=meris_file.find('j__')
    date_str=str(meris_file[index+3:index+11])
    
    year=date_str[0:4]
    month=date_str[4:6]
    day=date_str[6:8]

    meris_ncd_gz_file = basepath+ftp_meris_file
    meris_ncd_file    = str(meris_ncd_gz_file[0:len(meris_ncd_gz_file)-3]) # '.gz' abschneiden
    
    dbpath=basepath + "file_db"
    fulldbpath=dbpath + "/" + year + "/" + month +"/" +day + "/"
    dbfile=fulldbpath + meris_file
    dbcommand="touch " + dbfile
    uncompressCommand = "gunzip " + meris_ncd_gz_file
    pconvertCommand = pconvertTool + " -f dim -o " + dimapDestDir + " " + meris_ncd_file + " &"
    
    if not os.path.exists(fulldbpath): # wenn Tag noch nicht existiert
        os.makedirs(fulldbpath, 0o777)

    if not os.path.exists(dbfile):
        print("Downloading " + meris_file + " ..." + '\n')
        ftp.retrbinary('RETR '+ftp_meris_file, open(meris_ncd_gz_file, 'wb').write)
        os.system(dbcommand)
        filesize=os.path.getsize(meris_ncd_gz_file)
        print("Uncompressing " + meris_file + " ..." + '\n')
        os.system(uncompressCommand)
        print("Converting " + meris_file + " to DIMAP format..." + '\n')
        os.system(pconvertCommand)
        downloadedbytes=downloadedbytes+filesize
        logfile.write(ftp_meris_file+'\n')             # erfolgreich geholtes file, logfile waechst mit
        filecounter=filecounter+1

ftp.quit()

endtime=time()
    
elapsed = endtime - starttime
kilos  = downloadedbytes/1024.
megs   = downloadedbytes/1048567.
speed  = kilos/elapsed
logfile.write("Downloaded " + str(filecounter) + " files (" + str(megs) +" MB in " + str(elapsed) + " sec. (" + str(speed) + " kB/s)." +'\n')
logfile.close()

print("\n********************************************")
print(" Script \'get_netCDF_fromACRI.py\' finished.  ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("********************************************\n")

#EOF
