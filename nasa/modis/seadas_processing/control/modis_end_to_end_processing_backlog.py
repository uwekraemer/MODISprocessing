#!/usr/bin/env python

__author__ = 'uwe'

from os import system
from sys import argv, exit

from nasa.modis.seadas_processing.control.processing_scripts import l1aScript, l1bScript, quicklookScript
from nasa.modis.seadas_processing.control.processing_scripts import l2Script, gptTSMScript, l3binningScript
from nasa.modis.seadas_processing.control.processing_scripts import reprojectUTMScript, wiDeliveryScript


def printUsage():
    print("Usage: ", argv[0], "<date>")
    print("where date is a string in format yyyy-MM-dd representing which day to process,")
    print("e.g.  2013-08-23 ")

if len(argv) != 2:
    printUsage()
    exit(1)

date = argv[1]
if not len(date)==10:
    print("Wrong parameter: ", argv[1])
    printUsage()
    exit(1)

_year  = date[0:4]
_month = date[5:7]
_day   = date[8:10]
_backdate = _year + _month + _day
print("Processing products of ", _backdate, "...")

l1aCmd       = 'python ' + l1aScript          + ' ' + _backdate     # L1A_LAC => L1A_sub, GEO_sub
l1bCmd       = 'python ' + l1bScript          + ' ' + _backdate     # L1A_sub, GEO_sub => L1B_sub
qlGenCmd     = 'python ' + quicklookScript    + ' ' + _backdate     # L1B_sub => L1B_RGB
l2Cmd        = 'python ' + l2Script           + ' ' + _backdate     # L1B_sub => L2_sub
gptTSMCmd    = 'python ' + gptTSMScript       + ' ' + _backdate     # L2_sub => L2_TSM
l3binningCmd = 'python ' + l3binningScript    + ' ' + _backdate     # L2_TSM => L3_TSM
reprojectCmd = 'python ' + reprojectUTMScript + ' ' + _backdate     # L3_TSM => L3_UTM, L3_UTM_ql
deliveryCmd  = 'python ' + wiDeliveryScript   + ' ' + _year         # upload to data.waterinsight.nl

end2endCommands = [l1aCmd, l1bCmd, qlGenCmd, l2Cmd, gptTSMCmd, l3binningCmd, reprojectCmd, deliveryCmd]

for cmd in end2endCommands:
    print(cmd)
    print(system(cmd))

# EOF