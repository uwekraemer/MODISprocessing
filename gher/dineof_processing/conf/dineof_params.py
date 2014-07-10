__author__ = 'carole'

filename = 'ECOHAM_2003_chl_day.nc'
variables = ['chlor_a_mean'] # , KdPAR_mean, chlor_a_mean, tsm_678_mean
input_directory = 'G:/MODISA/L3_TSM/STD/NorthSea/reprojected_ECOHAM/2003' #'U:/INPUT_data/reprojected_bilin'
output_directory = 'C:/Users/carole/PycharmProjects/geoinfopy/sandbox/carole/DINEOF_process/DINEOF_inputs'
valid_pixel_threshold = 0.05
watermask_file = 'C:/Users/carole/PycharmProjects/geoinfopy/sandbox/carole/DINEOF_process/water_masks/ECOHAM_watermask.dim'
skipped_file_filename = 'skipped_files_ECOHAM_2003_chl_day.txt'
annual_mean = 'reprojected_bilin_A2010001_2010365_L3_nsea_2.0km.dim' #"C:/Users/carole/PycharmProjects/geoinfopy/sandbox/carole/DINEOF_process/reprojected_bilin_A2010001_2010365_L3_nsea_2.0km.dim")
winter_mean = "U:/INPUT_data/means/reprojected_jan-mar_mean_2010.dim"
spring_mean = "U:/INPUT_data/means/reprojected_apr-jun_mean_2010.dim"
summer_mean = "U:/INPUT_data/means/reprojected_jul-sep_mean_2010.dim"
fall_mean = "U:/INPUT_data/means/reprojected_oct-dec_mean_2010.dim"