#!/usr/bin/env python
from sys import argv

__author__ = 'uwe'

from sys import argv
from os.path import exists
from os import remove

def printUsage():
    print("Usage: ", argv[0], "<date>")
    print("where date is a string representing the date to process,")
    print("e.g. 20120607 for June 7, 2012.")

if len(argv) != 2:
    printUsage()
    exit(1)

back_date = argv[1]
if len(back_date)!=8:
    print("****************************")
    print("* date parameter malformed *")
    print("****************************")
    printUsage()
    exit(1)


trigger_dir = "/fs14/EOservices/OutputPool/MODISA/L3_ECOHAM/signals/"
trigger_file = trigger_dir + "dineof_trigger.txt"

if exists(trigger_file):
    remove(trigger_file)

fh = open(trigger_file, 'w')
fh.write(back_date)
fh.close()

#EOF