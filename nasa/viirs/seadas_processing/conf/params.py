__author__ = 'uwe'

_processing = 'OC'
_site = 'ns'

# NorthSea, BalticSea boundary coordinates:
#           -w -15.0000 -s 47.0000 -e 15.0000 -n 64.0000

west_lon_nsea_bsea  = -15.00
east_lon_nsea_bsea  =  31.00
south_lat_nsea_bsea =  47.00
north_lat_nsea_bsea =  66.00

# L2 parameter file parts
l2gen_io_params = '# PRIMARY INPUT OUTPUT FIELDS\n'

l2gen_suite_params = '# SUITE\n'
l2gen_suite_params += 'suite=OC\n'

l2gen_l2_params = '# PRODUCTS\n'
l2gen_l2_params += 'l2prod=BT_10763 BT_8550 Kd_490 Kd_vvv_lee Rrs_745 Rrs_862 Rrs_vvv Zeu_lee angstrom aot_862 '
l2gen_l2_params += 'cdom_index chlor_a ipar par pic poc qual_sst rhot_2257 sst\n'

l2gen_anc_params = '# ANCILLARY INPUTS  Default = climatology (select \'Get Ancillary\' to download ancillary files)\n'


# # PRIMARY INPUT OUTPUT FIELDS
# ifile=/fs14/EOservices/InputPool/VIIRS/NASA/L1A/2014/06/08/V2014159110136.L1A_NPP/SVM01_npp_d20140608_t1101376_e1103018_b13536_obpg_ops.h5
# geofile=/fs14/EOservices/InputPool/VIIRS/NASA/L1A/2014/06/08/V2014159110136.L1A_NPP/GMTCO_npp_d20140608_t1101376_e1103018_b13536_obpg_ops.h5
# ofile=/fs14/EOservices/InputPool/VIIRS/NASA/L1A/2014/06/08/V2014159110136.L1A_NPP/V2014159110137.L2_NPP
#
# # SUITE
# suite=OC
#
# # PRODUCTS
# l2prod=BT_10763 BT_8550 Kd_490 Kd_vvv_lee Rrs_745 Rrs_862 Rrs_vvv Zeu_lee angstrom aot_862 cdom_index chlor_a ipar par pic poc qual_sst rhot_2257 sst
#
# # ANCILLARY INPUTS  Default = climatology (select 'Get Ancillary' to download ancillary files)
# icefile=/home/uwe/tools/seadas/7.0.2/ocssw/run/var/anc/2014/159/N201415900_SEAICE_NSIDC_24h.hdf
# met1=/home/uwe/tools/seadas/7.0.2/ocssw/run/var/anc/2014/159/S201415906_NCEP.MET
# met2=/home/uwe/tools/seadas/7.0.2/ocssw/run/var/anc/2014/159/S201415912_NCEP.MET
# met3=/home/uwe/tools/seadas/7.0.2/ocssw/run/var/anc/2014/159/S201415912_NCEP.MET
# ozone1=/home/uwe/tools/seadas/7.0.2/ocssw/run/var/anc/2014/158/N201415800_O3_TOMSOMI_24h.hdf
# ozone2=/home/uwe/tools/seadas/7.0.2/ocssw/run/var/anc/2014/159/N201415900_O3_TOMSOMI_24h.hdf
# ozone3=/home/uwe/tools/seadas/7.0.2/ocssw/run/var/anc/2014/159/N201415900_O3_TOMSOMI_24h.hdf
# sstfile=/home/uwe/tools/seadas/7.0.2/ocssw/run/var/anc/2014/159/N2014159_SST_OIV2AV_24h.nc


