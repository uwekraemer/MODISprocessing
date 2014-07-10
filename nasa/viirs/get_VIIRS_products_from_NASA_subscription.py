__author__ = 'uwe'

from nasa.viirs.seadas_processing.conf.paths import viirsL2_SubsBasePath
from ftplib import FTP
from utils.utilities import ensureTrailingSlash, exit_on_empty_list, filter_list, getDateFromDOY
from os.path import exists
from os import chdir, getcwd, makedirs

ftp_server = 'samoa.gsfc.nasa.gov'
ftp_user = 'anonymous'
ftp_pass = 'viirs@brockmann-consult.de'

subscription = '2439'   # NorthSeaBalticSea region (http://oceancolor.gsfc.nasa.gov/sdpscgi/registered/subscriptions_manager.cgi)
user = 'bconsult'       # Subscription user: bconsult  password: volcano:vie

ftp_dir = '/subscriptions/VIIRS/XM/' + user + '/' + subscription
print(ftp_dir)
ftp_connection = FTP(host=ftp_server, user=ftp_user, passwd=ftp_pass)
ftp_connection.cwd(ftp_dir)
ftp_listing = ftp_connection.nlst()
exit_on_empty_list(ftp_listing)
listing = filter_list(ftp_listing, extension='.hdf')
listing.sort()
# print(listing)

for product_name in listing:
    acq_year = product_name[1:5]
    acq_doy = product_name[5:8]
    acq_date = getDateFromDOY(_year=acq_year, DOY=acq_doy)
    download_dir = viirsL2_SubsBasePath + ensureTrailingSlash(str(acq_year)) + ensureTrailingSlash(str(acq_date.month).zfill(2)) + ensureTrailingSlash(str(acq_date.day).zfill(2))
    if not exists(download_dir):
        makedirs(download_dir)
    chdir(download_dir)
    if not exists(product_name):
        print("Downloading " + product_name + " to " + download_dir + "...")
        ftp_connection.retrbinary('RETR '+product_name, open(product_name, 'wb').write)
    else:
        print("Product already here. Continuing...")
        continue

ftp_connection.quit()

# product names:
# V2014146064402.L2_NPP.NorthSeaBalticSea.hdf