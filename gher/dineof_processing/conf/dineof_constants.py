#!/usr/bin/env python3
__author__ = 'uwe'

headerPart  = ""
headerPart += "#"
headerPart += "# INPUT File for dineof 3.0"
headerPart += "#"
headerPart += "# Lines starting with a # or # are comments"
headerPart += "#"


dataPart  = ""
dataPart += "# gappy data to fill by DINEOF. For several matrices, separate names with commas ""
dataPart += "# Examples:  "
dataPart += "#          data = ['seacoos2005.avhrr','seacoos2005.chl']"
dataPart += "#          data = ['2Dbelcolour_region_period_anomaly.gher']"
dataPart += "#          data = ['dineof_netcdf.nc#chlor_a_mean','dineof_netcdf.nc#KdPAR_mean','dineof_netcdf.nc#tsm_678_mean']"
#####
#data = ['/data/carole/dineof-3.0/testing/DINEOF_input_ECOHAM_2006.nc#tsm_678_mean']
#####

maskPart  = ""
maskPart += "# land-sea mask of gappy data. Several masks separated by commas:"
maskPart += "# Example : "
maskPart += "#           mask = ['seacoos2005.avhrr.mask','seacoos2005.chl.mask']"
#####
#mask = ['/data/carole/dineof-3.0/testing/ECOHAM_watermask.nc#mask']
#####

timePart  = ""
timePart += "! time vector (necessary if B_DIFF option is activated in ppdef.h"
timePart += "! necessary files:"
timePart += "! time: time vector, indicating the increment between time steps in data file (must have same time dimension as data file)"
timePart += "! alpha: parameter specifying the strength of the filter"
timePart += "! numit: number of iterations for the filter"
timePart += "! See http://www.ocean-sci.net/5/475/2009/os-5-475-2009.pdf for more information"

#####
#time = '/data/carole/dineof-3.0/testing/DINEOF_input_ECOHAM_2006.nc#time'
#####
timePart += "alpha = 0.01"
timePart += "numit = 3"

nevPart  = ""
nevPart += "# Sets the numerical variables for the computation of the required"
nevPart += "# singular values and associated modes."
nevPart += "#"
nevPart += "# Give 'nev' the maximum of number of modes you allow to compute,"
nevPart += "# Dineof will stop after computing the optimal number of modes + 3 extra modes"
nevPart += "# for robust optimum detection."
nevPart += "nev = 50"

neiniPart  = ""
neiniPart += "# Give 'neini' the minimum  number of modes you want to compute"
neiniPart += "neini = 1"


ncvPart  = ""
ncvPart += "# Give 'ncv' the maximal size for the Krylov subspace"
ncvPart += "# (Do not change it as soon as ncv > nev+5)"
ncvPart += "# ncv must also be smaller than the temporal size of your matrix"
ncvPart += "ncv = 56"

tolPart  = ""
tolPart += "# Give 'tol' the threshold for Lanczos convergence"
tolPart += "# By default 1.e-8 is quite reasonable"
tolPart += "tol = 1.0e-8"

nitemaxPart  = ""
nitemaxPart += "# Parameter 'nitemax' defining the maximum number of iteration allowed for the stabilisation of eofs obtained by the cycle ((eof decomposition <-> truncated reconstruction and replacement of missing data)). An automatic criteria is defined by the following parameter 'itstop' to go faster"
nitemaxPart += "nitemax = 500"

toliterPart  = ""
toliterPart += "# Parameter 'toliter' is a precision criteria defining the threshold of automatic stopping of dineof iterations, once the ratio (rms of successive missing data reconstruction)/stdv(existing data) becomes lower then 'toliter'."
toliterPart += "toliter = 1.0e-3"

recPart  = ""
recPart += "# Parameter 'rec' for complete reconstruction of the matrix"
recPart += "# rec=1 will reconstruct all points; rec=0 only missing points"
recPart += "rec = 1"

eofPart  = ""
eofPart += "# Parameter 'eof' for writing the left and right modes of the"
eofPart += "#input matrix. Disabled by default. To activate, set to 1"
eofPart += "eof = 1"

normPart  = ""
normPart += "# Parameter 'norm' to activate the normalisation of the input matrix"""
normPart += "#for multivariate case. Disabled by default. To activate, set to 1"
normPart += "norm = 0"

OutputPart  = ""
OutputPart += "# Output folder. Left and Right EOFs will be written here"
OutputPart += "Output = '/data/carole/dineof-3.0/testing/Output/'"

#
# user chosen cross-validation points,
# remove or comment-out the following entry if the cross-validation points are to be chosen
# internally
#

# clouds = 'crossvalidation.clouds'

#
# "results" contains the filenames of the filled data
#
#results = ['All_95_1of2.sst.filled']
results = ['/data/carole/dineof-3.0/testing/Output/DINEOF_ECOHAM_tsm_2006_output.nc#tsm']

# seed to initialize the random number generator

seed = 243435


#-------------------------#
# cross-validation points #
#-------------------------#

#number_cv_points = 7000

#cloud surface size in pixels
cloud_size = 500



#cloud_mask = 'crossvalidation.mask'


#
# END OF PARAMETER FILE
#
