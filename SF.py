

########################################################
### Imports  ###########################################
########################################################


import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.special import binom as binomcoeff
from scipy.optimize import curve_fit
from scipy.integrate import quad
import datetime
import pprint
import math
import os
from matplotlib.ticker import AutoMinorLocator
import subprocess
import argparse
import re
#import SF_nestcom
#import SF_spectrum
#import SF_detector
#import SF_process





########################################################
### NEST Installation ##################################
########################################################


# collection of (my) viable NEST installations
nest_version_list = [
    "NEST4", # unknown but stably running NEST version (August 2020)
    "NEST__20200817__v2_1_0"
]


# selection of the utilized NEST installation via referencing the list above
flag_nest_version = nest_version_list[0] # <--- modify this list index if you'd like to change the NEST installation


# initialization of the corresponding paths of the NEST installation
if flag_nest_version == nest_version_list[0]:
    path_testnest = "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/" # The path below resembles the NEST installation on my laptop. I temporarily used that due to the Corona crisis.
    path_testNEST_cpp = path_testnest +"../nest/src/"
    path_nest_detectors = path_testnest +"../nest/include/Detectors/"
    detector_templatefilename = "DetectorExample_XENON10.hh"
    detector_templatefilestring = path_testnest +"../nest/include/Detectors/DetectorExample_XENON10.hh"
    path_nest_detectors = path_testnest +"../nest/include/Detectors/"


elif flag_nest_version == nest_version_list[1]:
    path_testnest = "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200817__v2_1_0/install/bin/"
    path_testNEST_cpp = path_testnest +"../../nest/src/"
    path_nest_detectors = path_testnest +"../nest/include/Detectors/"
    detector_templatefilename = "LUX_Run03.hh"
    detector_templatefilestring = path_testnest +"../../nest/include/Detectors/LUX_Run03.hh"
    path_nest_detectors = path_testnest +"../../nest/include/Detectors/"

else:
    raise Exception("You did not chose a proper NEST installation.\n Check 'SF.py' for details.")








########################################################
### File Structure #####################################
########################################################


# ---> If you want to modify the location of the input and output folder insert the corresponding paths here! <---
path_input_detectors = "./data/sample_detectors/"
path_input_spectra = "./data/sample_spectra/"
path_temp = "./temp/"


# The following detector is loaded per default.
testnestcppname = "testNEST.cpp"












