__author__ = 'carole'

from os import listdir, makedirs, remove, system
from os.path import exists
from sys import argv
from shutil import rmtree
from glob import glob


from bc.eodata.beam_processing.conf.demarine_conf import region, supersampling, num_rows, product_format
from bc.eodata.beam_processing.conf.demarine_conf import output_Binned_Data, output_format
from nasa.modis.seadas_processing.shared.utilities import getDOY, ensureTrailingSlash, exit_on_empty_list
from bc.eodata.beam_processing.conf.demarine_paths import modisL2_TSMBasePath_ns, modisL2_TSMBasePath_bs,modisL3_TSMBasePath
from bc.eodata.beam_processing.conf.demarine_conf import gptProcessor, l3binningDir




def printUsage():
    print("Usage: ", argv[0], "<date>")
    print("where date is a string representing the date to process,")
    print("e.g. 20120607 for June 7, 2012.")

if len(argv) != 2:
    printUsage()
    exit(1)

back_date = argv[1]
if len(back_date)!=8:
    print("****************************")
    print("* date parameter malformed *")
    print("****************************")
    printUsage()
    exit(1)

_year  = back_date[:4]
_month = back_date[4:6]
_day   = back_date[6:]
_doy   = getDOY(_year, _month, _day)
print("Processing date " + back_date + " (DOY = " + str(_doy)+ ").")

modisL2_TSMPath_ns  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL2_TSMBasePath_ns  + _year) + _month) + _day)
modisL2_TSMPath_bs  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL2_TSMBasePath_bs  + _year) + _month) + _day)
modisL3_TSMPath  = ensureTrailingSlash(ensureTrailingSlash(ensureTrailingSlash(modisL3_TSMBasePath  + _year) + _month) + _day)

print(modisL2_TSMPath_ns, modisL2_TSMPath_bs, modisL3_TSMPath)

for _path in [modisL3_TSMPath]:
    if not exists(_path):
        print("Making directory: ", _path, " ...")
        makedirs(_path)

srcList_ns = glob(modisL2_TSMPath_ns + '*.dim')
srcList_bs = glob(modisL2_TSMPath_bs + '*.dim')

srcList = srcList_ns + srcList_bs
srcList.sort()
Source_Products = ",".join(srcList)
print(srcList)
print(Source_Products)


outputProductPath = modisL3_TSMPath + 'MODISA_DeM' + '_' + back_date + '.dim'

#l3binningScript = '/Applications/beam-4.10/bin/binning.command'
#l3binningDatabase = '/FastBuffer/temp/l3_large_' + str(_year) + str(_doy) + '.bindb'
#l3binningConf = '/FastBuffer/temp/l3_large_' + str(_year) + str(_doy) + '.conf'
l3binningScript = gptProcessor
l3binningDatabase = l3binningDir + 'l3_large_' + str(_year) + str(_doy) + '.bindb'
l3binningConf = l3binningDir + 'l3_large_' + str(_year) + str(_doy) + '.xml'
if exists(l3binningDatabase):
    rmtree(l3binningDatabase)



request_init_block = ' <graph id="binningGraph">\n'

request_init_block += ' <version>1.0</version>\n'

request_init_block += ' <node id="binningNode">\n'
request_init_block += ' <operator>Binning</operator>\n'
request_init_block += ' <parameters>\n'
request_init_block += ' <sourceProductPaths>'+  Source_Products +'</sourceProductPaths>\n'
request_init_block += ' <sourceProductFormat>'+ product_format +'</sourceProductFormat>\n'
request_init_block += ' <region>'+ region +'</region>\n'
request_init_block += ' <outputBinnedData>'+ output_Binned_Data +'</outputBinnedData>\n'
request_init_block += ' <outputTargetProduct>true</outputTargetProduct>\n'

request_binning_block = ' <numRows>'+ str(num_rows) +'</numRows>\n'
request_binning_block += ' <superSampling>'+ str(supersampling) +'</superSampling>\n'
request_binning_block += ' <maskExpr>!l2_flags.PRODWARN AND NOT l2_flags.HISATZEN AND NOT ' \
                         '(l2_flags.STRAYLIGHT and not  l2_flags.LAND and aot_869 &gt; 0.1)</maskExpr>\n'
request_binning_block += ' <variables>\n'
request_binning_block += ' <variable>\n'
request_binning_block += ' <name>CHL</name>\n'
request_binning_block += ' <expr>fneq(chlor_a,-32767.0) AND NOT l2_flags.CHLFAIL AND NOT l2_flags.CHLWARN AND NOT l2_flags.PRODWARN ?chlor_a:NaN</expr>\n'
request_binning_block += ' </variable>\n'
request_binning_block += ' <variable>\n'
request_binning_block += ' <name>TSM</name>\n'
request_binning_block += ' <expr>tsm_678 &gt; 0.0 ?tsm_678:NaN</expr>\n'
request_binning_block += ' </variable>\n'
request_binning_block += ' <variable>\n'
request_binning_block += ' <name>SST2</name>\n'
request_binning_block += ' <expr>qual_sst == 0? sst : NaN or qual_sst == 1 ? sst : NaN</expr>\n'
request_binning_block += ' </variable>\n'
request_binning_block += ' <variable>\n'
request_binning_block += ' <name>PIC2</name>\n'
request_binning_block += ' <expr>pic &gt;0.0 ? pic : NaN</expr>\n'
request_binning_block += ' </variable>\n'
request_binning_block += ' <variable>\n'
request_binning_block += ' <name>POC2</name>\n'
request_binning_block += ' <expr>poc &gt;0.0 ? poc : NaN</expr>\n'
request_binning_block += ' </variable>\n'
request_binning_block += ' <variable>\n'
request_binning_block += ' <name>KdPAR2</name>\n'
request_binning_block += ' <expr>((fneq(Kd_412_lee,-6.553399834447191) and fneq(Kd_443_lee,-6.553399834447191) and  fneq(Kd_469_lee,-6.553399834447191) and fneq(Kd_488_lee,-6.553399834447191) and fneq(Kd_531_lee,-6.553399834447191) and fneq(Kd_547_lee,-6.553399834447191) and fneq(Kd_555_lee,-6.553399834447191) and fneq(Kd_645_lee,-6.553399834447191) and fneq(Kd_667_lee,-6.553399834447191) and fneq(Kd_678_lee,-6.553399834447191))) and !nan(KdPAR)? KdPAR:NaN</expr>\n'
request_binning_block += ' </variable>\n'
request_binning_block += ' <variable>\n'
request_binning_block += ' <name>PAR2</name>\n'
request_binning_block += ' <expr>par &gt; 0.0? par : NaN</expr>\n'
request_binning_block += ' </variable>\n'
request_binning_block += ' </variables>\n'
request_binning_block += ' <aggregators>\n'
request_binning_block += ' <aggregator>\n'
request_binning_block += ' <type>AVG</type>\n'
request_binning_block += ' <varName>CHL</varName>\n'
request_binning_block += ' <outputCounts>true</outputCounts>\n'
request_binning_block += ' </aggregator>\n'
request_binning_block += ' <aggregator>\n'
request_binning_block += ' <type>AVG</type>\n'
request_binning_block += ' <varName>TSM</varName>\n'
request_binning_block += ' <outputCounts>true</outputCounts>\n'
request_binning_block += ' </aggregator>\n'
request_binning_block += ' <aggregator>\n'
request_binning_block += ' <type>AVG</type>\n'
request_binning_block += ' <varName>PIC2</varName>\n'
request_binning_block += ' <outputCounts>true</outputCounts>\n'
request_binning_block += ' </aggregator>\n'
request_binning_block += ' <aggregator>\n'
request_binning_block += ' <type>AVG</type>\n'
request_binning_block += ' <varName>POC2</varName>\n'
request_binning_block += ' <outputCounts>true</outputCounts>\n'
request_binning_block += ' </aggregator>\n'
request_binning_block += ' <aggregator>\n'
request_binning_block += ' <type>AVG</type>\n'
request_binning_block += ' <varName>SST2</varName>\n'
request_binning_block += ' <outputCounts>true</outputCounts>\n'
request_binning_block += ' </aggregator>\n'
request_binning_block += ' <aggregator>\n'
request_binning_block += ' <type>AVG</type>\n'
request_binning_block += ' <varName>KdPAR2</varName>\n'
request_binning_block += ' <outputCounts>true</outputCounts>\n'
request_binning_block += ' </aggregator>\n'
request_binning_block += ' <aggregator>\n'
request_binning_block += ' <type>AVG</type>\n'
request_binning_block += ' <varName>PAR2</varName>\n'
request_binning_block += ' <outputCounts>true</outputCounts>\n'
request_binning_block += ' </aggregator>\n'
request_binning_block += ' </aggregators>\n'


request_update_block = ' <outputType>Product</outputType>\n'
request_update_block += ' <outputFile>'+ outputProductPath +'</outputFile>\n'
request_update_block += ' <outputFormat>'+ output_format +'</outputFormat>\n'
request_update_block += ' </parameters>\n'
request_update_block += ' </node>\n'
request_update_block += ' </graph>\n'

# Assembling request XML:


request = request_init_block
request += request_binning_block
request += request_update_block

# for item in srcList:
#     request += input_prefix
#     request += item
#     request += input_delimiter
#
# request += block_close
# request += request_finalize_block
# request += outputProductPath
# request += request_closer

if exists(l3binningConf):
    remove(l3binningConf)

# Jetzt wird das Requestfile erzeugt:

requestfile = open(l3binningConf, 'a')
requestfile.write(request)
requestfile.close()

# Binning starten
l3binningCommand = l3binningScript + " " + l3binningConf
print(l3binningCommand)
print("Processing L3...")
system(l3binningCommand)
