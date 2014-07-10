#!/usr/bin/env python3

skipped_file = open(os.path.join(output_directory,skipped_file_filename),'a')
input_files = [f for f in sorted(os.listdir(input_directory)) if os.path.isfile(os.path.join(input_directory, f)) and os.path.basename(f).endswith('.dim')]
startDate_date  = int(jdcal.gcal2jd(int(input_files[0][6:10]),int(input_files[0][10:12]),int(input_files[0][12:14]))[1])
endDate_date = int(jdcal.gcal2jd(int(input_files[-1][6:10]),int(input_files[-1][10:12]),int(input_files[-1][12:14]))[1]) + 10

mode = 'w'
dataset = Dataset(os.path.join(output_directory,filename), mode=mode, format='NETCDF3_CLASSIC') # NETCDF4

some_product = beampy.ProductIO.readProduct(os.path.join(input_directory, input_files[0]))

width = some_product.getSceneRasterWidth()
height = some_product.getSceneRasterHeight()



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
    some_product.getGeoCoding().getGeoPos(beampy.PixelPos.newPixelPos(x + 0.5, 0), geo_pos)
    lon_variable[x] = geo_pos.getLon()

for y in range(height):
    some_product.getGeoCoding().getGeoPos(beampy.PixelPos.newPixelPos(0, y + 0.5), geo_pos)
    lat_variable[y] = geo_pos.getLat()

for var in variables:
    dt = some_product.getBand(var).getDataType()
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

waterpixel_count = count_water_pixels(watermask_file)

time_index = 0
skipped_products_count = 0
base_jd = jdcal.gcal2jd(1970, 1, 1)[1]
data = np.zeros(width, dtype=np.float32)

data[:] = 9999.0
file_index = 0
# loop over the date
for date in range(startDate_date, endDate_date+1):
    time_variable[time_index] = date - base_jd
    if file_index + 1 < len(input_files):
        current_date = int(jdcal.gcal2jd(int(input_files[file_index+1][6:10]),int(input_files[file_index+1][10:12]),int(input_files[file_index+1][12:14]))[1])

        if current_date <= date:
            file_index += 1


    input_file = input_files[file_index]
    print(date, input_file)

    print('Reading product \'' + input_file + '\'')
    current_path = os.path.join(input_directory, input_file)
    current_product = beampy.ProductIO.readProduct(current_path)
    if '20130101' in input_file:
        last_valid_product_path = current_path
    current_product_jd = jdcal.gcal2jd(int(input_file[6:10]),int(input_file[10:12]),int(input_file[12:14])) # for 'cb_ns_20041225_eo_bc_lat_lon_ecoham.data

    skip_product = False

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

    if skip_product:
        ## for replacing skipped product with last available product
        print('Skipped product \'' + current_product.getName() + ' replaced by \'' + last_valid_product_path)
        skipped_file.write('\n' + current_product.getName() + ' replaced by  ' + last_valid_product_path)
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
            target_variable[time_index : time_index + 1, y : y + 1, 0 : width] = data

    current_product.dispose()
    if not skip_product:
        last_valid_product_path = current_path
    time_index += 1

print(skipped_products_count)
dataset.close()
skipped_file.close()
