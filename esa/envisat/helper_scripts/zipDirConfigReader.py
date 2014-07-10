#!/usr/bin/env python
# -*- coding: latin-1 -*
from configparser import ConfigParser

configDir  ='/home/uwe/tools/config/'
configFilePath = configDir + 'zipDirConfig.ini'
config = ConfigParser()
config.read(configFilePath)

num_dirs  = int(config.get("ematter", "dirs"))
src_dirs  = []
dest_dirs = []
for dir_index in range(num_dirs):
    src_dirs.append(config.get("srcDirectories", "srcDir"+ str(dir_index)))
    src_dirs[dir_index] += "zipped/"
    dest_dirs.append(config.get("destDirectories", "destDir"+ str(dir_index)))

print()
print("srcDirectories:")
print(src_dirs)
print()
print("destDirectories:")
print(dest_dirs)

#EOF