__author__ = 'uwe'

from datetime import date
from sys import argv


def printUsage():
    print("Usage: getDOY.py <date>")
    print("where date is a string value specifying the date for which the Day Of Year shall be computed:")
    print("e.g. 20120510. It has to start with \'20\' and must be exactly 8 characters long.")


argc=len(argv)
if argc < 2:          # the program was called incorrectly
    print("\nToo few parameters passed!")
    printUsage()
    exit(1)

try:
    _date = str(argv[1])
except TypeError:
    print("date parameter must be of type string!")
    printUsage()
    print("\nError in parameters. Now exiting...\n")
    exit(1)

if not len(_date)==8 or not _date.startswith('20'):
    print("\ndate parameter unusable.")
    printUsage()
    exit(1)

_year = int(_date[:4])
_month =  int(_date[4:6])
_day = int(_date[6:8])

#print _year, _month, _day

ref0Year = _year - 1
#print ref0Year

def getDOY():
    d0 = date(ref0Year, 12, 31)
    #print d0
    d1 = date(_year, _month, _day)
    #print d1
    delta=d1-d0
    return delta.days

doy=getDOY()
print(doy)


