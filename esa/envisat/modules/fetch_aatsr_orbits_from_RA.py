#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: fetch_aatsr_orbits_from_RA.py

#Download der AATSR NR-Daten vom FTP Server der Rolling Archives

from ftplib import FTP
import os.path
import os
import sys
import time                #wir wollen logfiles mit einem timestamp

def printUsage():
    print("Usage: fetch_aatsr_orbits_from_RA.py serverID productType")
    print("where serverID includes:")
    print("\"ES\", or \"KS\"\n")
    print("and productType is the type specifier for AATSR products.")
    print("Possible productType values are \"NR\" and \"TOA\".")

try:
    argc=len(sys.argv)
    if argc < 3:          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        serverID = sys.argv[1]
        productType = sys.argv[2]
        if (serverID in ["ES", "KS"] and productType in ["NR", "TOA"]):
            # do something
            print("\nSynchronising " + str(sys.argv[1]) + " products with local archive...")
        else:               # incorrect parameters
            print("Wrong parameters!")
            printUsage()
            sys.exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)    

#sys.exit(1)

print("\n***************************************************")
print(" Script \'fetch_aatsr_orbits_from_RA.py\' at work... ")
print("***************************************************\n")

baseIncomingDir = '/fs14/EOservices/InputPool/AATSR/'
baseDir = baseIncomingDir + productType + '/'
tempDir = baseDir + 'RA_temp/'
dbDir   = baseIncomingDir + productType + '/productsDB/'

if serverID   == "ES":
    archive_id = "ESRIN"
    server     = 'oa-es.eo.esa.int'
    user       = 'atsusr'
    passwd     = 'ats12onra'
elif serverID == "KS":
    archive_id = "Kiruna"
    server     = 'oa-ks.eo.esa.int'
    user       = 'atsusr'
    passwd     = 'ats12onra'

try:
    ftp = FTP(server, user, passwd)    #login
except:
    print("unable to connect to the ftp-server")
    sys.exit(1)

try:
    aatsr_files = ftp.nlst()                #Liste der files erstellen 
except:
    print("directory does not exist on the ftp-server")
    sys.exit(1)

#print aatsr_files

thetime   = time.localtime()
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
    print("unable to open the log file")
    ftp.quit()
    sys.exit(1)

filecounter=0
downloadedbytes=0
starttime=time.time()

# wir wollen nur diese orbits:
'''
aatsr_orbits = ['_00008_', '_00022_', '_00036_', '_00037_', '_00051_', \
                '_00065_', '_00079_', '_00080_', '_00094_', '_00108_', \
                '_00122_', '_00123_', '_00136_', '_00137_', '_00151_', \
                '_00165_', '_00166_', '_00179_', '_00180_', '_00194_', \
                '_00208_', '_00209_', '_00222_', '_00223_', '_00237_', \
                '_00251_', '_00265_', '_00266_', '_00280_', '_00294_', \
                '_00308_', '_00309_', '_00323_', '_00337_', '_00351_', \
                '_00352_', '_00366_', '_00380_', '_00394_', '_00395_', \
                '_00409_', '_00423_', '_00437_', '_00438_', '_00451_', \
                '_00452_', '_00466_', '_00480_', '_00494_', '_00495_']
'''
proc_list  = {}
proc_count = 0

for item in aatsr_files:
#    for rel_orbit_count in range(len(aatsr_orbits)):
#        if item.find(aatsr_orbits[rel_orbit_count])>0 and item.startswith('ATS_NR__2'):
    if item.startswith('ATS_' + productType):
        #print aatsr_orbits[rel_orbit_count]+" found in "+ item
        #print "Adding ", item, "to proc_list"
        proc_list[proc_count]=item
        proc_count += 1
        #break

#print "proc_list: " + str(proc_list)


for ftp_aatsr_file in proc_list: 
    
    aatsr_file = os.path.basename(proc_list[ftp_aatsr_file])

    # ATS_NR__2PNPDK20060329_085539_000066042046_00222_21318_0187.N1.gz
    # 0         1         2         3         4         5         6
    # 012345678901234567890123456789012345678901234567890123456789012345   
    year=aatsr_file[14:18]
    month=aatsr_file[18:20]
    day=aatsr_file[20:22]
    
    uncompress = False

    if aatsr_file.endswith('.gz'):
        uncompress_type="gunzip -f"      # force extraction, even if file exists
        uncompress = True
    elif aatsr_file.endswith('.zip'):
        uncompress_type="unzip -o"       # overwrite if file exists
        uncompress = True
    elif aatsr_file.endswith('.N1'):
        uncompress_type="none"
        
    dbPath = dbDir + year + "/" + month + "/" + day + "/"
    dbFile = dbPath + aatsr_file[0:62]    
    dbCommand="touch " + dbFile
    temp_aatsr_file = tempDir + aatsr_file

    if uncompress:
        uncompressCommand = uncompress_type + " " + temp_aatsr_file

    if not os.path.exists(dbPath): # wenn Tag noch nicht existiert
        os.makedirs(dbPath)
        print("day nicht")
            
    if not os.path.exists(dbFile):  # wenn das file noch nicht existiert und es geladen werden soll
        print("Downloading " + aatsr_file + " ..." + '\n')
        ftp.retrbinary('RETR '+aatsr_file, open(temp_aatsr_file, 'wb').write)
        os.system(dbCommand)
        filesize=os.path.getsize(temp_aatsr_file)
        if uncompress:
            os.system(uncompressCommand)
        downloadedbytes=downloadedbytes+filesize
        logfile.write(dbFile+'\n')             # erfolgreich geholtes file, logfile waechst mit
        filecounter += 1
    elif os.path.exists(dbFile):  # wenn das file schon vorhanden ist
        print(aatsr_file+ " already here!")

ftp.quit()

endtime=time.time()
    
elapsed = endtime - starttime
kilos=downloadedbytes/1024.
megs=downloadedbytes/1048567.
speed=kilos/elapsed
logfile.write("Downloaded " + str(filecounter) + " files from " + archive_id + " (" + str(megs) +" MB in " + str(elapsed) + " sec. (" 
+ str(speed) + " kB/s)." +'\n')

print("\n***************************************************")
print(" Script \'fetch_aatsr_orbits_from_RA.py\' finished. ")
print("***************************************************\n")

