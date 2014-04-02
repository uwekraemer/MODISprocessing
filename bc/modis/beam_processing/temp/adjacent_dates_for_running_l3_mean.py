__author__ = 'uwe'

from calendar import isleap
from glob import glob as glob
from os import makedirs, remove
from os.path import exists

from nasa.modis.seadas_processing.shared.utilities import getDateFromDOY, ensureTrailingSlash


_beamBinDir = '/Applications/beam-4.10/bin/'
_l3_binning_processor = _beamBinDir + 'binning.command'

_year = 2011
_num_days_in_l3 = 31

_productsBaseInputPath  = '/Volumes/MODIS_PROC5/MODISA/L2_TSM/STD/NorthSea/'
_productsOutputPath     = '/FastBuffer/tsm_computation/L3_products/' \
                          + ensureTrailingSlash(str(2010)) \
                          + ensureTrailingSlash(str(_num_days_in_l3))
if not exists(_productsOutputPath):
    makedirs(_productsOutputPath)
_requestsOutputPath     = _productsOutputPath.replace('L3_products', 'L3_requests')
if not exists(_requestsOutputPath):
    makedirs(_requestsOutputPath)

_productRegExp = '??????.L2_TSM.dim'

_l3_lat_min, _l3_lat_max, _l3_lon_min, _l3_lon_max = 47.0, 64.0, -15.0, 12.0
_l3_binning_db_path = '/Volumes/SpeedDisk/l3_database_' + str(_num_days_in_l3) + 'd.bindb'
_l3_out_prod_type = 'BEAM-DIMAP' # possible other types: CSV, GeoTIFF, HDF5, NetCDF-BEAM, NetCDF-CF, NetCDF4-BEAM
_l3_out_prod_ext  = '.dim'       # possible other types: .csv, .tiff, .hdf5, .nc, .nc, .nc  # TODO check nc extensions
_l3_xml_type_str = '<?xml version="1.0" encoding="ISO-8859-1"?>\n'

_l3_xml_req_list_opener = '<RequestList>\n'
_l3_xml_req_list_closer = '</RequestList>\n'

_l3_xml_req_type_opener = '    <Request type="BINNING">\n'
_l3_xml_req_type_closer = '    </Request>\n'

_l3_xml_inp_prod_opener = '        <InputProduct file="'
_l3_xml_inp_prod_closer = '" />\n'

_l3_region = 'nsea'
_l3_resolution = '2.0'    # km
_l3_xml_out_prod_opener = '        <OutputProduct file="'
_l3_xml_out_prod_closer = '" format="'+ _l3_out_prod_type + '" />\n'

def get_l3_binning_init_block():
    _l3_init_parameter  = '        <Parameter name="process_type" value="init" />\n'
    _l3_init_parameter += '        <Parameter name="database" value="' + _l3_binning_db_path + '" />\n'
    _l3_init_parameter += '        <Parameter name="lat_min" value="'+ str(_l3_lat_min) + '" />\n'
    _l3_init_parameter += '        <Parameter name="lat_max" value="'+ str(_l3_lat_max) + '" />\n'
    _l3_init_parameter += '        <Parameter name="lon_min" value="'+ str(_l3_lon_min) + '" />\n'
    _l3_init_parameter += '        <Parameter name="lon_max" value="'+ str(_l3_lon_max) + '" />\n'
    _l3_init_parameter += '        <Parameter name="log_prefix" value="l3" />\n'
    _l3_init_parameter += '        <Parameter name="log_to_output" value="false" />\n'
    _l3_init_parameter += '        <Parameter name="resampling_type" value="binning" />\n'
    _l3_init_parameter += '        <Parameter name="grid_cell_size" value="' + _l3_resolution + '" />\n'
    _l3_init_parameter += '        <Parameter name="band_name.0" value="chlor_a" />\n'
    _l3_init_parameter += '        <Parameter name="bitmask.0" value="fneq(chlor_a,-32767.0) AND NOT l2_flags.CHLFAIL AND NOT l2_flags.CHLWARN AND NOT l2_flags.PRODWARN" />\n'
    _l3_init_parameter += '        <Parameter name="binning_algorithm.0" value="Arithmetic Mean" />\n'
    _l3_init_parameter += '        <Parameter name="weight_coefficient.0" value="1.0" />\n'
    _l3_init_parameter += '        <Parameter name="band_name.1" value="Kd_490" />\n'
    _l3_init_parameter += '        <Parameter name="bitmask.1" value="fneq(Kd_490, -6.553399834447191)" />\n'
    _l3_init_parameter += '        <Parameter name="binning_algorithm.1" value="Arithmetic Mean" />\n'
    _l3_init_parameter += '        <Parameter name="weight_coefficient.1" value="1.0" />\n'
    _l3_init_parameter += '        <Parameter name="band_name.2" value="tsm_678" />\n'
    _l3_init_parameter += '        <Parameter name="bitmask.2" value="tsm_678 &gt; 0.0" />\n'
    _l3_init_parameter += '        <Parameter name="binning_algorithm.2" value="Arithmetic Mean" />\n'
    _l3_init_parameter += '        <Parameter name="weight_coefficient.2" value="1.0" />\n'
    _l3_init_parameter += '        <Parameter name="band_name.3" value="KdPAR" />\n'
    _l3_init_parameter += '        <Parameter name="bitmask.3" value="((fneq(Kd_412_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_443_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_469_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_488_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_531_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_547_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_555_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_645_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_667_lee,-6.553399834447191) '
    _l3_init_parameter +=                                   '&amp;&amp; fneq(Kd_678_lee,-6.553399834447191)))'
    _l3_init_parameter +=                                   '&amp;&amp; !nan(KdPAR)" />\n'
    _l3_init_parameter += '        <Parameter name="binning_algorithm.3" value="Arithmetic Mean" />\n'
    _l3_init_parameter += '        <Parameter name="weight_coefficient.3" value="1.0" />\n'
    return _l3_init_parameter

def get_l3_binning_update_block():
    _l3_update_parameter  = '        <Parameter name="process_type" value="update" />\n'
    _l3_update_parameter += '        <Parameter name="database" value="' + _l3_binning_db_path + '" />\n'
    _l3_update_parameter += '        <Parameter name="log_prefix" value="l3" />\n'
    _l3_update_parameter += '        <Parameter name="log_to_output" value="false" />\n'
    return _l3_update_parameter

def get_l3_binning_finalize_block():
    _l3_finalize_parameter  = '        <Parameter name="process_type" value="finalize" />\n'
    _l3_finalize_parameter += '        <Parameter name="database" value="' + _l3_binning_db_path + '" />\n'
    _l3_finalize_parameter += '        <Parameter name="delete_db" value="true" />\n'
    _l3_finalize_parameter += '        <Parameter name="log_prefix" value="l3" />\n'
    _l3_finalize_parameter += '        <Parameter name="log_to_output" value="false" />\n'
    _l3_finalize_parameter += '        <Parameter name="tailoring" value="false" />\n'
    return _l3_finalize_parameter

print(str(_year)+ " is leap year: "+ str(isleap(_year)))
print("Number of days in each L3 product: ", _num_days_in_l3)

if isleap(_year):
    num_days_in_year = 366
else:
    num_days_in_year = 365

doys = range(1, num_days_in_year, 1)
doys=[str(i).zfill(3) for i in doys]


_batch_file_path = _requestsOutputPath + 'A' + str(_year) + '_' + str(_num_days_in_l3) + 'days.txt'
_batch_file = open(_batch_file_path, 'a')
_batch_file.write('#!/bin/bash\n')

from bc.modis.beam_processing.temp.temp import get_dates_33
_year_seq = get_dates_33()
print(_year_seq)
#exit(1)

for _seq_ind in range(len(_year_seq)):
    _seq = _year_seq[_seq_ind]
    print("New request:", _seq)
    _output_product_name = 'A' + _seq[0] + '_' + _seq[-1] + '_L3_' + _l3_region + '_' + _l3_resolution + 'km' + _l3_out_prod_ext
    _output_product_path = _productsOutputPath + _output_product_name
    _request_file_name   = _output_product_name.replace(_l3_out_prod_ext, '.xml')
    _request_file_path   = _requestsOutputPath + _request_file_name
    _inputProducts =[]
    for index in range(_num_days_in_l3):
        _date = getDateFromDOY(_year, int(_year_seq[_seq_ind][index]))
        _datePath = ensureTrailingSlash(str(_date.year)) + \
                    ensureTrailingSlash(str(_date.month).zfill(2)) + \
                    ensureTrailingSlash(str(_date.day).zfill(2))
        _productsInputPath = _productsBaseInputPath +  _datePath
        _glob_expression =  _productsInputPath + 'A' + str(_year) + _year_seq[_seq_ind][index] + _productRegExp
        _glob_result = glob(_glob_expression)
        for _item in _glob_result:
            _inputProducts.append(_item)
    if exists(_request_file_path):
        try:
            remove(_request_file_path)
        except OSError:
            print("Request file could not be created! " + _request_file_path + " is a directory. Now exiting...")
            exit(1)

    _request_file = open(_request_file_path, 'a')
    _request_file.write(_l3_xml_type_str)
    _request_file.write(_l3_xml_req_list_opener)
    _request_file.write(_l3_xml_req_type_opener)
    _request_file.write(get_l3_binning_init_block())
    _request_file.write(_l3_xml_req_type_closer)

    _request_file.write(_l3_xml_req_type_opener)
    _request_file.write(get_l3_binning_update_block())
    for item in _inputProducts:
        _request_file.write(_l3_xml_inp_prod_opener + item + _l3_xml_inp_prod_closer)
    _request_file.write(_l3_xml_req_type_closer)

    _request_file.write(_l3_xml_req_type_opener)
    _request_file.write(get_l3_binning_finalize_block())
    _request_file.write(_l3_xml_out_prod_opener)
    _request_file.write(_output_product_path)
    _request_file.write(_l3_xml_out_prod_closer)
    _request_file.write(_l3_xml_req_type_closer)

    _request_file.write(_l3_xml_req_list_closer)
    _request_file.close()

    _batch_file.write(_l3_binning_processor + ' ' + _request_file_path + '\n')

_batch_file.close()

#EOF