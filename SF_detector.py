
########################################################
### Imports ############################################
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
import SF





########################################################
### Helper Functions ###################################
########################################################


# This is a helper function used to convert a boolean value in Python into a string that corresponds to a boolean value in C++.
# USAGE:
#    gen_detector_hh_file_from_dict()
def conv_to_cpp_bool(python_bool_val):
    if python_bool_val==True:
        return "true"
    else:
        return "false"


# This function is used to convert floats/ints to strings and vice versa so that one can insert detector parameters into filenames without having to type "." characters.
# USAGE: within the '1.3. Parameter Sweep' cell within the 'er_nr_discrimination' study
def numberstring(number_int_float_or_string):
    if type(number_int_float_or_string)==int:
        return str(number_int_float_or_string)
    elif type(number_int_float_or_string)==float:
        return str(number_int_float_or_string).replace(".","_")
    elif type(number_int_float_or_string)==str:
        return float(number_int_float_or_string)
    else:
        raise Exception("wrong input type")


# This is a helper function used to search a specific line of the <templatefilename>.hh file for a parameter string and (if found) replace the corresponding values.
# USAGE:
#    gen_detector_hh_file_from_dict()
def modify_detector_parameter_in_line(linestring, parameterstring, value):
    valuestring = str(value)
    # if the parameter appears within the linestring do modification stuff
    if parameterstring +" " in linestring:
        modlinestring = re.sub("\=\s.*\;", "= " +valuestring +";//", linestring)
        return modlinestring
    else:
        return linestring


# This function is used to generate and return a dictionary containing the detector parameters extracted from a .txt file.
# USAGE:
#    SF_detector()
def gen_detector_dict_from_txt_file(detectorname, folderpath):

    ### initializing the detector list and dictionary
    print(f"SF_detector: extracting detector parameters from {detectorname}.txt .")
    detector_dictionary = {}
    detector_list = []

    ### reading in the detector data
    with open(folderpath +detectorname +".txt", 'r') as inputfile:
        for line in inputfile:
            detector_list.append(line)
    print(f"SF_detector: read in parameters from {detectorname}.txt .")

    ### filling the detector dictionary
    for i in detector_list:
        if re.compile(r'\s*"[^"]*"\s:\s[^,]*[,|}]').search(i):
        #modlinestring = re.sub("\=\s.*\;", "= " +valuestring +";", linestring)
        #lst = re.compile(r"\([^)]*,[^)]*,[^)]*,[^)]*,[^)]*\)").search(line).group(0).strip().replace("(","").replace(")","").split(", ")
            k = re.compile(r'"[^"]*"').search(i).group(0).replace('"','')
            v_prelim = re.compile(r':\s*[^,}]*[,|}]').search(i).group(0).replace(',','').replace('}','').replace(': ','')
            if "False" in v_prelim:
                v = False
            elif "True" in v_prelim:
                v = True
            else:
                v = float(v_prelim)
            new_entry = {k:v}
            detector_dictionary.update(new_entry)

    ### returning the detector dictionary
    print(f"SF_detector: successfully extracted detector parameters from {detectorname}.txt .")
    return detector_dictionary


# This function is used to generate a <detectorname>.hh file from a detector parameters dictionary.
# INPUT:
#    You have to specify the detector name (string withouth file ending).
# FUNCTION:
#    The file specified by 'templatefilename' is used as a template.
#    It is looped over and the respective parameters are then exchanged with the values stored in the dictionary.
# OUTPUT:
#    The <detectorname>.hh file is saved in both the './input_detectors/' folder and the './Detectors/' folder within the NEST installation.
# USAGE:
#    SF_detector()
def gen_detector_hh_file_from_dict(
    detectorname,
    templatefilestring = SF.detector_templatefilestring,
    savefolders = [SF.path_input_detectors, SF.path_nest_detectors],
    # Primary Scintillation (S1) parameters
    g1 = 0.073,       		# phd per S1 phot at dtCntr (not phe). Divide out 2-PE effect
    sPEres = 0.58,    		# single phe resolution (Gaussian assumed)
    sPEthr = 0.35,    		# POD threshold in phe, usually used IN PLACE of sPEeff
    sPEeff = 1.00,    		# actual efficiency, can be used in lieu of POD threshold
    noise_0_ = 0.0,   		# baseline noise mean and width in PE (Gaussian)
    noise_1_ = 0.0,   		# baseline noise mean and width in PE (Gaussian)
    P_dphe = 0.2,     		# chance 1 photon makes 2 phe instead of 1 in Hamamatsu PMT
    coinWind = 100,   		# S1 coincidence window in ns
    coinLevel = 2,    		# how many PMTs have to fire for an S1 to count
    numPMTs = 89,     		# For coincidence calculation
    # Linear noise" terms as defined in Dahl thesis and by D. McK
    noise_2_ = 3e-2,  		# S1 -> S1 Gaussian-smeared with noise[2]*S1
    noise_3_ = 3e-2,  		# S2 -> S2 Gaussian-smeared with noise[3]*S2
    # Ionization and Secondary Scintillation (S2) parameters
    g1_gas = .0655,   		# phd per S2 photon in gas, used to get SE size
    s2Fano = 3.61,    		# Fano-like fudge factor for SE width
    s2_thr = 300.,    		# the S2 threshold in phe or PE, *not* phd. Affects NR most
    E_gas = 12.,      		# field in kV/cm between liquid/gas border and anode
    eLife_us = 2200., 		# the drift electron mean lifetime in micro-seconds
    # Thermodynamic Properties  [if you are getting warnings about being in gas, lower T and/or raise p]
    inGas = False,  		# 
    T_Kelvin = 177.,  		# for liquid drift speed calculation
    p_bar = 2.14,     		# gas pressure in units of bars, it controls S2 size
    # Data Analysis Parameters and Geometry
    dtCntr = 40.,     		# center of detector for S1 corrections, in usec.
    dt_min = 20.,     		# minimum. Top of detector fiducial volume
    dt_max = 60.,     		# maximum. Bottom of detector fiducial volume
    radius = 50.,     		# millimeters (fiducial rad)
    radmax = 50.,     		# actual physical geo. limit
    TopDrift = 150.,  		# mm not cm or us (but, this *is* where dt=0), a z-axis value of 0 means the bottom of the detector (cathode OR bottom PMTs), In 2-phase, TopDrift=liquid/gas border. In gas detector it's GATE, not anode!
    anode = 152.5,    		# the level of the anode grid-wire plane in mm, In a gas TPC, this is not TopDrift (top of drift region), but a few mm, above it
    gate = 147.5,           # mm. This is where the E-field changes (higher), in gas detectors, the gate is still the gate, but it's where S2 starts
    cathode = 1.00,         # mm. Defines point below which events are gamma-X
    # 2-D (X & Y) Position Reconstruction
    PosResExp = 0.015,      # exp increase in pos recon res at hi r, 1/mm
    PosResBase = 70.8364,   # baseline unc in mm, see NEST.cpp for usage
):

    ### Initializing
    print(f"SF_detector: generating {detectorname}.hh.")
    # defining the detector parameters dictionary with all the parameters as strings (note that the input dictionary does not necessarily have to contain all parameters - a default value is passed on otherwise)
    dict_parameters = {
        # Primary Scintillation (S1) parameters
        "g1" : str(g1),                   # phd per S1 phot at dtCntr (not phe). Divide out 2-PE effect
        "sPEres" : str(sPEres),           # single phe resolution (Gaussian assumed)
        "sPEthr" : str(sPEthr),           # POD threshold in phe, usually used IN PLACE of sPEeff
        "sPEeff" : str(sPEeff),           # actual efficiency, can be used in lieu of POD threshold
        "noise[0]" : str(noise_0_),       # baseline noise mean and width in PE (Gaussian)
        "noise[1]" : str(noise_1_),       # baseline noise mean and width in PE (Gaussian)
        "P_dphe" : str(P_dphe),           # chance 1 photon makes 2 phe instead of 1 in Hamamatsu PMT
        "coinWind" : str(coinWind),       # S1 coincidence window in ns
        "coinLevel" : str(coinLevel),     # how many PMTs have to fire for an S1 to count
        "numPMTs" : str(numPMTs),         # For coincidence calculation
        # Linear noise" terms as defined in Dahl thesis and by D. McK
        "noise[2]" : str(noise_2_),       # S1 -> S1 Gaussian-smeared with noise[2]*S1
        "noise[3]" : str(noise_3_),       # S2 -> S2 Gaussian-smeared with noise[3]*S2
        # Ionization and Secondary Scintillation (S2) parameters
        "g1_gas" : str(g1_gas),           # phd per S2 photon in gas, used to get SE size
        "s2Fano" : str(s2Fano),           # Fano-like fudge factor for SE width
        "s2_thr" : str(s2_thr),           # the S2 threshold in phe or PE, *not* phd. Affects NR most
        "E_gas" : str(E_gas),             # field in kV/cm between liquid/gas border and anode
        "eLife_us" : str(eLife_us),       # the drift electron mean lifetime in micro-seconds
        # Thermodynamic Properties  [if you are getting warnings about being in gas, lower T and/or raise p]
        "inGas" : conv_to_cpp_bool(inGas),
        "T_Kelvin" : str(T_Kelvin),       # for liquid drift speed calculation
        "p_bar" : str(p_bar),             # gas pressure in units of bars, it controls S2 size
        # Data Analysis Parameters and Geometry
        "dtCntr" : str(dtCntr),           # center of detector for S1 corrections, in usec.
        "dt_min" : str(dt_min),           # minimum. Top of detector fiducial volume
        "dt_max" : str(dt_max),           # maximum. Bottom of detector fiducial volume
        "radius" : str(radius),           # millimeters (fiducial rad)
        "radmax" : str(radmax),           # actual physical geo. limit
        "TopDrift" : str(TopDrift),       # mm not cm or us (but, this *is* where dt=0), a z-axis value of 0 means the bottom of the detector (cathode OR bottom PMTs), In 2-phase, TopDrift=liquid/gas border. In gas detector it's GATE, not anode!
        "anode" : str(anode),             # the level of the anode grid-wire plane in mm, In a gas TPC, this is not TopDrift (top of drift region), but a few mm, above it
        "gate" : str(gate),               # mm. This is where the E-field changes (higher), in gas detectors, the gate is still the gate, but it's where S2 starts
        "cathode" : str(cathode),         # mm. Defines point below which events are gamma-X
        # 2-D (X & Y) Position Reconstruction
        "PosResExp" : str(PosResExp),     # exp increase in pos recon res at hi r, 1/mm
        "PosResBase" : str(PosResBase),   # baseline unc in mm, see NEST.cpp for usage
    }
    # reading in the template file
    print(f"SF_detector: reading {templatefilestring}")
    template_file_data_unmodified = []
    with open(templatefilestring, 'r') as inputfile:
        for line in inputfile:
            template_file_data_unmodified.append(line)

    ### Modifying the Template Detector Data
    print(f"SF_detector: modifying the template .hh file.")
    # looping over the entries of 'template_file_data_unmodified' and modifying those
    template_file_data_modified = template_file_data_unmodified.copy()
    if SF.flag_nest_version == SF.nest_version_list[0]:
        for i in range(len(template_file_data_modified)):
            if i==12:
                template_file_data_modified[i] = '#ifndef ' +detectorname +'_hh\n'
            if i==13:
                template_file_data_modified[i] = '#define ' +detectorname +'_hh 1\n'
            if i==19:
                template_file_data_modified[i] = 'class ' +detectorname +' : public VDetector {\n'
            if i==21:
                template_file_data_modified[i] = '  ' +detectorname +'() {\n'
            if i==23:
                template_file_data_modified[i] = '    cerr << "You are currently using the ' +detectorname +' detector."\n'
            if i==30:
                template_file_data_modified[i] = '  virtual ~' +detectorname +'(){};\n'
            elif i>35 and i<90:
                for key,val in dict_parameters.items():
                    if "    " +key +" =" in template_file_data_modified[i]:  # each line has to be checked for the string '"    " +key +" ="' because otherwise some of the parameters would be found multiple times within the file
                        template_file_data_modified[i] = modify_detector_parameter_in_line(linestring=template_file_data_modified[i], parameterstring=key, value=val)
    elif SF.flag_nest_version == SF.nest_version_list[1]:
        for i in range(len(template_file_data_modified)):
            if i==1:
                template_file_data_modified[i] = '#ifndef ' +detectorname +'_hh\n'
            if i==2:
                template_file_data_modified[i] = '#define ' +detectorname +'_hh 1\n'
            if i==11:
                template_file_data_modified[i] = 'class ' +detectorname +' : public VDetector {\n'
            if i==15:
                template_file_data_modified[i] = '  ' +detectorname +'() {\n'
            if i==17:
                template_file_data_modified[i] = '    cerr << "You are currently using the ' +detectorname +' detector.";\n'
            if i==22:
                template_file_data_modified[i] = '  virtual ~' +detectorname +'(){};\n'
            elif i>26 and i<75:
                for key,val in dict_parameters.items():
                    if "    " +key +" =" in template_file_data_modified[i]:  # each line has to be checked for the string '"    " +key +" ="' because otherwise some of the parameters would be found multiple times within the file
                        template_file_data_modified[i] = modify_detector_parameter_in_line(linestring=template_file_data_modified[i], parameterstring=key, value=val)

    ### saving the <detectorname>.hh File to the folders specified within the 'savefolders' input parameter.
    for pathstring in savefolders:
        with open(pathstring +detectorname +".hh", 'w+') as outputfile:
            for i in template_file_data_modified:
                outputfile.write(i)
        print(f"SF_detector: saved {pathstring}{detectorname}.hh")
    return


# This function is used to print out the detector parameters (in latex or html format).
# It is used to easily insert them into presentations or wiki notes.
# 'input_string_format' : "default_parameters", "parameter_sweep"
# 'output_format' : "html", "latex"
def print_detector_parameters(input_string="jfk", input_string_format="default_parameters", output_format="html"):
    # preparing the input string
    text = input_string.replace("    ", "")
    text = list(text.split("\n"))
    # printing the lines for the default parameters
    if input_string_format == "default_parameters":
        for line in text:
            if line != "" and line[0] != "#":
                param_name = line[:line.index(":")].replace('"','').replace(' ','')
                param_val = line[line.index(":"):line.index("#")].replace(':','').replace(' ','').replace(',','')
                param_comment = line[line.index("#")+2:].replace('#','')
                if output_format == "html":
                    print("| ''" +param_name +"'' | " +param_val +" | " +param_comment +" |")
                elif output_format == "latex":
                    print("| ''" +param_name +"'' | " +param_val +" | " +param_comment +" |")
                else:
                    print(f"invalid input parameter 'output_format': {output_format}.")
                    return
            elif line != "" and line[0] == "#":
                if output_format == "html":
                    print("^ " +line[2:] +" ^^^")
                elif output_format == "latex":
                    print("^ " +line[2:] +" ^^^")
                else:
                    print(f"invalid input parameter 'output_format': {output_format}.")
                    return
            else:
                continue #print(f"line: {line}")
        return
    # printing the lines for the parameter sweep
    elif input_string_format == "parameter_sweep":
        for line in text:
            if line != "" and line[0] != "#":
                param_name = line[:line.index(":")].replace('"','').replace(' ','')
                param_vals = line[line.index("[")+1:line.index("]")].replace(':','')
                if "#" in line:
                    param_comment = line[line.index("#")+2:].replace('#','')
                else:
                    param_comment = ""
                if output_format == "html":
                    print("| ''" +param_name +"'' | " +param_vals +" | " +param_comment +" |")
                elif output_format == "latex":
                    print("| ''" +param_name +"'' | " +param_vals +" | " +param_comment +" |")
                else:
                    print(f"invalid input parameter 'output_format': {output_format}.")
                    return
            else:
                continue #print(f"line: {line}")
        return
    else:
        print(f"invalid input parameter 'input_string_format': {input_string_format}.")
        return





########################################################
### Main: SF_detector() ################################
########################################################


# This is the SF_detector main function.
# Its purpose is to generate a detector header file and copy it into the NEST 'Detectors' folder.
# INPUT:
#    You have to specify the input detector (string corresponding to either a <detectorname>.txt or <detectorname>.hh file within the './input_detectors/' folder).
# FUNCTION:
#    If the specified <detectorname>.hh file does not alread exist, it is generated from the <detectorname>.txt file.
#    The <detectorname>.hh file is then copied into the 'Detectors' folder of the NEST installation.
#    Note that the afterwards necessary clean install of NEST (in order to implemnt the detector into the 'testNEST' executable) is done by the 'SF_nestcom_implementdetector' function defined within 'SF_nestcom.py'.
# OUTPUT:
#    This function returns the boolean variable 'flag_detectorokay'.
#    Its value is True if everything was generated correctly and False if an error occurred.
# NOTE:
#    Daniel, you still wanted to implement a 'force' option.
def SF_detector(
    detectorname,
    path_nestdetectors,
    path_sfsdetectors,
    templatefilename,
    force=False
):#, file_detectortemplate, flag_force=False):

    ### Initializing
    print("#######################################")
    print("SF_detector: initializing.")
    flag_detectorokay = False

    ### Checking for the <detectorname>.hh File and Generating it Within the input_detectors Folder
    # check if <detectorname>.hh exists
    if os.path.isfile(path_sfsdetectors +detectorname +".hh") == True and force == False:
        print(f"SF_detector: {detectorname}.hh found.")
        flag_detectorokay = True
    # check if <detectorname>.txt exists
    elif os.path.isfile(path_sfsdetectors +detectorname +".txt")==True:
        print(f"SF_detector: {detectorname}.txt found.")
        try:
            detector_parameters = gen_detector_dict_from_txt_file(detectorname=detectorname, folderpath=path_sfsdetectors)
            gen_detector_hh_file_from_dict(detectorname=detectorname, templatefilename=templatefilename, folder_sfs=path_sfsdetectors, **detector_parameters)
            flag_detectorokay = True
        except:
            print(f"SF_detector: ERROR.")
            print(f"---> could not generate file '{detectorname}.hh'.")
    # neither of the <detectorname>.hh and <detectorname>.txt files exists
    else:
        print(f"SF_detector: There is neither a <detectorname>.hh or <detectorname>.txt file matching your specification '{detectorname}'.")

    ### Copying the <detectorname>.hh to the NEST Installation
    if flag_detectorokay == True:
        try:
            subprocess.call('cp ' +path_sfsdetectors +detectorname +'.hh ' +path_nestdetectors +detectorname +'.hh' , shell=True)
            print(f"SF_detector: {detectorname}.hh saved to {path_nestdetectors}.")
        except:
            flag_detectorokay = False
            print(f"SF_detector: ERROR.")
            print(f"---> could not copy file '{detectorname}.hh' into '{path_nestdetectors}'")

    ### End of Program
    if flag_detectorokay == True:
        outcome = "success"
    else:
        outcome = "fail !!!!!!!!!!!!!!!!!!!!!!!!!"
    print(f"SF_detector: Finished ---> {outcome}")
    print("#######################################\n")
    return flag_detectorokay





