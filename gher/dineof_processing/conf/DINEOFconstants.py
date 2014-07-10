#!/usr/bin/env python3
__author__ = 'uwe'

headerPart  = ""
headerPart += "#\n"
headerPart += "# INPUT File for dineof 3.0\n"
headerPart += "#\n"
headerPart += "# Lines starting with a # or # are comments\n"
headerPart += "#\n"


dataPart  = "\n"
dataPart += "# gappy data to fill by DINEOF. For several matrices, separate names with commas \n"
dataPart += "# Examples:  \n"
dataPart += "#          data = ['seacoos2005.avhrr','seacoos2005.chl']\n"
dataPart += "#          data = ['2Dbelcolour_region_period_anomaly.gher']\n"
dataPart += "#          data = ['dineof_netcdf.nc#chlor_a_mean','dineof_netcdf.nc#KdPAR_mean','dineof_netcdf.nc#tsm_678_mean']\n"
#####
#data = ['/data/carole/dineof-3.0/testing/DINEOF_input_ECOHAM_2006.nc#tsm_678_mean']
#####

maskPart  = "\n"
maskPart += "# land-sea mask of gappy data. Several masks separated by commas:\n"
maskPart += "# Example : \n"
maskPart += "#           mask = ['seacoos2005.avhrr.mask','seacoos2005.chl.mask']\n"
#####
#mask = ['/data/carole/dineof-3.0/testing/ECOHAM_watermask.nc#mask']
#####

timePart  = "\n"
timePart += "# time vector (necessary if B_DIFF option is activated in ppdef.h\n"
timePart += "# necessary files:\n"
timePart += "# time: time vector, indicating the increment between time steps in data file (must have same time dimension as data file)\n"
timePart += "# alpha: parameter specifying the strength of the filter\n"
timePart += "# numit: number of iterations for the filter\n"
timePart += "# See http://www.ocean-sci.net/5/475/2009/os-5-475-2009.pdf for more information\n"

#####
#time = '/data/carole/dineof-3.0/testing/DINEOF_input_ECOHAM_2006.nc#time'
#####
timePart += "alpha = 0.01\n"
timePart += "numit = 3\n"

nevPart  = "\n"
nevPart += "# Sets the numerical variables for the computation of the required\n"
nevPart += "# singular values and associated modes.\n"
nevPart += "#\n"
nevPart += "# Give 'nev' the maximum of number of modes you allow to compute,\n"
nevPart += "# Dineof will stop after computing the optimal number of modes + 3 extra modes\n"
nevPart += "# for robust optimum detection.\n"
nevPart += "nev = 50\n"

neiniPart  = "\n"
neiniPart += "# Give 'neini' the minimum  number of modes you want to compute\n"
neiniPart += "neini = 1\n"


ncvPart  = "\n"
ncvPart += "# Give 'ncv' the maximal size for the Krylov subspace\n"
ncvPart += "# (Do not change it as soon as ncv > nev+5)\n"
ncvPart += "# ncv must also be smaller than the temporal size of your matrix\n"
ncvPart += "ncv = 56\n"

tolPart  = "\n"
tolPart += "# Give 'tol' the threshold for Lanczos convergence\n"
tolPart += "# By default 1.e-8 is quite reasonable\n"
tolPart += "tol = 1.0e-8\n"

nitemaxPart  = "\n"
nitemaxPart += "# Parameter 'nitemax' defining the maximum number of iteration allowed for the stabilisation of eofs obtained by the cycle ((eof decomposition <-> truncated reconstruction and replacement of missing data)). An automatic criteria is defined by the following parameter 'itstop' to go faster\n"
nitemaxPart += "nitemax = 500\n"

toliterPart  = "\n"
toliterPart += "# Parameter 'toliter' is a precision criteria defining the threshold of automatic stopping of dineof iterations, once the ratio (rms of successive missing data reconstruction)/stdv(existing data) becomes lower then 'toliter'.\n"
toliterPart += "toliter = 1.0e-3\n"

recPart  = "\n"
recPart += "# Parameter 'rec' for complete reconstruction of the matrix\n"
recPart += "# rec=1 will reconstruct all points; rec=0 only missing points\n"
recPart += "rec = 1\n"

eofPart  = "\n"
eofPart += "# Parameter 'eof' for writing the left and right modes of the\n"
eofPart += "#input matrix. Disabled by default. To activate, set to 1\n"
eofPart += "eof = 1\n"

normPart  = "\n"
normPart += "# Parameter 'norm' to activate the normalisation of the input matrix""\n"
normPart += "#for multivariate case. Disabled by default. To activate, set to 1\n"
normPart += "norm = 0\n"

OutputPart  = "\n"
OutputPart += "# Output folder. Left and Right EOFs will be written here\n"

cvPart  = "\n"
cvPart += "# user chosen cross-validation points,\n"
cvPart += "# remove or comment-out the following entry if the cross-validation points\n"
cvPart += "# are to be chosen internally\n"
cvPart += "#\n"
cvPart += "# clouds = 'crossvalidation.clouds'\n"

resultsPart  = "\n"
resultsPart += "# 'results' contains the filenames of the filled data\n"
resultsPart += "#\n"
resultsPart += "#results = ['All_95_1of2.sst.filled']\n"
#######
# results = ['/data/carole/dineof-3.0/testing/Output/DINEOF_ECOHAM_tsm_2006_output.nc#tsm']
#######

seedPart  = "\n"
seedPart += "# seed to initialize the random number generator\n"
seedPart += "seed = 243435\n"


cvpPart  = "\n"
cvpPart += "#-------------------------#\n"
cvpPart += "# cross-validation points #\n"
cvpPart += "#-------------------------#\n"
cvpPart += "#number_cv_points = 7000\n"

csPart  = "\n"
csPart += "#cloud surface size in pixels\n"
csPart += "cloud_size = 500\n"
csPart += "#cloud_mask = 'crossvalidation.mask'\n"

eopfPart  =  "\n"
eopfPart +=  "#\n"
eopfPart +=  "# END OF PARAMETER FILE\n"
eopfPart +=  "#\n"
