__author__ = 'uwe'

from nasa.modis.seadas_processing.conf.params import _processing, _site
from nasa.modis.seadas_processing.shared.utilities import ensureTrailingSlash

modisBaseInputPath = '/Volumes/tank/EOdata/MODISA/' # bcmacpro1 (development)

modisGEOBasePath     = modisBaseInputPath + 'GEO/'     + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)
modisGEO_subBasePath = modisBaseInputPath + 'GEO_sub/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)

modisL1A_LACBasePath = modisBaseInputPath + 'L1A_LAC/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)
modisL1A_subBasePath = modisBaseInputPath + 'L1A_sub/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)

modisL1B_HKMBasePath = modisBaseInputPath + 'L1B_HKM/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)
modisL1B_QKMBasePath = modisBaseInputPath + 'L1B_QKM/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)

modisL1B_LACBasePath = modisBaseInputPath + 'L1B_LAC/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)
modisL1B_subBasePath = modisBaseInputPath + 'L1B_sub/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)

modisL1B_OBCBasePath = modisBaseInputPath + 'L1B_OBC/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)
modisBrowseBasePath  = modisBaseInputPath + 'L1B_RGB/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)

modisL2_LACBasePath  = modisBaseInputPath + 'L2_LAC/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)
modisL2_subBasePath  = modisBaseInputPath + 'L2_sub/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)

# modisL2_TSMBasePath  = modisBaseInputPath + 'L2_TSM/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)
modisL2_TSMBasePath  = '/Volumes/MODISA/MODISA/L2_TSM/'
# modisL2_TSMBasePath  = '/Volumes/fs14/EOservices/OutputPool/MODISA/L2_TSM/'
#
# modisL3_TSMBasePath  = modisBaseInputPath + 'L3_TSM/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)     # L3 binned products, large area. Name e.g. cb_ns_20130603_eo_bc_lat_lon.dim
modisL3_TSMBasePath  = '/Volumes/MODIS_PROC8/MODISA/L3_TSM/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)     # L3 binned products, large area. Name e.g. cb_ns_20130603_eo_bc_lat_lon.dim

# modisL3_TSM_UTMPath  = modisBaseInputPath + 'L3_UTM/'      # reprojected L3 products,        Name e.g. cb_ns_20130603_eo_bc.dim
modisL3_TSM_UTMPath  = '/Volumes/MODIS_PROC8/MODISA/L3_UTM/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)      # reprojected L3 products,        Name e.g. cb_ns_20130603_eo_bc.dim
modisL3_TSM_UTM_QLPath  = '/Volumes/MODIS_PROC8/MODISA/L3_UTM_ql/' + ensureTrailingSlash(ensureTrailingSlash(_processing) + _site)# quicklooks from reprojected L3 products

seadasHome = '/Applications/seadas6.4/'                     # bcmacpro1 (development)

seadasScriptsDir = seadasHome + 'run/scripts/'
seadasBinDir = seadasHome + 'run/bin/macosx_intel/'         # bcmacpro1 (development)

imageMagickBinDir = '/usr/local/bin/'                       # bcmacpro1 (development)

beam_410Home ='/Applications/beam-4.10/'                    # bcmacpro1 (development)
beam_410BinDir = beam_410Home + 'bin/'
l3binningDir = '/Volumes/SpeedDisk/l3binning/'
