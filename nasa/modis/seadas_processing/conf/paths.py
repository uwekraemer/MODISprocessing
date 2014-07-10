__author__ = 'uwe'

modisBaseInputPath = '/Volumes/fs14-1/EOservices/InputPool/MODISA/' # bcmacpro1 (development)
# modisBaseInputPath  = '/fs14/EOservices/InputPool/MODISA/'          # bcserver7 (deployment)
modisBaseOutputPath = '/Volumes/fs14-1/EOservices/OutputPool/MODISA/'         # bcserver7 (deployment)
# modisBaseOutputPath = '/fs14/EOservices/OutputPool/MODISA/'         # bcserver7 (deployment)

modisGEOBasePath     = modisBaseInputPath + 'GEO/'
modisGEO_subBasePath = modisBaseInputPath + 'GEO_sub/'
modisL1A_LACBasePath = modisBaseInputPath + 'L1A_LAC/'
modisL1A_subBasePath = modisBaseInputPath + 'L1A_sub/'
modisL1B_HKMBasePath = modisBaseInputPath + 'L1B_HKM/'
modisL1B_QKMBasePath = modisBaseInputPath + 'L1B_QKM/'
modisL1B_LACBasePath = modisBaseInputPath + 'L1B_LAC/'
modisL1B_subBasePath = modisBaseInputPath + 'L1B_sub/'
modisL1B_OBCBasePath = modisBaseInputPath + 'L1B_OBC/'
modisBrowseBasePath  = modisBaseInputPath + 'L1B_RGB/'

modisL2_LACBasePath = modisBaseOutputPath + 'L2_LAC/'
modisL2_TSMBasePath = modisBaseOutputPath + 'L2_TSM/'
modisL2_FRTBasePath = modisBaseOutputPath + 'L2_FRT/'       # by-products for Fronten project
modisL2_subBasePath = modisBaseOutputPath + 'L2_sub/'
modisL3_TSMBasePath = modisBaseOutputPath + 'L3_TSM/'       # L3 binned products, large area. Name e.g. cb_ns_20130603_eo_bc_lat_lon.dim
modisL3_TSM_UTMPath = modisBaseOutputPath + 'L3_UTM/'       # reprojected L3 products,        Name e.g. cb_ns_20130603_eo_bc.dim
modisL3_TSM_UTM_QLPath  = modisBaseOutputPath + 'L3_UTM_ql/'# quicklooks from reprojected L3 products
modisL3_ECOHAMBasePath  = modisBaseOutputPath + 'L3_ECOHAM/'# reprojected L3 products,        Name e.g. cb_ns_20130603_eo_ecoham.dim


################ SeaDAS 6.4 ################
#seadasHome = '/Applications/seadas6.4/'                    # bcmacpro1 (development)
# seadasHome = '/home/uwe/tools/seadas/6.4/'                  # bcserver7 (deployment)

# seadasScriptsDir = seadasHome + 'run/scripts/'
#seadasBinDir = seadasHome + 'run/bin/macosx_intel/'       # bcmacpro1 (development)
# seadasBinDir = seadasHome + 'run/bin/linux/'             # bcserver7 (deployment)

################ SeaDAS 7.0 ################
seadasOCSSWROOT = '/Applications/seadas-7.0.2/ocssw/'           # bcmacpro1 (development)
# seadasOCSSWROOT = '/home/uwe/tools/seadas/7.0.2/ocssw/'  # bcserver7 (deployment)

seadasScriptsDir = seadasOCSSWROOT + 'run/scripts/'
seadasBinDir = seadasOCSSWROOT + 'run/bin/macosx_intel/'       # bcmacpro1 (development)
# seadasBinDir = seadasOCSSWROOT + 'run/bin/linux/'             # bcserver7 (deployment)


############### ImageMagick ################
#imageMagickBinDir = '/usr/local/bin/'                      # bcmacpro1 (development)
imageMagickBinDir = '/usr/bin/'                          # bcserver7 (deployment)

beam_410Home   = '/home/uwe/tools/beam-4.10/'
beam_410BinDir = beam_410Home + 'bin/'
l3binningDir   = '/fs14/temp/.l3binning/'
