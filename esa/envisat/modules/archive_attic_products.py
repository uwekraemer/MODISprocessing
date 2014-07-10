#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: archive_attic_products.py

# Products have been put to the attic if they are older than a specified amount of days
# To save disk space, this script puts each product in a single tgz archive.

from smtplib import SMTP
from os import system, walk
from os.path import normpath
from sys import exit
from time import time, localtime, strftime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

print("\n***********************************************\n")
print(" Script \'archive_attic_products.py\' at work... \n")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()) + '\n')
print("***********************************************\n")

message_header = "<p>Script <b>archive_attic_products.py</b><br>" +  "Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()) + '</p>'

from_address = 'uwe@bcserver7.bc.intern'  
to_address   = 'uwe.kraemer@brockmann-consult.de'

def send_mail(message):
    message = message_header + message
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'An error message from bcserver7'
    msgRoot['From'] = from_address
    msgRoot['To'] = to_address
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    
    msgText = MIMEText('This mail was intended to be read as html.')
    msgAlternative.attach(msgText)
    
    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(message, 'html')
    msgAlternative.attach(msgText)
    
    # We use a special image to be embedded
    fp = open('/home/uwe/tools/attention.jpg', 'rb')
    #fp = open('/home/uwe/tools/attention.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    
    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
        
    server = SMTP('localhost')
    server.set_debuglevel(1)
    try:
        server.sendmail(from_address, to_address, msgRoot.as_string())
    except:
        print("Email could not be sent. Now quitting.")
        server.quit()
        exit(1)
    server.quit()

# These directories are being scanned
targetDirectories = ['/fs14/EOservices/Attic/AATSR/NR/',
                     '/fs14/EOservices/Attic/MERIS/RR/WAQS-caseR/',
                     '/fs14/EOservices/Attic/MERIS/RR/WAQS-IPF/',
                     '/fs14/EOservices/Attic/MERIS/RR/WAQS-MC/',
                     '/fs14/EOservices/Attic/MERIS/RR/WAQS-WeW/',
                     '/fs14/EOservices/Attic/MERIS/RR/L1b-Estonia/'
                     ]
send_a_mail = False
message = ''

for item in targetDirectories:
    for root, dirs, files in walk(item):
        for file in files:
            if file.endswith('.dim'):
                system('cd ' + root)
                dirName = file[0:len(file)-3]+'data'
                if dirName in dirs:
                    dirPath = normpath(root + '/' + dirName) + '/'
                    srcPath = dirPath.replace('Attic', 'OutputPool')
                    # to be sure that it is complete, the directory will be synced with the OutputPool
                    rsyncCommand = 'rsync -avupogtP ' + srcPath + ' ' + dirPath
                    print(rsyncCommand)
                    system(rsyncCommand)
                    archive_call = 'cd ' + root + '; tar czf ' + file[0:len(file)-3] + 'tgz ' + file[0:len(file)-2] + '*'
                    print(archive_call)
                    if system(archive_call) == 0:
                        remove_call = 'cd ' + root + '; rm -r ' + file[0:len(file)-2]+'*'
                        print(remove_call)
                        try:
                            #pass
                            print('Trying to remove DIMAP file ' + file + ' and the accompanying data directory...')
                            system(remove_call)
                        except:
                            send_a_mail = True
                            subject = '<b>Directory could not be removed:</b><br>'
                            message = message + subject + 'The command ' + remove_call + ' was not successful. Please check.<br>'
                else:
                    if file.startswith('._'):
                        # somehow filenames like '._20060215_20060221_wew_north_sea_l3_1.2km.dim'
                        # exist in the concerned directories. Ignore them:
                        pass
                    else:
                        # Assuming this is a regular DIMAP XML file, we now try to complete missing files 
                        # (the script that puts files to the attic works on time stamps, so if a file 
                        # is being touched afterwards, it would not be put to the attic. This would result
                        # in directories with the same name on both sides, both incomplete.)
                        dirPath = normpath(root + '/' + dirName) + '/'
                        srcPath = dirPath.replace('Attic', 'OutputPool')
                        # try to get it from the OutputPool
                        rsyncCommand = 'rsync -avupogtP ' + srcPath + ' ' + dirPath
                        print(rsyncCommand)
                        system(rsyncCommand)
                        send_a_mail = True
                        subject = '<b>Data directory of dimap was missing:</b><br>'
                        message = message + subject + 'The accompanying data directory for the file ' + root + file + '/ did not exist.<br>'
                        message = message + 'It has been tried to copy it from ' + srcPath + '. Please check.<br>'

if send_a_mail == True:
    send_mail(message)
 
print("\n**********************************************")
print(" Script \'archive_attic_products.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("**********************************************\n")

# EOF