#!/usr/bin/env python

__author__ = 'uwe'

from os import system
from sys import argv, exit

from utils.utilities import getBackDate
from nasa.modis.seadas_processing.control.processing_scripts import l1aScript, l1bScript, quicklookScript
from nasa.modis.seadas_processing.control.processing_scripts import l2Script, gptTSMScript, l3binningScript
from nasa.modis.seadas_processing.control.processing_scripts import reprojectUTMScript, reprojectECOHAMScript
from nasa.modis.seadas_processing.control.processing_scripts import dineof_notificationScript, wiDeliveryScript


def printUsage():
    print("Usage: ", argv[0], "<backDay>")
    print("where back_day is an integer representing which day to process,")
    print("e.g. 0 for today, 1 for yesterday, etc.")

if len(argv) != 2:
    printUsage()
    exit(1)

try:
    backDay = int(argv[1])
except ValueError:
    print("Wrong parameter: ", argv[1])
    printUsage()
    exit(1)

backDate = getBackDate(backDay)
_year  = str(backDate.year)
_month = str(backDate.month).zfill(2)
_day   = str(backDate.day).zfill(2)
_backdate = _year + _month + _day
print("Processing products of ", _backdate, "...")
# exit(1)

l1aCmd       = 'python ' + l1aScript          + ' ' + _backdate     # L1A_LAC => L1A_sub, GEO_sub
l1bCmd       = 'python ' + l1bScript          + ' ' + _backdate     # L1A_sub, GEO_sub => L1B_sub
qlGenCmd     = 'python ' + quicklookScript    + ' ' + _backdate     # L1B_sub => L1B_RGB
l2Cmd        = 'python ' + l2Script           + ' ' + _backdate     # L1B_sub => L2_sub
gptTSMCmd    = 'python ' + gptTSMScript       + ' ' + _backdate     # L2_sub => L2_TSM
l3binningCmd = 'python ' + l3binningScript    + ' ' + _backdate     # L2_TSM => L3_TSM
reprojectUTMCmd = 'python ' + reprojectUTMScript + ' ' + _backdate     # L3_TSM => L3_UTM, L3_UTM_ql
reprojectECOCmd = 'python ' + reprojectECOHAMScript + ' ' + _backdate  # L3_TSM => L3_ECOHAM
dineofNotificationCmd = 'python ' + dineof_notificationScript + ' ' + _backdate
deliveryCmd  = 'python ' + wiDeliveryScript   + ' ' + _backdate     # upload to data.waterinsight.nl

end2endCommands  = [l1aCmd, l1bCmd, qlGenCmd, l2Cmd, gptTSMCmd, l3binningCmd]
end2endCommands += [reprojectUTMCmd, reprojectECOCmd, dineofNotificationCmd, deliveryCmd]

for cmd in end2endCommands:
    print(cmd)
    print(system(cmd))

# EOF