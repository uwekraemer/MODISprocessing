__author__ = 'uwe'

toolsDir = '/Users/uwe/Documents/Development/Python/EOservices/MODISprocessing/bc/eodata/beam_processing/tools/'
beam410HomeDir = '/Applications/beam-4.10/'
beam500HomeDir = '/Applications/beam-5.0/'

beamHomeDir = beam410HomeDir
beamBinDir  = beamHomeDir + 'bin/'
gptProcessor = beamBinDir + 'gpt.command'
pconvProcessor = beamBinDir + 'pconvert.command'
binningProcessor = beamBinDir + 'binning.command'

beamProcessingConfDir ='/Volumes/uwe/cronjobs/bc/eodata/beam_processing/conf/' # bcmacpro1 (development)
TSM_graph_file = toolsDir + 'bandMerge/MODIS_TSM_KdPAR_BandMerge.xml'
UTM_graph_file = toolsDir + 'reproject/reproject_UTM_portal_BandWriter.xml'
ECOHAM_graph_file     = beamProcessingConfDir + 'reproject_BandWriter_ECOHAM.xml'

color_palettes_dir = toolsDir + 'pconvert/color_palettes/'
cobios_chl_palette = color_palettes_dir + 'chl_cobios.cpd'

imageMagickBinDir    = '/usr/local/bin/'
imageMagickConvert   = imageMagickBinDir + 'convert'
imageMagickComposite = imageMagickBinDir + 'composite'
imageMagickMontage   = imageMagickBinDir + 'montage'
imageMagickMogrify   = imageMagickBinDir + 'mogrify'

landMaskFile = toolsDir + 'pconvert/cb_ns_overlay.png'  # Cobios

imageMagickResourcesDir = toolsDir + 'imagemagick/'
legendsDir = imageMagickResourcesDir + 'legends/'
waqssMasksDir = imageMagickResourcesDir + 'masks/'

nosLandmaskFile = waqssMasksDir + 'nosLandMask.png'
basLandmaskFile = waqssMasksDir + 'basLandMask.png'

fontsDir = imageMagickResourcesDir + 'fonts/'
veraBoldFont = fontsDir + 'VeraBd.ttf'

# modisBaseOutputPath = '/Volumes/tank/EOdata/MODISA/'         # bcmacpro1 (processing)
modisBaseOutputPath = '/Volumes/MODISA/MODISA/'         # bcmacpro1 (processing)
modisDailyBasePath  = modisBaseOutputPath + 'daily-merged/'
modisWeeklyBasePath = modisBaseOutputPath + 'weekly/'

wac_graph_file = beamProcessingConfDir + 'binning-wac.xml'
sst_graph_file = beamProcessingConfDir + 'binning-sst.xml'
