#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: backup_home_dir.py

# Backup uwe's home directory 

from os import system
from time import localtime, strftime
from os.path import exists

print "\n****************************************"
print " Script \'backup_home_dir.py\' at work... "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************\n"

src_dir  = '/home/uwe/'
dest_dir = '/nas01/bcserver7/uwe/'
if not exists(dest_dir):
    mkdir_command = 'mkdir -p ' + src_dir    # we need to create it, otherwise rsync will fail
    system(mkdir_command)

# rsync -avupogtP --delete --delete-after /home/uwe/ /fs4/backups/bcserver7/home/uwe/
rsync_command = 'rsync -avupogtP --delete --delete-after ' + src_dir + ' ' + dest_dir
system(rsync_command)

print "\n****************************************"
print " Script \'backup_home_dir.py\' finished. "
print " Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
print "****************************************\n"

# EOF
