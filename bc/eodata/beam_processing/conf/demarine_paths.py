__author__ = 'carole'

modisBaseInputPath  = '/Volumes/MODIS_PROC3/'          # bcserver?
# modisBaseOutputPath = 'U:/INPUT_data/'         # bcserver 13
modisBaseOutputPath = 'W:/DeMarine/'         # bcserver 12-data_sh

modisL2_TSMBasePath_ns = modisBaseInputPath + '/MODISA/L2_TSM/STD/NorthSea/'
modisL2_TSMBasePath_bs = modisBaseInputPath + '/MODISA/L2_TSM/STD/BalticSea/'
modisL3_TSMBasePath  = modisBaseOutputPath + 'L3_BINNED/'
modisL3_TSMDemarine_FineGrid_Path = modisBaseOutputPath + 'L3_REPROJECT_FINE/'
modisL3_TSMDemarine_CoarseGrid_Path = modisBaseOutputPath + 'L3_REPROJECT_COARSE/'


#seadasHome = '/Applications/seadas6.4/'                    # bcmacpro1 (development)
seadasHome = '/home/uwe/tools/seadas/6.4/'                  # bcserver7 (deployment)

seadasScriptsDir = seadasHome + 'run/scripts/'
#seadasBinDir = seadasHome + 'run/bin/macosx_intel/'       # bcmacpro1 (development)
seadasBinDir = seadasHome + 'run/bin/linux/'             # bcserver7 (deployment)

#imageMagickBinDir = '/usr/local/bin/'                      # bcmacpro1 (development)
imageMagickBinDir = '/usr/bin/'                          # bcserver7 (deployment)



