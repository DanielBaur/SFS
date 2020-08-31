
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


# This function is used to generate a datestring (datestring() ---> "20190714")
def datestring():
    return str(datetime.datetime.today().year) +str(datetime.datetime.today().month).zfill(2) +str(datetime.datetime.today().day).zfill(2)


# This function is used to generate a timestring (datestring() ---> "1725")
def timestring():
    return str(datetime.datetime.now().time().hour).zfill(2) +str(datetime.datetime.now().time().minute).zfill(2)


# function to convert a runlist entry to a string that can be fed into the restNEST executable
def entry_to_testneststring(entry):
    return str(entry[0]) +" " +str(entry[1]) +" " +str(entry[2]) +" " +str(entry[2]) +" " + str(entry[3]) +" " +"-1" 





########################################################
### SF_nestcom_implementdetector(), SF_nestcom_runnest #
########################################################


# This is one of the SF_nestcom main functions.
# Its purpose is to implement a specific <detectorname>.hh file into the NEST installation.
# INPUT:
#    You have to specify the  <detectorname>.hh file (string without file ending) to be implemented.
# FUNCTION:
#    The relevant entries in the files '' within the NEST installation are are modified in a way such that a following clean install implements the desired detector properties.
# OUTPUT:
#    This function returns the boolean variable 'flag_detectorokay'.
#    Its value is True if everything worked correctly and False if an error occurred.
def SF_nestcom_implementdetector(
    filestring_detector,
    path_testNEST = SF.path_testnest,
    testNESTname = SF.testnestcppname,
    path_testNEST_cpp = SF.path_testNEST_cpp
):

    # Initializing
    print("#######################################")
    print("SF_nestcom_implementdetector: Initializing.")
    detectorname = os.path.splitext(os.path.basename(filestring_detector))[0]

    # saving the <detectorname>.hh file to the dedicated folder within the NEST installation
    subprocess.call("cp " +filestring_detector +" " +SF.path_nest_detectors +detectorname +".hh", shell=True)
    print(f"SF_nestcom_implementdetector: copied '{filestring_detector}' into '{SF.path_nest_detectors}'")

    ### modifying the 'testNEST.cpp' file and performing a clean re-install

    # reading in the 'testNEST.cpp' file
    print(f"SF_nestcom_implementdetector: reading in file '{path_testNEST_cpp +testNESTname}'")
    testnestcpp_file_data_unmodified = []
    with open(path_testNEST_cpp +testNESTname, 'r') as inputfile:
        for line in inputfile:
            testnestcpp_file_data_unmodified.append(line)

    # modifying the retrieved data
    print(f"SF_nestcom_implementdetector: modifying data of file '{path_testNEST_cpp +testNESTname}'")
    testnestcpp_file_data_modified = testnestcpp_file_data_unmodified.copy()
    if SF.flag_nest_version == SF.nest_version_list[0]:
        for i in range(len(testnestcpp_file_data_modified)):
            if i==18:
                testnestcpp_file_data_modified[i] = '#include "' +detectorname +'.hh"\n'
            if i==29:
                testnestcpp_file_data_modified[i] = '  ' +detectorname +'* detector = new ' +detectorname +'();\n'
    elif SF.flag_nest_version == SF.nest_version_list[1]:
        for i in range(len(testnestcpp_file_data_modified)):
            if i==18:
                testnestcpp_file_data_modified[i] = '#include "' +detectorname +'.hh"\n'
            if i==35:
                testnestcpp_file_data_modified[i] = '  ' +detectorname +'* detector = new ' +detectorname +'();\n'

    # overwriting the 'testNEST.cpp' file
    print(f"SF_nestcom_implementdetector: editing file '{path_testNEST_cpp +testNESTname}'")
    with open(path_testNEST_cpp +testNESTname, 'w') as outputfile:
        for i in testnestcpp_file_data_modified:
            outputfile.write(i)

    # performing a clean re-install
    if SF.flag_nest_version == SF.nest_version_list[0]:
        build_path_add = ""
    elif SF.flag_nest_version == SF.nest_version_list[1]:
        build_path_add = "../"
    print(f"SF_nestcom_implementdetector: performing a clean re-install")
    subprocess.call("(cd " +path_testNEST +build_path_add +"../build && make clean)", shell=True)
    print(f"SF_nestcom_implementdetector: performed 'make clean'")
    subprocess.call("(cd " +path_testNEST +build_path_add +"../build && make)", shell=True)
    print(f"SF_nestcom_implementdetector: performed 'make'")
    subprocess.call("(cd " +path_testNEST +build_path_add +"../build && make install)", shell=True)
    print(f"SF_nestcom_implementdetector: performed 'make install'")

    # End of Program
    return


# This is one of the SF_nestcom main functions.
# Its purpose is to run NEST for a given spectrum (i.e. a ndarray)) - after the detector was previously modified by the 'SF_nestcom_implementdetector()' function.
# INPUT:
#    You have to pass the names of both the spectrum (ndarray) and also the detector (string).
# FUNCTION:
#    The the spectrum is passed on to NEST and run.
#    The output is then saved in the specified folder (typically './output_sf/') and named '<datestring>__<spectrum>__<detector>'.
# OUTPUT:
#    The output is a boolean True if everything worked fine. If not, then the output is False.
def SF_nestcom_runnest(
    filestring_spectrum,
    pathstring_output,
    detectorname = datestring() +"_detector",
    path_testnest = SF.path_testnest,
    output_pre_string="sf_output",
    flag_deletetxt = True,
    flag_use_corrected_s1s2_values = True
):

    ### Initializing
    print("#######################################")
    print("SF_nestcom_runnest: initializing.")
    flag_runnestokay = False
    s1_column_id = 6 # 7 corresponds to the corrected value
    s2_column_id = 10 # 11 corresponds to the corrected value
    if flag_use_corrected_s1s2_values == True:
        s1_column_id = 7
        s2_column_id = 11
    arraystringlist = []
    path_inputspectrum = os.path.dirname(filestring_spectrum) +"/"
    spectrumname = os.path.splitext(os.path.basename(filestring_spectrum))[0]
    temporaryfilestring = "NEST_output.txt"
    try:
        subprocess.call("mkdir temp", shell=True)
    except:
        pass
    temporaryfolder = "./temp/"
    outputstring = output_pre_string +"__" +spectrumname +"__" +detectorname
    spectrum_ndarray = np.load(path_inputspectrum +spectrumname +".npy")

    ### Running NEST and Processing the Output
    ### Looping Over the Spectrum ndarray and running NEST for every sublist of the spectrum ndarray
    ### The NEST output is forwarded to a (temporary) file called 'NEST_output.txt' stored in './temp/'.
    ### Out of this file ndarray is generated and also saved within './temp/'.
    ### The 'NEST_output.txt' file is then deleted and newly generated with the next NEST run.
    print(f"SF_nestcom_runnest: running NEST via: $ testNEST <n_events> <ER_or_NR> <e_dep_min> <e_dep_max> <e_drift> <pos>") # for the position '-1' corresponds to a random position within the detector
    for i in range(len(spectrum_ndarray)):
        savestring = "EVENTS_" +str(spectrum_ndarray[i][0]) +"__INTERACTION_" +str(spectrum_ndarray[i][1]) +"__ENERGY_" +str(spectrum_ndarray[i][2]).replace(".","_") +"__EDRIFT_" +str(spectrum_ndarray[i][3]).replace(".","_")
        arraystringlist.append(savestring +".npy")
        print(f"SF_nestcom_runnest: running {savestring}")
        subprocess.call(path_testnest +"testNEST " +str(spectrum_ndarray[i][0]) +" " +str(spectrum_ndarray[i][1]) +" " +str(spectrum_ndarray[i][2]) +" " +str(spectrum_ndarray[i][2]) +" " +str(spectrum_ndarray[i][3]) +" " +str(spectrum_ndarray[i][4]) +" >> " +temporaryfolder +temporaryfilestring, shell=True)
        print(f"SF_nestcom_runnest: successfully ran {savestring}")
        # saving the NEST output as ndarray
        nest_output_tuple_list = []
        with open(temporaryfolder +temporaryfilestring, 'r') as nest_output_txt_file:
            for line in nest_output_txt_file:
                row = line.strip().split("\t")
                if len(row)!=12:
                    continue
                elif "E_[keV]" in row[0]:
                    continue
                elif "field [V/cm]" in row:
                    continue
                elif "g1" in row[0]:
                    continue
                else:
                    nest_output_tuple_list.append((spectrum_ndarray[i][1], np.float64(spectrum_ndarray[i][2]), np.float64(row[1]),  np.uint64(row[4]),  np.uint64(row[5]), np.float64(row[s1_column_id]), np.float64(row[s2_column_id])))  # order of the output per event/line: [interaction_type, E [keV],  field [V
                    ## checking whether either the number of primary electrons or photons equals zero
                    #if np.uint64(row[4]) != 0 and np.uint64(row[5]) != 0:
                    #    nest_output_tuple_list.append((spectrum_ndarray[i][1], np.float64(spectrum_ndarray[i][2]), np.float64(row[1]),  np.uint64(row[4]), np.uint64(row[5]), np.float64(row[s1_column_id]), np.float64(row[s2_column_id])))
                    ## if either the number of primary electrons or photons equals zero make sure that at least the energy is small enough for this to be justified.
                    ## (The reason for this cross check is a possible NEST bug (see: studies -> nest_stuff_for_other_people -> section 5))
                    #elif (np.uint64(row[4]) == 0 or np.uint64(row[5]) == 0) and np.float64(spectrum_ndarray[i][2]) <= 20:
                    #    nest_output_tuple_list.append((spectrum_ndarray[i][1], np.float64(spectrum_ndarray[i][2]), np.float64(row[1]),  np.uint64(row[4]),  np.uint64(row[5]), np.float64(row[s1_column_id]), np.float64(row[s2_column_id])))  # order of the output per event/line: [interaction_type, E [keV],  field [V/cm],  Nph,  Ne]
                    #nest_output_tuple_list.append((spectrum_ndarray[i][1], np.float64(spectrum_ndarray[i][2]), np.float64(row[1]),  np.uint64(row[4]),  np.uint64(row[5])))  # order of the output per event/line: [interaction_type, E [keV],  field [V/cm],  Nph,  Ne]
#            for k in range(len(nest_output_tuple_list)):
#                print(f"interaction_type: {nest_output_tuple_list[i][0]}")
#                print(f"energy_deposition: {nest_output_tuple_list[i][1]}")
#                print(f"field_strength: {nest_output_tuple_list[i][2]}")
#                print(f"number_of_photons: {nest_output_tuple_list[i][3]}")
#                print(f"number_of_electrons: {nest_output_tuple_list[i][4]}")
        nest_output_dtype = np.dtype([
            ("interaction_type", np.unicode_, 16),
            ("energy_deposition", np.float64),
            ("field_strength", np.float64),
            ("number_of_photons", np.uint64),
            ("number_of_electrons", np.uint64),
            ("s1_phe", np.float64),
            ("s2_phe", np.float64),
        ])
        nest_output_ndarray = np.array(nest_output_tuple_list, nest_output_dtype)
        np.save(temporaryfolder +savestring +".npy", nest_output_ndarray)
        if flag_deletetxt == True:
            subprocess.call("rm " +temporaryfolder +temporaryfilestring, shell=True)
        print(f"SF_nestcom_runnest: saved {savestring}")
    ### Summarizing all ndarrays Into One Single ndarray
    ### As soon as the loop over the spectrum ndarray is finished, all ndarrays within './temp/' are summarized into one output ndarray.
    ### This ndarray is named <datestring>__<spectrum>__<detector>.npy and stored within './output_sf/'.
    ### Afterwards the content of './temp/' deleted.
    print(f"SF_nestcom_runnest: generating {outputstring}.npy")
    ndarray_list = []
    for i in range(len(arraystringlist)):
        ndarray_list.append(np.load(temporaryfolder +arraystringlist[i]))
    concatenated_array = np.concatenate(ndarray_list)
    print(f"SF_nestcom_runnest: generated concatenated array {outputstring}")
    np.save(pathstring_output +outputstring +".npy", concatenated_array)
    print(f"SF_nestcom_runnest: saved concatenated array {pathstring_output +outputstring}.npy")
    # cleaning up
    if flag_deletetxt == True:
        subprocess.call("rm -r " +temporaryfolder +"*", shell=True)
    print(f"SF_nestcom_runnest: cleaned up {temporaryfolder}")
    ### Setting the Output Flag
    flag_runnestokay = True 
    #except:
    #    flag_runnestokay = False

    ### End of Program
    if flag_runnestokay == True:
        print(f"SF_nestcom_runnest: finished ---> success")
        print("#######################################\n")
        return concatenated_array
    else:
        outcome = "fail !!!!!!!!!!!!!!!!!!!!!!!!!"
        print(f"SF_nestcom_runnest: finished ---> fail")
        print("#######################################\n")
        return flag_runnestokay





