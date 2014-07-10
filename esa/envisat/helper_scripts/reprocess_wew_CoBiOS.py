#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: reprocess_wew_WAQS_childs.py

from os import system, listdir, remove
from os.path import exists
from sys import argv, exit
from time import localtime, strftime

def printUsage():
    print("Usage: reprocess_wew_WAQS_childs.py start_date end_date")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date")
    

try:
    argc=len(argv)
    if (argc < 3):          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        exit(1)
    else:                   # we have also received parameters
        start_date = argv[1]
        end_date   = argv[2]
        if (int(start_date) <= int(end_date) ):
            # do something
            print("\nReprocessing products from " + start_date + " to " + end_date + "...\n")
        else:               # incorrect parameters
            print("Wrong parameters!")
            printUsage()
            exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    exit(1)    


print("\n**************************************************")
print(" Script \'reprocess_wew_WAQS_childs.py\' at work... ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("**************************************************\n")

thetime   = localtime()
year_str  = str(thetime[0]) + "/"

# Verzeichnisse
# baseDir = '/fs14/EOservices/Repositories/MERIS/RR/WAQSrepository/'
# smileCorrSrcDir  = baseDir + start_date[0:4] + '/'
# smileCorrDestDir = '/fs14/EOservices/InputPool/MERIS/RR/waqs_child_temp/smile_corrected/'

wewSrcDir = '/fs14/EOservices/OutputPool/MERIS/RR/CoBiOS/L1/'
wewDestDir = '/fs14/EOservices/OutputPool/MERIS/RR/CoBiOS/FUB/' #'/fs14/EOservices/OutputPool/MERIS/RR/WAQS-WeW/Level2/'

# print '\n\n###################################################################'
# print '#                     smile correction part'
# print '###################################################################\n\n'

# # tool config
# smile_corr_home   = '/home/uwe/tools/smile_corr/'
# smile_corr_script = smile_corr_home + 'meris-smile.sh'
# smile_corr_conf   = smile_corr_home + 'smile_corr_request.xml'

# # konstante xml-bausteine fuer requests
# smile_corr_request_skeleton_1 =  '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n<RequestList>\n'
# smile_corr_request_skeleton_1 += '    <Request type=\"SMILE_CORRECTION\">\n'
# smile_corr_request_skeleton_1 += '        <Parameter name=\"output_format\" value=\"BEAM-DIMAP\" />\n'
# smile_corr_request_skeleton_1 += '        <Parameter name=\"include_all\" value=\"true\" />\n'
# smile_corr_request_skeleton_1 += '        <Parameter name=\"bands\" value=\"radiance_1,radiance_2,radiance_3,radiance_4,radiance_5,radiance_6,radiance_7,radiance_8,radiance_9,radiance_10,radiance_11,radiance_12,radiance_13,radiance_14,radiance_15\" />\n'
# smile_corr_request_skeleton_1 += '        <Parameter name=\"log_prefix\" value=\"smile_corr\" />\n'
# smile_corr_request_skeleton_1 += '        <Parameter name=\"log_to_output\" value=\"false\" />\n'
# smile_corr_input_opener       =  '        <InputProduct file=\"'
# smile_corr_input_delimiter    = '\" />\n'
# smile_corr_output_opener      =  '        <OutputProduct file=\"'
# smile_corr_output_delimiter   = '\" format=\"BEAM-DIMAP\" />\n'
# smile_corr_request_closer     = '    </Request>\n</RequestList>\n'

# for date_int in range(int(start_date), int(end_date)+1):
    # date = str(date_int)
    # print date
    # # Inputliste holen
    # smile_corr_src_list  = listdir(smileCorrSrcDir)
    # smile_corr_list_size = len(smile_corr_src_list)
    
    # # Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 oder Level2 sind:
    # for a in range(smile_corr_list_size):
        # for item in smile_corr_src_list:
            # if not item.startswith('MER') or item.startswith('MER_RR__0') or item.startswith('MER_RR__2') or item.endswith('.dim') or item.find(date)<0:
                # print "Removing " + item + " from list."
                # smile_corr_src_list.remove(item)
    # print smile_corr_src_list
    # #exit(1)
    # smile_corr_list_size = len(smile_corr_src_list)
    # if smile_corr_list_size == 0:
        # print "Nothing to do here. Now quitting."
        # exit(1)
    
    # for meris_file in smile_corr_src_list:    
        # # MER_RR__1PNPDE20051126_053458_000011252042_00463_19555_0425.N1
        # # 0         1         2         3         4         5         6
        # # 01234567890123456789012345678901234567890123456789012345678901   
    
        # smile_corr_input_filename  = smileCorrSrcDir + meris_file
        # smile_corr_output_filename = smileCorrDestDir + meris_file[0:len(meris_file)-2] + 'dim'
        
        # smile_corr_request = smile_corr_request_skeleton_1 + smile_corr_input_opener + smile_corr_input_filename + smile_corr_input_delimiter + smile_corr_output_opener + smile_corr_output_filename + smile_corr_output_delimiter + smile_corr_request_closer
    
        # # Requestfile soll noch nicht existieren:
        # if exists(smile_corr_conf):
            # remove(smile_corr_conf)
        
        # # Erst jetzt wird es erzeugt:
        # smile_corr_requestfile = open(smile_corr_conf, 'a')
        # smile_corr_requestfile.write(smile_corr_request)
        # smile_corr_requestfile.close()
    
        # smile_corr_command = smile_corr_script + " " + smile_corr_conf
        # print smile_corr_command
        # print "Processing file " + meris_file + " ..."
        # system(smile_corr_command)


print('\n\n###################################################################')
print('#                     water processing part')
print('###################################################################\n\n')

# tool config
wewHome   = '/home/uwe/tools/wew_water/'
wewScript = wewHome + 'wew-water.sh'
wewConf   = wewHome + 'water1.1.xml'

# konstante xml-bausteine fuer requests
wew_request_skeleton_1 =  "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n<RequestList>\n"
wew_request_skeleton_1 += "    <Request type=\"WATER\">\n"
wew_request_skeleton_1 += "        <Parameter name=\"output_format\" value=\"BEAM-DIMAP\" />\n"
wew_request_skeleton_1 += "        <Parameter name=\"Normout\" value=\"false\" />\n"
wew_request_skeleton_1 += "        <Parameter name=\"Extout\" value=\"true\" />\n"
wew_request_skeleton_1 += "        <Parameter name=\"caseI\" value=\"false\" />\n"
wew_request_skeleton_1 += "        <Parameter name=\"caseII\" value=\"true\" />\n"
wew_request_skeleton_1 += "        <Parameter name=\"ozone_norm\" value=\"true\" />\n"
wew_request_skeleton_1 += "        <Parameter name=\"ray_corr\" value=\"false\" />\n"
wew_request_skeleton_1 += "        <InputProduct URL=\"file:"
wew_input_delimiter    =                                    "\" />\n"
wew_request_skeleton_2  =  "        <OutputProduct URL=\"file:"
wew_output_delimiter   =              "\" format=\"BEAM-DIMAP\" />\n"
wew_request_skeleton_3  =  "    </Request>\n"
wew_request_skeleton_3  += "</RequestList>\n"

for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)
    print(date)
    # Inputliste holen
    src_list = listdir(wewSrcDir)
    list_size = len(src_list)
    
    # Liste bereinigen um die Dateien, die keine MERIS-Produkte oder Level0 oder Level2 sind:
    for a in range(list_size):
        for item in src_list:
            if not item.startswith('RadCor') or item.startswith('MER') or item.startswith('MER_RR__0') or item.startswith('MER_RR__2') or item.endswith('.data') or item.find(date)<0:
                src_list.remove(item)
    print(src_list)
    # Jetzt geht's los:
    for meris_file in src_list:    
        # MER_RR__1PNPDE20051126_053458_000011252042_00463_19555_0425.N1
        # 0         1         2         3         4         5         6
        # 01234567890123456789012345678901234567890123456789012345678901   
        acquisition_time = meris_file[21:36]
        orbit = meris_file[56:61]
	print(acquisition_time)
	print(orbit)
        
        wew_input_filename = wewSrcDir + meris_file
        wew_output_filename= wewDestDir + "MER_RR_" + acquisition_time + "_" + orbit + "_fw.dim"
        
        request = wew_request_skeleton_1 + wew_input_filename + wew_input_delimiter + wew_request_skeleton_2 + wew_output_filename + wew_output_delimiter + wew_request_skeleton_3
    
        # Requestfile soll noch nicht existieren:
        if exists(wewConf):
            remove(wewConf)
        
        # Erst jetzt wird es erzeugt:
        requestfile = open(wewConf, 'a')
        requestfile.write(request)
        requestfile.close()
    
        wewCommand = wewScript + " " + wewConf
        print("\nProcessing file " + meris_file + " ...\n")
        system(wewCommand)

        ##############################################
        #  here we are removing the input product !! #
        ##############################################
        
#        input_file_components = wew_input_filename[0:len(wew_input_filename)-2] + '*'
#        try:
#            print 'Removing ' + input_file_components#
#            system('rm -r ' + input_file_components)
#        except:
#            print input_file_components + ' could not be removed!'


print("\n*************************************************")
print(" Script \'reprocess_wew_WAQS_childs.py\' finished. ")
print(" Date: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("*************************************************\n")

# EOF
