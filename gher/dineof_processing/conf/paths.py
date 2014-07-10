#!/usr/bin/env python3
__author__ = 'uwe'

inputBaseDir = "/fs14/EOservices/OutputPool/MODISA/L3_ECOHAM/"

trigger_dir = inputBaseDir + "signals/"
trigger_file = trigger_dir + "dineof_trigger.txt"
trigger_lock = trigger_file.replace("txt", "lck")

productionBaseDir = '/opt/cobios/data/'
dineof_inputDir  = productionBaseDir + 'dineof_input/'
dineof_outputBaseDir = productionBaseDir + 'dineof_output/'

watermask_nc_file = dineof_inputDir + 'ECOHAM_watermask.nc'
watermask_dim_file = dineof_inputDir + 'ECOHAM__watermask.dim'

dineof_home = '/opt/dineof-3.0/'
dineof_executable = dineof_home + 'dineof'
