#!/usr/bin/env python3

__author__ = 'uwe'

from datetime import date, timedelta
from os import makedirs, system
from os.path import basename, exists, join
from sys import argv, exit
from conf.paths import inputBaseDir, dineof_inputDir, dineof_outputBaseDir, watermask_dim_file, watermask_nc_file, dineof_executable
from conf.DINEOFparams import variables, valid_pixel_threshold
import conf.DINEOFconstants as dc

import beampy
from netCDF4 import Dataset
import numpy as np
import jdcal


def printUsage():
    print("Usage: ", argv[0], " <date>")
    print("where date denotes a date in the format YYYYMMDD")
    print("like e.g. 20131220\n")
    exit(1)

def getBackDate(backDay):
    _back_date = date.today() - timedelta(backDay)
    return str(_back_date.year) + str(_back_date.month).zfill(2) + str(_back_date.day).zfill(2)

def getInputProductsList(delta_days):
    inputProductsList = []
    for day in range(-10 + delta_days, 365):
        _backDate = getBackDate(day)
        inputProduct = join(inputBaseDir , _backDate[:4] + '/' + 'cb_ns_' + _backDate + '_eo_bc_lat_lon_ecoham.dim')
        inputProductsList.append(inputProduct)
    inputProductsList.sort()
    return inputProductsList

def count_water_pixels(watermask_file, width, height):
    watermask_product = beampy.ProductIO.readProduct(watermask_file)
    water_band = watermask_product.getBand('land_water_fraction')
    waterpixel_count = 0
    for y in range(height):
        for x in range(width):
            if water_band.getSampleFloat(x, y) == 1: # for band math created
                waterpixel_count += 1
    if waterpixel_count == 0:
        print('Product location does not have any water pixels')
        exit(0)
    watermask_product.dispose()
    return waterpixel_count

def getDINEOFinputFileName(proc_date):
    return join(dineof_inputDir, "DINEOF_ECOHAM_tsm_input_" + proc_date + ".nc")

def getDINEOFoutputDir(proc_date):
    return join(dineof_outputBaseDir, "DINEOF_ECOHAM_tsm_" + proc_date + "/")

def getDINEOFoutputFileName(proc_date):
    dineof_outputDir = getDINEOFoutputDir(proc_date)
    return join(dineof_outputDir, "DINEOF_ECOHAM_tsm_output_" + proc_date + ".nc")

def getDINEOFconfFileName(proc_date):
    return join(dineof_inputDir, 'dineof_init_' + proc_date + '.conf')

def getUnlogOutputFileName(proc_date):
    dineof_outputDir = getDINEOFoutputDir(proc_date)
    return join(dineof_outputDir, "retrans_DINEOF_ECOHAM_tsm_output_" + proc_date + ".nc")

def writeDINEOFconfFile(proc_date):
    conf_filePath = getDINEOFconfFileName(proc_date)
    dineof_outputDir = join(dineof_outputBaseDir, "DINEOF_ECOHAM_tsm_" + proc_date + "/")
    if not exists(dineof_outputDir):
        makedirs(dineof_outputDir)
    with open(conf_filePath, 'a') as conf_file:
        conf_file.write(dc.headerPart)
        conf_file.write(dc.dataPart)
        conf_file.write("data = ['" + getDINEOFinputFileName(proc_date) + "#tsm_678_mean']\n")
        conf_file.write(dc.maskPart)
        conf_file.write("mask = ['" + watermask_nc_file + "#mask']\n")
        conf_file.write(dc.timePart)
        conf_file.write("time = '" + getDINEOFinputFileName(proc_date) + "#time'\n")
        conf_file.write(dc.nevPart)
        conf_file.write(dc.neiniPart)
        conf_file.write(dc.ncvPart)
        conf_file.write(dc.tolPart)
        conf_file.write(dc.nitemaxPart)
        conf_file.write(dc.toliterPart)
        conf_file.write(dc.recPart)
        conf_file.write(dc.eofPart)
        conf_file.write(dc.normPart)
        conf_file.write(dc.OutputPart)
        conf_file.write("Output = '" + getDINEOFoutputDir(proc_date) + "'\n")
        conf_file.write(dc.cvPart)
        conf_file.write(dc.resultsPart)
        conf_file.write("results = ['" + getDINEOFoutputFileName(proc_date) + "#tsm']\n")
        conf_file.write(dc.seedPart)
        conf_file.write(dc.cvpPart)
        conf_file.write(dc.csPart)
        conf_file.write(dc.eopfPart)

def makeDINEOFcube(proc_date, fileList):
    skippedFilesLogPath = dineof_inputDir + 'skipped_files_ECOHAM_' + proc_date + '.txt'
    skippedFilesLog = open(skippedFilesLogPath, 'a')
    startDate_date  = int(jdcal.gcal2jd(int(basename(fileList[0])[6:10]),int(basename(fileList[0])[10:12]),int(basename(fileList[0])[12:14]))[1])
    endDate_date = int(jdcal.gcal2jd(int(basename(fileList[-1])[6:10]),int(basename(fileList[-1])[10:12]),int(basename(fileList[-1])[12:14]))[1])
    dataset = Dataset(getDINEOFinputFileName(proc_date), mode='w', format='NETCDF3_CLASSIC') # NETCDF4
    earliestProduct = beampy.ProductIO.readProduct(fileList[0])
    width = earliestProduct.getSceneRasterWidth()
    height = earliestProduct.getSceneRasterHeight()
    dataset.createDimension("longitude", width)
    dataset.createDimension("latitude", height)
    dataset.createDimension("time", None)

    lon_variable = dataset.createVariable('longitude', np.float64, ('longitude'))
    lon_variable.units = 'degree'
    lon_variable.long_name = 'longitude coordinate of projection'
    lon_variable.standard_name = 'longitude'

    lat_variable = dataset.createVariable('latitude', np.float64, ('latitude'))
    lat_variable.units = 'degree'
    lat_variable.long_name = 'latitude coordinate of projection'
    lat_variable.standard_name = 'latitude'

    time_variable = dataset.createVariable('time', np.float32, ('time'))
    time_variable.units = 'days since 1970-1-1 0:0:0'
    time_variable.long_name = 'time'

    geo_pos = beampy.GeoPos.newGeoPos(0, 0)
    for x in range(width):
        earliestProduct.getGeoCoding().getGeoPos(beampy.PixelPos.newPixelPos(x + 0.5, 0), geo_pos)
        lon_variable[x] = geo_pos.getLon()

    for y in range(height):
        earliestProduct.getGeoCoding().getGeoPos(beampy.PixelPos.newPixelPos(0, y + 0.5), geo_pos)
        lat_variable[y] = geo_pos.getLat()

    for var in variables:
        dt = earliestProduct.getBand(var).getDataType()
        if dt <= 12:
            data_type = np.int32
        elif dt == 30:
            data_type = np.float32
        elif dt == 31:
            data_type = np.float64
        else:
            raise ValueError('cannot handle band of data type \'' + dt + '\'')

        variable = dataset.createVariable(var, data_type, ('time', 'latitude', 'longitude'), fill_value=9999.0)
        variable.missing_value = 9999.0
    waterpixel_count = count_water_pixels(watermask_dim_file, width, height)

    time_index = 0
    skipped_products_count = 0
    base_jd = jdcal.gcal2jd(1970, 1, 1)[1]
    data = np.zeros(width, dtype=np.float32)

    data[:] = 9999.0
    file_index = 0
    # loop over the date
    for date in range(startDate_date, endDate_date + 1):
        time_variable[time_index] = date - base_jd
        if file_index + 1 < len(fileList):
            current_date = int(jdcal.gcal2jd(int(basename(fileList[file_index+1])[6:10]),int(basename(fileList[file_index+1])[10:12]),int(basename(fileList[file_index+1])[12:14]))[1])
            if current_date <= date:
                file_index += 1

        input_file = fileList[file_index]
        print(date, input_file)

        skip_product = False
        print('Reading product \'' + input_file + '\'')
        current_path = input_file
        if exists(input_file):
            current_product = beampy.ProductIO.readProduct(input_file)
            if input_file == fileList[0]:
                last_valid_product_path = current_path


            for var in variables:
                current_band = current_product.getBand(var)
                valid_pixel_count = 0

                valid_mask = np.zeros(width, dtype=np.bool)
                for y in range(height):
                    current_band.readValidMask(0, y, width, 1, valid_mask)
                    for x in range(width):
                        if valid_mask[x]:
                            valid_pixel_count += 1

                enough_valid_pixels = valid_pixel_count / waterpixel_count > valid_pixel_threshold
                if not enough_valid_pixels:
                    skip_product |= True
                    skipped_products_count += 1
                break # stopping loop after first variable for performance reasons
        else:
            skip_product |= True
            skipped_products_count += 1

        if skip_product:
            ## for replacing skipped product with last available product
            print('Skipped product \'' + current_product.getName() + ' replaced by \'' + last_valid_product_path)
            skippedFilesLog.write('\n' + current_product.getName() + ' replaced by  ' + last_valid_product_path)
            current_product.dispose()
            if not last_valid_product_path:
                raise ValueError("first product is missing")
            current_product = beampy.ProductIO.readProduct(last_valid_product_path)
        for var in variables:
            current_band = current_product.getBand(var)
            target_variable = dataset.variables[var]
            for y in range(height):
                current_band.readPixelsFloat(0, y, width, 1, data)
                data = data.reshape((1, 1, width))
                data = np.log10(data)
                data = np.where(np.isneginf(data), 9999.0, data)
                data = np.where(np.isnan(data), 9999.0, data)
                target_variable[time_index : time_index + 1, y : y + 1, 0 : width] = data

        current_product.dispose()
        if not skip_product:
            last_valid_product_path = current_path
        time_index += 1

    print(skipped_products_count)
    dataset.close()
    skippedFilesLog.close()

def unlogDINEOFoutput(proc_date):
    ori_file = getDINEOFinputFileName(proc_date)    # this is the input to dineof prior to processing
    in_file  = getDINEOFoutputFileName(proc_date)   # this is the dineof output that we use as input for unlog-ing
    out_file = getUnlogOutputFileName(proc_date)    # this is the unlog-ed output file
    print(ori_file, exists(ori_file))

    # read input nc file and attribute variables names
    input_file = Dataset(in_file, mode='r')
    width = len(input_file.dimensions['dim001'])
    height = len(input_file.dimensions['dim002'])
    time_len = len(input_file.dimensions['dim003'])
    tsm = input_file.variables['tsm']

    # get geolocation from original file
    original_file = Dataset(ori_file, mode='r')
    lat_ori = original_file.variables['latitude']
    lon_ori = original_file.variables['longitude']
    time_ori = original_file.variables['time']

    # define output file
    dataset = Dataset(out_file, mode='w', format='NETCDF3_CLASSIC') # NETCDF4

    dataset.createDimension("longitude", width)
    dataset.createDimension("latitude", height)
    dataset.createDimension("time", time_len)

    lon_variable = dataset.createVariable('longitude', np.float64, ('longitude'))
    lon_variable.units = 'degree'
    lon_variable.long_name = 'longitude coordinate of projection'
    lon_variable.standard_name = 'longitude'

    lat_variable = dataset.createVariable('latitude', np.float64, ('latitude'))
    lat_variable.units = 'degree'
    lat_variable.long_name = 'latitude coordinate of projection'
    lat_variable.standard_name = 'latitude'

    time_variable = dataset.createVariable('time', np.float32, ('time'))
    time_variable.units = 'days since 1970-1-1 0:0:0'
    time_variable.long_name = 'time'

    target_tsm_variable = dataset.createVariable('tsm', np.float32, ('time', 'latitude', 'longitude'), fill_value=9999.0)
    target_tsm_variable.missing_value = 9999.0
    target_tsm_variable.units = 'g.m^-3 '
    target_tsm_variable.long_name = 'tsm'

    lat_variable[:] = lat_ori[:]
    lon_variable [:] = lon_ori[:]
    time_variable[:] = time_ori[:]

    # for bigger files:
    max_y = tsm.shape[2]-1
    max_x = tsm.shape[1]-1

    # for tsm
    for x in range(max_x):
        time_data = tsm[:, x:x+1,:]
        retrans_tsm = np.power(10, time_data)
        retrans_tsm = np.where(retrans_tsm > 200.0, 1.0, retrans_tsm)
        target_tsm_variable[:, x:x+1, :] = retrans_tsm

    input_file.close()
    original_file.close()
    dataset.close()


if __name__ == '__main__':
    argc = len(argv)
    if argc < 2:
        printUsage()
    else:
        proc_date = argv[1]
        print("Processing date: ", proc_date)

    writeDINEOFconfFile(proc_date)

    proc_year = int(proc_date[:4])
    proc_month = int(proc_date[4:6])
    proc_day = int(proc_date[6:])
    proc_datetime = date(proc_year, proc_month, proc_day)
    delta_days = (date.today() - proc_datetime).days

    inputProductsList = getInputProductsList(delta_days)
    #print(inputProductsList)
    makeDINEOFcube(proc_date, inputProductsList)
    dineof_call = dineof_executable + ' ' + getDINEOFconfFileName(proc_date)
    system(dineof_call)
    unlogDINEOFoutput(proc_date)
