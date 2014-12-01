__author__ = 'uwe'

_processing = 'STD'
# _processing = 'NASA'

_site = 'NorthSeaBalticSea'
#_site = 'NorthSea'
# _site = 'BalticSea'

# NorthSea, BalticSea boundary coordinates:
#           -w -15.0000 -s 47.0000 -e 15.0000 -n 64.0000

west_lon_nsea_bsea  = -15.00
east_lon_nsea_bsea  =  32.00
south_lat_nsea_bsea =  47.00
north_lat_nsea_bsea =  66.00

# L2 processing parameters
l2gen_const_params = ''
l2gen_const_params += 'l2prod1=aot_869 angstrom Rrs_vvv chlor_a Kd_490 pic poc cdom_index ipar nflh par sst qual_sst BT_8550 BT_11000 rhot_2130 Zeu_lee Kd_vvv_lee\n'
#l2gen_const_params += 'l2prod1=aot_869 angstrom Rrs_vvv chlor_a chl_oc2 chl_oc3 chl_giop chl_gsm Kd_490 Kd_490_morel Kd_PAR_morel pic poc cdom_index ipar nflh par sst qual_sst BT_8550 BT_11000 rhot_2130 Zeu_lee Zeu_morel Zsd_morel Zhl_morel Kd_vvv_lee\n'
#l2gen_const_params += 'l2prod1=aot_vvv a_vvv bb_vvv\n'

l2gen_const_params += 'spixl=       1\n'
l2gen_const_params += 'epixl=      -1\n'
l2gen_const_params += 'dpixl=       1\n'
l2gen_const_params += 'sline=       1\n'
l2gen_const_params += 'eline=      -1\n'
l2gen_const_params += 'dline=       1\n'
l2gen_const_params += 'ctl_pt_incr=       1\n'
l2gen_const_params += 'proc_ocean=       1\n'
l2gen_const_params += 'atmocor=       1\n'
l2gen_const_params += 'proc_land=       1\n'
l2gen_const_params += 'proc_sst=       1\n'
l2gen_const_params += 'resolution=    1000\n'
l2gen_const_params += 'gas_opt=      15\n'
l2gen_const_params += 'pol_opt=       3\n'
if _processing == 'STD':
    l2gen_const_params += 'aer_opt=      -3\n' # SeaDAS standard AC
else:
    l2gen_const_params += 'aer_opt=      -10\n' # SeaDAS MUMM AC
l2gen_const_params += 'aermodmin=      -1\n'
l2gen_const_params += 'aermodmax=      -1\n'
l2gen_const_params += 'aermodrat=      0.00000\n'
l2gen_const_params += 'mumm_alpha=      1.94500\n'
l2gen_const_params += 'mumm_gamma=      1.00000\n'
l2gen_const_params += 'mumm_epsilon=      1.00000\n' # SeaDAS MUMM AC
l2gen_const_params += 'aer_rrs_short=     -1.00000\n'
l2gen_const_params += 'aer_rrs_long=     -1.00000\n'
l2gen_const_params += 'aer_swir_short=    1240\n'
l2gen_const_params += 'aer_swir_long=    2130\n'
l2gen_const_params += 'aer_wave_short=     748\n'
l2gen_const_params += 'aer_wave_long=     869\n'
l2gen_const_params += 'aer_iter_max=      10\n'
l2gen_const_params += 'brdf_opt=       7\n'
l2gen_const_params += 'iop_opt=       0\n'
l2gen_const_params += 'glint_opt=       1\n'
l2gen_const_params += 'outband_opt=       2\n'
l2gen_const_params += 'filter_opt=       1\n'
l2gen_const_params += 'filter_file=$OCDATAROOT/modisa/msl12_filter.dat\n'
l2gen_const_params += 'no2file=$OCDATAROOT/common/no2_climatology.hdf\n'
l2gen_const_params += 'land=$OCDATAROOT/common/landmask.dat\n'
l2gen_const_params += 'water=$OCDATAROOT/common/watermask.dat\n'
l2gen_const_params += 'gain=[0.9731,0.9910,1.0132,0.9935,1.0002,0.9994,1.0012,1.0280,0.9996,0.9998,0.9989,1.0254,1.0, 1.0, 1.0, 1.0]\n'
l2gen_const_params += 'offset=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]\n'
l2gen_const_params += 'albedo=    0.0270000\n'
l2gen_const_params += 'rhoamin=  0.000200000\n'
l2gen_const_params += 'qaa_adg_s=    0.0150000\n'
l2gen_const_params += 'chloc2_wave=[488,547]\n'
l2gen_const_params += 'chloc2_coef=[0.2500,-2.4752,1.4061,-2.8237, 0.5405]\n'
l2gen_const_params += 'chloc3_wave=[443,488,547]\n'
l2gen_const_params += 'chloc3_coef=[0.2424,-2.7423,1.8017, 0.0015,-1.2280]\n'
l2gen_const_params += 'chloc4_wave=[]\n'
l2gen_const_params += 'chloc4_coef=[]\n'
l2gen_const_params += 'chlclark_wave=[443,488,547]\n'
l2gen_const_params += 'chlclark_coef=[0.789273,-3.925523,11.637764,-27.157997,27.936958,-10.398587]\n'
l2gen_const_params += 'nlwmin=     0.150000\n'
l2gen_const_params += 'wsmax=      12.0000\n'
l2gen_const_params += 'tauamax=     0.300000\n'
l2gen_const_params += 'epsmin=     0.800000\n'
l2gen_const_params += 'epsmax=      1.35000\n'
l2gen_const_params += 'glint=   0.00500000\n'
l2gen_const_params += 'windspeed=   -1000\n'
l2gen_const_params += 'windangle=   -1000\n'
l2gen_const_params += 'pressure=   -1000\n'
l2gen_const_params += 'ozone=   -1000\n'
l2gen_const_params += 'watervapor=   -1000\n'
l2gen_const_params += 'relhumid=   -1000\n'
l2gen_const_params += 'sunzen=      70.0000\n'
l2gen_const_params += 'satzen=      60.0000\n'
l2gen_const_params += 'maskland=       1\n'
l2gen_const_params += 'maskcloud=       1\n'
l2gen_const_params += 'maskglint=       0\n'
l2gen_const_params += 'maskbath=       0\n'
l2gen_const_params += 'masksunzen=       0\n'
l2gen_const_params += 'masksatzen=       0\n'
l2gen_const_params += 'maskhilt=       1\n'
l2gen_const_params += 'maskstlight=       0\n'
l2gen_const_params += 'giop_wave=[412,443,469,488,531,547,555]\n'
l2gen_const_params += 'giop_fit_opt=       1\n'
l2gen_const_params += 'giop_maxiter= 500\n'
l2gen_const_params += 'giop_aph_opt=       2\n'
l2gen_const_params += 'giop_adg_opt=       1\n'
l2gen_const_params += 'giop_bbp_opt=       3\n'
l2gen_const_params += 'giop_aph_file=$OCDATAROOT/common/aph_default.txt\n'
l2gen_const_params += 'giop_adg_file=$OCDATAROOT/common/adg_default.txt\n'
l2gen_const_params += 'giop_bbp_file=$OCDATAROOT/common/bbp_default.txt\n'
l2gen_const_params += 'giop_aph_s= 0.500000\n'
l2gen_const_params += 'giop_adg_s= 0.0145000\n'
l2gen_const_params += 'giop_bbp_s= 1.03373\n'

# L3 processing parameters
west_lon_large_nsea_l3  = -15.0
east_lon_large_nsea_l3  =  32.0
south_lat_large_nsea_l3 =  47.0
north_lat_large_nsea_l3 =  66.0

west_lon_large_bsea_l3  =  7.0
east_lon_large_bsea_l3  = 32.0
south_lat_large_bsea_l3 = 53.0
north_lat_large_bsea_l3 = 65.0

l3_grid_cell_size = 1.2
