#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: zip_dimap_files.py

from glob import glob
from os import chdir,remove
from os.path import basename, exists
from sys import argv,exit,stdout
from time import localtime, strftime
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from configparser import ConfigParser

baseDir = '/home/uwe/tools/'
configDir  = baseDir + 'config/'

configFilePath = configDir + 'zipDirConfig.ini'
config = ConfigParser()
config.read(configFilePath)

num_dirs = int(config.get("meta", "dirs"))
src_dirs = []
for dir_index in range(num_dirs):
    src_dirs.append(config.get("srcDirectories", "srcDir"+ str(dir_index)))

def printUsage():
    print("Usage: zip_dimap_files \'dir_index\'")
    print("where dir_index is an integer value specifying the index of the directory to process:")
    for dir_index in range(num_dirs):
        print(dir_index, ": ", src_dirs[dir_index]) 

try:
    argc=len(argv)
    if (argc == 1):          # the program was called without parameters
        print("\'dir_index\' specifier is missing!\n")
        exit(1)
    else:
        try:
            dir_index = int(argv[1])
            if not dir_index in range(num_dirs):
                print("\'dir_index\' must be in the range between 0 and " + str(num_dirs-1))
                exit(1)
        except ValueError:
            print("\'dir_index\' must be of type integer!\n")
            exit(1)        
except:
    printUsage()
    print("Error in parameters. Now exiting...")
    exit(1)    


print("\n****************************************")
print(" Script \'zip_dimap_files.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("****************************************\n")


def zip_them(str, data_content):
    dimap_file     = str + 'dim'
    dimap_data_dir = str + 'data'
    zip_file_name  = 'zipped/' + str + 'zip'
    if not exists(zip_file_name):
        dest_zip_file = ZipFile(zip_file_name, 'w')
        print("\nZip file created: ", zip_file_name, ".")
        data_content = glob(dimap_data_dir + '/*')   # find content inside the data dir
        zip_info = ZipInfo(dimap_data_dir + '/')     # create the directory inside
        zip_info.external_attr = 0o775 << 16         # the zipfile, set permissions for the directory
        zip_info.create_system = 3                   # tell the zip file that we are on UNIX
        dest_zip_file.writestr(zip_info, '')          # write the info to it
        print("Writing to zip: ", dimap_file, "...")
        dest_zip_file.write(dimap_file, dimap_file, ZIP_DEFLATED)  # write the dimap file into
        for item in data_content:
            print("Writing to zip: ", item, "...")
            dest_zip_file.write(item, item, ZIP_DEFLATED)          # write all dimap data to the zip file
        dest_zip_file.close()
    else:
        print("Zip file ", zip_file_name, " exists already; skipping.")

src_dir = src_dirs[dir_index]
chdir(src_dir)      # Important to change dir into that directory; struggling with leading paths in zip files is awesome

print("\n\nZipping DIMAP products in ", src_dir, "...\n\n")

dimap_file_paths = glob('*.dim')        # find all dimap files
dimap_file_paths.sort()
dimap_data_dirs  = glob('*.data')       # find all data directories
dimap_data_dirs.sort()

dimap_file_paths_array_size = len(dimap_file_paths)
dimap_data_dirs_array_size  = len(dimap_data_dirs)
print(dimap_file_paths_array_size, dimap_data_dirs_array_size)

zip_file_names = []
min_array_size = min(dimap_file_paths_array_size, dimap_data_dirs_array_size)
iter_range = list(range(min_array_size))

for counter in iter_range:
    dimap_file_str = dimap_file_paths[counter][0:len(dimap_file_paths[counter])-3]
    dimap_data_str = dimap_data_dirs[counter][0:len(dimap_data_dirs[counter])-4]
    for counter2 in iter_range:
        dimap_data_str = dimap_data_dirs[counter2][0:len(dimap_data_dirs[counter2])-4]
        if (dimap_file_str == dimap_data_str):
            print(dimap_file_str, dimap_data_str)
            data_content = glob(dimap_data_dirs[counter] + '/*')
            zip_them(dimap_data_str, data_content)
        else:
            continue


print("\n***************************************")
print(" Script \'zip_dimap_files.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("***************************************\n")
# EOF
