#!/usr/bin/env python3

__author__ = 'uwe'

# bcmacpro1 (Development)
# viirsBaseInputPath  = '/Volumes/fs14-1/EOservices/InputPool/VIIRS/'
# viirsBaseOutputPath = '/Volumes/fs14-1/EOservices/OutputPool/VIIRS/'

# bcserver7vm (Deployment)
viirsBaseInputPath  = '/fs14/EOservices/InputPool/VIIRS/'
viirsBaseOutputPath = '/fs14/EOservices/OutputPool/VIIRS/'

viirsL1A_BasePath = viirsBaseInputPath + 'NASA/L1A/'
viirsL2_BasePath  = viirsBaseOutputPath + 'NASA/L2/'
viirsL2_SubsBasePath  = viirsBaseOutputPath + 'NASA/L2_subscription/'

# macmini (Home Development)
# viirsBaseInputPath  = '/Volumes/ImageData/EOdata/VIIRS/'
# viirsBaseOutputPath = viirsBaseInputPath
#
# viirsL1A_BasePath = viirsBaseInputPath + 'NASA-oceandata/L1A/'
# viirsL2_BasePath  = viirsBaseOutputPath + 'NASA-oceandata/L2/'
#
# seadasHome = '/Applications/seadas-7.0.2/'                    # macmini (Home Development)
seadasHome = '/home/uwe/tools/seadas/7.0.2/'                  # bcserver7vm (deployment)

seadasScriptsDir = seadasHome + 'ocssw/run/scripts/'
# seadasBinDir = seadasHome + 'ocssw/run/bin/macosx_intel/'     # macmini (Home Development)
seadasBinDir = seadasHome + 'ocssw/run/bin/linux/'            # bcserver7vm (deployment)
