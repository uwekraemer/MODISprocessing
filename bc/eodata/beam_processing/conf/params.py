#!/usr/bin/env python3
__author__ = 'uwe'

west_lon_nos = "-5.0"           # lon_min
north_lat_nos = "63.0"          # lat_max
east_lon_nos = "13.0"           # lon_max
south_lat_nos = "49.0"          # lat_min
nos_polygon = "\"POLYGON(({0} {1}, {2} {3}, {4} {5}, {6} {7}, {8} {9}))\"".format(west_lon_nos, south_lat_nos,
                                                                                  east_lon_nos, south_lat_nos,
                                                                                  east_lon_nos, north_lat_nos,
                                                                                  west_lon_nos, north_lat_nos,
                                                                                  west_lon_nos, south_lat_nos)
west_lon_bas = "9.0"            # lon_min
north_lat_bas = "66.0"          # lat_max
east_lon_bas = "31.0"           # lon_max
south_lat_bas = "53.0"          # lat_min
bas_polygon = "\"POLYGON(({0} {1}, {2} {3}, {4} {5}, {6} {7}, {8} {9}))\"".format(west_lon_bas, south_lat_bas,
                                                                                  east_lon_bas, south_lat_bas,
                                                                                  east_lon_bas, north_lat_bas,
                                                                                  west_lon_bas, north_lat_bas,
                                                                                  west_lon_bas, south_lat_bas)


