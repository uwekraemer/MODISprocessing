__author__ = 'uwe'

from os import system

months = ['201303']
days   = range(1, 32, 1)
print(days)

for month in months:
    for day in days:
        _day = month + str(day).zfill(2)
        command = "python /home/uwe/cronjobs/nasa/modis/seadas_processing/l2/create_MODIS_L2_sub.py " + _day
        print(command)
        #_ret = system(command)
