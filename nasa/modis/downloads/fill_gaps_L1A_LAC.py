__author__ = 'uwe'

import operator
from os import chdir, getcwd, makedirs, system
from os.path import exists

def ensureTrailingSlash(path):
    if not path.endswith('/'):
        return path + '/'
    else:
        return path


MODIS_localBaseDir = '/fs14/EOservices/InputPool/MODISA/L1A_LAC/' # bcserver7
#MODIS_localBaseDir = '/Volumes/fs14/EOservices/InputPool/MODISA/L1A_LAC/' # bcmacpro1
baseURL = 'http://oceandata.sci.gsfc.nasa.gov/MODISA/L1/'

dates={ '20120530':151, '20120531':152, '20120601':153, '20120602':154, '20120603':155,
        '20120604':156, '20120605':157, '20120606':158, '20120607':159, '20120608':160,
        '20120609':161, '20120610':162, '20120612':164, '20120618':170, '20120629':181,
        '20120630':182, '20120701':183, '20120710':192, '20120711':193, '20120731':213,
        '20120801':214, '20120802':215, '20120803':216, '20120804':217, '20120805':218}

sorted_dates = sorted(iter(dates.items()), key=operator.itemgetter(1))

print(sorted_dates[0][1])

for d in range(len(sorted_dates)):
    datum = sorted_dates[d][0]
    doy   = sorted_dates[d][1]
    _year = datum[:4]
    _month= datum[4:6]
    _day = datum[6:8]
    localInputDir = MODIS_localBaseDir  + ensureTrailingSlash(str(_year)) \
                                        + ensureTrailingSlash(str(_month).zfill(2)) \
                                        + ensureTrailingSlash(str(_day).zfill(2))
    if not exists(localInputDir):
        makedirs(localInputDir)
    chdir(localInputDir)
    destURL = baseURL  + ensureTrailingSlash(str(_year)) + ensureTrailingSlash(str(doy))
    wgetCommand = "wget -nc -S -O - " + destURL + " |grep L1A_LAC.bz2|wget -N --wait=0.5 --random-wait --force-html -i -"
    print(datum, _year, _month, _day, getcwd(), destURL, wgetCommand)
    system(wgetCommand)


    

