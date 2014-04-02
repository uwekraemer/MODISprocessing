__author__ = 'uwe'

from nasa.modis.seadas_processing.shared.utilities import ensureTrailingSlash
from os.path import exists

from beampy import String
from beampy import Product
from beampy import ProductData
from beampy import ProductIO
from beampy import ProductUtils


inputProductsBaseDir = '/FastBuffer/tsm_computation/L3_products/'
year = '2010'
l3_levels = ['1', '7', '15', '31']

inputProductsDirs = []
for level in l3_levels:
    inputProductsDirs.append(ensureTrailingSlash(ensureTrailingSlash(inputProductsBaseDir+year)+level))

print(inputProductsDirs)

myDOY = '60'

daily_product = inputProductsDirs[0] + 'A' + year + myDOY.zfill(3) + '_' + year + myDOY.zfill(3) + '_L3_nsea_2.0km.dim'
print(daily_product, exists(daily_product))
fallback_prods = []
