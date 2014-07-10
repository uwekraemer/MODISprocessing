__author__ = 'uwe'
from os import system

from utils.utilities import getBackDate


backdays  = range(2,-1,-1)   # [2, 1, 0]

while True:
    for _backday in backdays:
        _backdatetime = getBackDate(_backday)
        _backdate = str(_backdatetime.year) + str(_backdatetime.month).zfill(2) + str(_backdatetime.day).zfill(2)
        geochildgen_l1a_cmd = 'python /home/uwe/cronjobs/nasa/modis/seadas_processing/GEO/create_MODIS_GEO_L1A_extract.py ' + _backdate
        geochildgen_l1b_cmd = 'python /home/uwe/cronjobs/nasa/modis/seadas_processing/l1b/create_MODIS_L1B_sub.py ' + _backdate
        quicklook_gen_cmd   = 'python /home/uwe/cronjobs/nasa/modis/seadas_processing/browse/create_MODIS_L1B_sub_browse.py ' + _backdate

        system(geochildgen_l1a_cmd)
        system(geochildgen_l1b_cmd)
        system(quicklook_gen_cmd)


#for date in `cat datesl1b.txt`; do
#  python /home/uwe/cronjobs/nasa/modis/seadas_processing/GEO/create_MODIS_GEO_L1A_extract.py $date;
#  python /home/uwe/cronjobs/nasa/modis/seadas_processing/l1b/create_MODIS_L1B_sub.py $date;
#  python /home/uwe/cronjobs/nasa/modis/seadas_processing/browse/create_MODIS_L1B_sub_browse.py $date;
#  done
