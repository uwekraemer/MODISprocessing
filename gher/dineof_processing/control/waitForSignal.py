#!/usr/bin/env python3
__author__ = 'uwe'

from os import rename, system, remove
from os.path import exists
from sys import exit
from time import sleep
from conf.paths import trigger_file, trigger_lock

def read_date(filePath):
    _file = open(filePath, 'r')
    try:
        line = _file.readline()
        return line
    except IOError as err:
        print(("Could not open " + trigger_file).format(err))
        exit(1)


if __name__ == '__main__':
    if exists(trigger_file):
        print("Trigger file found. Starting DINEOF processing...")
        rename(trigger_file, trigger_lock)
        proc_date = read_date(trigger_lock)[:8]

        print("Date is ", proc_date)

        # Processing part comes here
        syscall = "/bin/bash -c \"export LD_LIBRARY_PATH=/etc/alternatives/jdk_home/jre/lib/amd64/server; " \
                  "export BEAM_HOME=/opt/beam-4.11; export PYTHONPATH=/opt/cobios/dineof_processing; " \
                  "python3 /opt/cobios/dineof_processing/control/processDINEOF.py " + proc_date + "\""
        system(syscall)

        try:
            remove(trigger_lock)
        except EnvironmentError as err:
            print("Trigger lock file has disappeared!".format(err))
    else:
        print("\nTrigger file " + trigger_file + " not found. Nothing to do.\n")
        exit(1)

