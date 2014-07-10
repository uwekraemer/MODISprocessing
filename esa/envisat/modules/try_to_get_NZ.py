#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: try_to_get_NZ.py

#Download der Meris FR-Daten vom FTP Server des DLR

from ftplib import FTP
import os.path
import os
import sys
import time                #wir wollen logfiles mit einem timestamp

try:
    ftp = FTP('ftp1.nz.dlr.de','envisat','mapp#!')    #login
except:
    print "unable to connect to the ftp-server"
    sys.exit(1)

try:
    meris_files = ftp.nlst('data')                #Liste der files erstellen 
except:
    print "directory does not exist on the ftp-server"
    sys.exit(1)

print "\n**************************************"
print " Script \'try_to_get_NZ.py\' at work... "
print "**************************************\n"

basepath ='/fs14/EOservices/InputPool/MERIS/FR/NZ'
realpath = basepath+'/images/'

thetime   = time.localtime()
year_str  = str(thetime[0])
month_str = str(thetime[1])
day_str   = str(thetime[2])

if thetime[1] < 10:
    month_str = "0"+ month_str

if thetime[2] < 10:
    day_str = "0"+ day_str

datestring = year_str + month_str + day_str

logfilename = basepath + "/ftp_get.log"

try:
    logfile = open(logfilename, 'a')
    logfile.write('\n'+datestring+'\n')
except:
    print "unable to open the log file"
    sys.exit(1)

filecounter=0
downloadedbytes=0
starttime=time.time()

for ftp_meris_file in meris_files:     

    download=0

    meris_file = os.path.basename(ftp_meris_file)
        
    year=meris_file[14:18]
    month=meris_file[18:20]
    day=meris_file[20:22]
    type =meris_file[4:9]

    if (type.find('FR__1')==0) and ftp.size(ftp_meris_file)>0:
        download=1
    elif (type.find('FR__2')==0) and ftp.size(ftp_meris_file)>0:
        download=0

    if download==0:
        print "Skipping " + meris_file + ".\n"
        break
        
    dummypath    = basepath  + "/" + year + "/" + month +"/" +day + "/"
    dummyfile    = dummypath + meris_file
    dummycommand ="touch " + dummyfile

    real_meris_file = realpath + meris_file

    if not os.path.exists(basepath+"/" + year):        #wenn Jahr noch nicht existiert
        os.mkdir(basepath+"/" + year)                  #directory year
        os.mkdir(basepath+"/" + year+"/" + month)      #directory month
        os.mkdir(dummypath)                            #directory day
        print "year nicht"
    elif not os.path.exists(basepath + "/" + year + "/" + month):             # wenn Monat noch nicht existiert
        os.mkdir(basepath+"/" + year+"/" + month)
        os.mkdir(dummypath)
        print "month nicht"
    elif not os.path.exists(basepath + "/" + year + "/" + month + "/" + day): # wenn Tag noch nicht existiert
        os.mkdir(dummypath)
        print "day nicht"

    if not os.path.exists(dummyfile) and download == 1:  # wenn das file noch nicht existiert und es geladen werden soll
        print "Downloading " + meris_file + " ..." + '\n'
        ftp.retrbinary('RETR '+ftp_meris_file, open(real_meris_file, 'wb').write)
        os.system(dummycommand)
        filesize = os.path.getsize(real_meris_file)
        downloadedbytes = downloadedbytes + filesize
        logfile.write(dummyfile +'\n')             # erfolgreich geholtes file, logfile waechst mit
        filecounter = filecounter + 1
    elif os.path.exists(dummyfile) and download==1:  # wenn das file schon vorhanden ist
        print meris_file + " already here!"        

ftp.quit()

endtime=time.time()
    
elapsed = endtime - starttime
kilos   = downloadedbytes / 1024.
megs    = downloadedbytes / 1048567.
speed   = kilos / elapsed
log_string = "Downloaded " + str(filecounter) + " files (" + str(megs) +" MB in " + str(elapsed) + " sec. (" + str(speed) + " kB/s)." +'\n'
logfile.write(log_string)
logfile.close()

print "\n" + log_string + "\n"

print "\n**************************************"
print " Script \'try_to_get_NZ.py\' finished. "
print "**************************************\n"

#EOF
