#!/usr/bin/env python3
__author__ = 'uwe'

seadasProcessingScriptsBasePath = '/home/uwe/cronjobs/nasa/modis/seadas_processing/'
beamProcessingScriptsBasePath = '/home/uwe/cronjobs/bc/eodata/beam_processing/'
dineofProcessingScriptsBasePath = '/home/uwe/cronjobs/gher/dineof_processing/'
bcDataDistributionScriptsBasePath = '/home/uwe/cronjobs/bc/eodata/distribution/'

# InputPool
l1aScript          = seadasProcessingScriptsBasePath   + 'GEO/create_MODIS_GEO_L1A_extract.py'      # L1A_LAC => L1A_sub, GEO_sub
l1bScript          = seadasProcessingScriptsBasePath   + 'l1b/create_MODIS_L1B_sub.py'              # L1A_sub, GEO_sub => L1B_sub
quicklookScript    = seadasProcessingScriptsBasePath   + 'browse/create_MODIS_L1B_sub_browse.py'    # L1B_sub => L1B_RGB

# OutputPool
l2Script           = seadasProcessingScriptsBasePath   + 'l2/create_MODIS_L2_sub.py'                # L1B_sub => L2_sub
gptTSMScript       = seadasProcessingScriptsBasePath   + 'l2/create_MODIS_TSM.py'                   # L2_sub => L2_TSM
l3binningScript    = beamProcessingScriptsBasePath     + 'l3_binning/create_MODIS_TSM_L3_daily.py'  # L2_TSM => L3_TSM
reprojectUTMScript = beamProcessingScriptsBasePath     + 'reproject/project_L3_daily_UTM.py'        # L3_TSM => L3_UTM, L3_UTM_ql
reprojectECOHAMScript = beamProcessingScriptsBasePath  + 'reproject/project_L3_daily_ECOHAM.py'     # L3_TSM => L3_ECOHAM
dineof_notificationScript = dineofProcessingScriptsBasePath + 'conf/notify_for_dineof.py'
wiDeliveryScript   = bcDataDistributionScriptsBasePath + 'upload_products_for_waterinsight_daily.py' # upload to data.waterinsight.nl
