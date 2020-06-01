
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
### Global Definitions #################################
########################################################


# ---> Insert the path to your testNEST executable here! <---
path_testnest = "/scratch/db1086/NEST4/install/"
# The path below resembles the NEST installation on my laptop. I temporarily used that due to the Corona crisis.
path_testnest = "/home/daniel/Desktop/arbeitsstuff/NEST4/install/"


# ---> If you want to modify the location of the input and output folder insert the corresponding paths here! <---
path_input_detectors = "./data/sample_detectors/"
path_input_spectra = "./data/sample_spectra/"
path_temp = "./temp/"
path_nest_detectors = path_testnest +"../nest/include/Detectors/"


# The following detector is loaded per default.
detector_templatefilename = "DetectorExample_XENON10.hh"
path_testNEST_cpp = path_testnest +"../nest/"
testnestcppname = "src/testNEST.cpp"



########################################################
### Helper Functions ###################################
########################################################


# function to check how many files within a specified folder contain a certain string in their name
#def files_containing_string(filestring, foldername):
#    filelist = []
#    for filename in os.listdir(foldername):
#        if filestring in filename:
#            filelist.append(filename)
#    #filelist.append(filename for filename in os.listdir(foldername) if filestring in filename)
#    return filelist


# This function is used to compare two files line by line.
# If two lines differ they are both printed.
#def compare_txt_files(file1, file2):
#    f1_list = []
#    with open(file1, 'r') as f1:
#        for line in f1:
#            f1_list.append(line)
#    f2_list = []
#    with open(file2, 'r') as f2:
#        for line in f2:
#            f2_list.append(line)
#    for i in range(min(len(f1_list), len(f2_list))):
#        if f1_list[i] != f2_list[i]:
#            print(f1_list[i])
#            print(f2_list[i])




'''
########################################################
### Main: SF() #########################################
########################################################


# This is the SF main function.
# Its purpose is to automatize and wrap the NEST functionality to generate primary quanta and convert them into S1 and S2 photoelectrons.
# INPUT: 
#    You have to specify both the input spectrum and the detector you conduct your studies with.
#    Therefore you have to pass the names (as strings) of the respective files within './input_spectrum/' and './input_detector/' respectively.
# FUNCTION:
#    First NEST is newly installed with the detector you specified being implemented.
#    Afterwards the specified spectrum is passed onto NEST (i.e. the testNEST executable), NEST does its job and generates primary quanta and the output is written to one single file.
# OUTPUT:
#    The output file is a numpy structured array (ndarray, .npy file) stored within './output_sf/'.
#    It is named the following way: <datestring>__<spectrum>__<detector>.npy
def SF(spectrum, detector, pathtestnest=path_testnest, pathspectra=path_input_spectra, pathdetectors=path_input_detectors, pathoutput=path_output_sf, flag_force=False):

    ### Initializing
    print("\n#############################################################")
    print("SF: initializing.")
    print("#############################################################\n")
    flag_detectorokay = False
    flag_spectrumokay = False
    flag_nestrunokay = False
    flag_sfokay = False

    ### Retrieving the Detector and Setting UP NEST ---> see SF_detector.py, SF_nestcom.py
    print("#############################################################")
    print("SF: setting up NEST with the detector --> {detector}")
    print("#############################################################\n")
    flag_detectorokay = SF_detector.SF_detector(detectorname=detector, path_nestdetectors=path_nest_detectors, path_sfsdetectors=pathdetectors, templatefilename=detector_templatefilename, force=flag_force)
    if flag_detectorokay == True:
        flag_detectorokay = SF_nestcom.SF_nestcom_implementdetector(detectorname=detector, path_testNEST=pathtestnest)

    ### Retrieving the Spectrum ---> see SF_spectrum.py
    print("#############################################################")
    print("SF: retrieving the spectrum --> {spectrum}")
    print("#############################################################\n")
    flag_spectrumokay = SF_spectrum.SF_spectrum(spectrum=spectrum, path_sfsspectra=pathspectra, force=flag_force) # flag_spectrumokay stores either the ndarray representing the spectrum or the boolean value False

    ### Running NEST and Saving the Output ---> see SF_nestcom.py
    print("#############################################################")
    print("SF: running NEST.")
    print("#############################################################\n")
    # detector and spectrum look fine ---> run NEST
    if flag_detectorokay == True and flag_spectrumokay != False:
        flag_nestrunokay = SF_nestcom.SF_nestcom_runnest(path_inputspectrum=pathspectra, spectrumname=spectrum, detectorname=detector, path_testnest=pathtestnest, path_output=pathoutput)
    else:
        print("SF: NEST not run due to previous error")

    ### End of Program
    # NEST run successfully
    if flag_nestrunokay == True:
        outcome = "success"
        flag_sfokay = True
    # NEST not run successfully
    else:
        if flag_detectorokay == False and flag_spectrumokay != False:
            problem = "detector"
        elif flag_detectorokay == True and flag_spectrumokay == False:
            problem = "spectrum"
        else:
            problem = "detector + spectrum"
        outcome = f"fail: {problem}"
    print("#############################################################")
    print("SF: finished")
    print(f"---> {outcome}")
    print("#############################################################\n")
    return flag_sfokay
'''




########################################################
### Executing Signal Formation as Main #################
########################################################

if __name__ == "__main__":
    # processing the input arguments
    '''
    parser = argparse.ArgumentParser(description='Process SFS input.')
    parser.add_argument('-s', '--spectrum', dest='spectrum', type=str, required=True)
    parser.add_argument('-d', '--detector', dest='detector', type=str, required=True)
    parser.add_argument('--pathtestnest', dest='pathtestnest', type=str, required=False, default=path_testnest)
    parser.add_argument('--pathspectra', dest='pathspectra', type=str, required=False, default=path_input_spectra)
    parser.add_argument('--pathdetectors', dest='pathdetectors', type=str, required=False, default=path_input_detectors)
    parser.add_argument('--pathoutput', dest='pathoutput', type=str, required=False, default=path_output_sf)
    parser.add_argument('--fs', dest='force_spectrum', type=bool, required=False, default=False)
    # obtaining the strings corresponding to input arguments
    s = parser.parse_args().spectrum
    d = parser.parse_args().detector
    ptn = parser.parse_args().pathtestnest
    ps = parser.parse_args().pathspectra
    pdc =  parser.parse_args().pathdetectors
    po =  parser.parse_args().pathoutput
    fs = parser.parse_args().force_spectrum
    # executing the SF function with the retrieved objects
    flag_sf = SF(spectrum=s, detector=d, pathtestnest=ptn, pathspectra=ps, pathdetectors=pdc, pathoutput=po, force_spectrum=fs)
    print("\n")
    '''




