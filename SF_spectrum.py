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
import json
from scipy.integrate import quad






########################################################
### Helper Functions ###################################
########################################################


# This function is used to check, whether a regular expression (note: r"kjfsdklja") is contained within a string
# USED BY:
#    ---> gen_spectrum_ndarray_from_file()
def check_for_rex(rexstring, string):
    boo=False
    if re.compile(rexstring).search(string):
        boo=True
    return boo


# This function is used to convert an input tuple list resembling a SFS spectrum into a ndarray.
# INPUT:
#    You just have to pass the tuple list to convert.
# FUNCTION:
#    The given tuple list is read in and converted to a ndarray.
# OUTPUT:
#    This function returns the ndarray generated from the input tuple list.
# USED BY:
#    ---> gen_spectrum_ndarray_from_file()
#    (This is btw. the function used within GND.ipynb to pass custom input on to NEST.)
def gen_spectrum_ndarray_from_tuplelist(spectrum_tuple_list):
    # defining the ndarray dtype
    spectrum_ndarray_dtype = np.dtype([
        ("number_of_events", np.uint64),
        ("interaction_type", np.unicode_, 16),
        ("energy_deposition", np.float64),
        ("field_strength", np.float64),
        ("position", np.unicode_, 32)
    ])
    # generating and returning the spectrum ndarray
    spectrum_ndarray = np.array(spectrum_tuple_list, spectrum_ndarray_dtype)
    return spectrum_ndarray


# This function is used to convert an input file (e.g. .txt or .json) resembling a SFS spectrum and convert it into a ndarray.
# INPUT:
#    You have to specify the input spectrum (i.e. string but WITH the correct file ending such as .txt or .json).
# FUNCTION:
#    The specified file is read in and converted to a ndarray.
# OUTPUT:
#    This function returns the ndarray generated from the input file.
# USAGE:
#    ---> SF_spectrum()
# NOTE:
#    Implement the option to not specify the position of the interaction as usually this is random anyhow.
def gen_spectrum_ndarray_from_file(spectrumfilename, path):

    ### Initializing
    spectrum_tuple_list = []

    ### Step 1: Generating a Tuple List
    # .json
    if spectrumfilename.endswith(".json"):
        spectrumname = spectrumfilename[:-5]
        spectrum_tuple_list = json.load(path +spectrumfilename)
    # .txt
    elif spectrumfilename.endswith(".txt"):
        spectrumname = spectrumfilename[:-4]
        # looping over the "NEST_output.txt" file and writing the contents into the upper list
        with open(path +spectrumfilename, 'r') as spectrumfile:
            for line in spectrumfile:
                if "#" not in line and check_for_rex(rexstring=r"\([^)]*,[^)]*,[^)]*,[^)]*,[^)]*\)", string=line)==True:
                    lst = re.compile(r"\([^)]*,[^)]*,[^)]*,[^)]*,[^)]*\)").search(line).group(0).strip().replace("(","").replace(")","").split(", ")
                    tup = (int(lst[0]), lst[1], float(lst[2]), float(lst[3]), lst[4])
                    spectrum_tuple_list.append(tup)
    # any other file type
    else:
        raise Exception(f"SF_spectrum: ERROR\n---> only .txt and .json files are supported so far, plese edit the SF_spectrum.gen_spectrum_ndarray_from_file() function")

    ### Step 2: Saving the ndarray
    spectrum_ndarray = gen_spectrum_ndarray_from_tuplelist(spectrum_tuple_list=spectrum_tuple_list)
    np.save(path +spectrumname +".npy", spectrum_ndarray)

    ### End of Program
    return spectrum_ndarray





########################################################
### Generating Spectra on the Go via Function Calls ####
########################################################


###  Gnampfinos: Parameter Sweep  ######################
# This function is used to generate a gnampfino spectrum by calculating the cartesian product of the specified parameter range.
# USAGE:
#    ---> not used within any function
def gen_gnampfino_parametersweep(name, savefolder, number_of_samples_per_run, paramrange_interactiontype, paramrange_energydeposition, paramrange_edrift):
    # generating the tuple list
    gnampfino_parametersweep_tuple_list = []
    for i in paramrange_interactiontype:
        for j in paramrange_energydeposition:
            for k in paramrange_edrift:
                gnampfino_parametersweep_tuple_list.append((number_of_samples_per_run, i,j,k,"-1"))
    # converting the tuple list to a ndarray and saving it
    gnampfino_parametersweep_ndarray = gen_spectrum_ndarray_from_tuplelist(spectrum_tuple_list=gnampfino_parametersweep_tuple_list)
    np.save(savefolder +name +".npy", gnampfino_parametersweep_ndarray)
    print(f"SF_spectrum: saved ndarray '{name}.npy' to '{savefolder}'")
    return gnampfino_parametersweep_ndarray


###  WIMPs  #######################################
# This function is used to generate a WIMP recoil spectrum by executing Marc's modified .cpp file.
# NOTE:
#    The unmodified version is executed in the following way:
#     1. source root
#     2. loading the file with root: root .L xenon_limits.cpp
#     3. execute the desired command within root: diffrate_int(40.,1e-47,1,5,50)
# NOTE:
#    So far this function just outputs histogram data (counts +bin_centers).
# USAGE:
#    ---> encode_functioncallstring()
def gen_wimp_recoil_spectrum_marc(mass=40.0, crosssection=1e-47, exposure=5):
    subprocess.call("source /usr/local/root-6.10.06/root-6.10.06-build/bin/thisroot.sh", shell=True)
    subprocess.call("root -q -l './xenon_limits_mod.cpp(40.,1e-47)'", shell=True)
    return


###  WIMPs  #######################################
# This function is used to generate a WIMP recoil spectrum.
def gen_wimp_recoil_spectrum(
    # main parameters
    mass_wimp_gev = 40.0, # in GeV/c^2
    cross_section_wimp_proton_cm2 = 1e-47, # in cm^2
    mass_detector_target_t = 40, # in tonnes
    time_exposure_y = 5, # in years
    e_nr_kev = None, # default is 'None'
    # parameters
    energy_threshold_kev = 2, # in keV_nr
    wimp_dark_matter_mass_density_gevcm3 = 0.3, # in GeV/c^2/cm^3
    velocity_escape_kmps = 544, # in km/s
    velocity_circular_kmps = 220, # in km/s
    mass_target_nucleus_u = 130.9050824, # in amu
    mass_proton_u = 1.00727647, # in amu
    mass_number_target_nucleus = 131,
    # output parameters
    energy_nuclear_recoil_min = 0, # in keV_nr
    energy_nuclear_recoil_max = 60, # in keV_nr
    number_of_bins_or_samples = 120,
    # flags
    flag_output = "histogram"
):

    ### model calculation
    # conversion to SI units
    mass_target_nucleus = mass_target_nucleus_u *1.66053906660 *10**(-27) # conversion to kg
    mass_proton = mass_proton_u *1.66053906660 *10**(-27) # conversion to kg
    mass_detector_target = mass_detector_target_t *1000 # conversion to kg
    time_exposure = time_exposure_y *365 *24 *60 *60 # conversion to s
    mass_wimp = (mass_wimp_gev *10**9 *1.60218 *10**(-19))/((3*10**8)**2) # conversion to kg
    energy_threshold = energy_threshold_kev *1000 *1.60218 *10**(-19) # conversion to Joule
    cross_section_wimp_proton = cross_section_wimp_proton_cm2 *(1/10000) # conversion to m^2
    wimp_dark_matter_mass_density = wimp_dark_matter_mass_density_gevcm3 *(1000000) # conversion to GeV/m^3
    velocity_escape = velocity_escape_kmps *1000 # conversion to m/s
    velocity_circular = velocity_circular_kmps *1000 # conversion to m/s
    # derived quantities
    number_of_target_nuclei = mass_detector_target/mass_target_nucleus
    redmass_wimp_proton = (mass_proton *mass_wimp)/(mass_proton +mass_wimp)
    redmass_wimp_nucleus = (mass_wimp *mass_target_nucleus)/(mass_wimp +mass_target_nucleus)
    velocity_min = np.sqrt((mass_target_nucleus *energy_threshold)/(2 *(redmass_wimp_nucleus**2)))
    # integrated spin-independent WIMP nucleus cross-section
    cross_section_integrated_wimp_nucleus_spin_independent = mass_number_target_nucleus**2 *(redmass_wimp_nucleus/redmass_wimp_proton)**2 *cross_section_wimp_proton
    # nuclear form factors (Helm model: https://iopscience.iop.org/article/10.1088/0253-6102/55/6/21/pdf)
    def nuclear_form_factor(energy_nuclear_recoil):
        # recoil energy -> momentum transfer
        p = np.sqrt(2*mass_target_nucleus *(energy_nuclear_recoil*1000 *1.60218 *10**(-19)))
        q = p/(1.0545718*10**(-34))
        r_n = 1.2*mass_number_target_nucleus**(1/3)*(1/10**(15)) # nuclear radius in m
        # calculating substeps
        qr_n = q*r_n
        s = (1/10**(15)) # skin thickness in m
        qs = q*s
        #a = 3*(np.sin(math.radians(qr_n))-qr_n*np.cos(math.radians(qr_n)))
        a = 3*(np.sin(qr_n)-qr_n*np.cos(qr_n))
        b = (qr_n)**3
        c = np.exp(-((q*s)**2/2))
        return a/b *c
    # wimp velocity distribution
    def wimp_velocity_distribution(v):
        v_0 = np.sqrt(2/3) *velocity_circular
        j = 4 *np.pi *v**2
        f = np.sqrt((np.pi *v_0**2))**3
        exp = np.exp(-((v**2)/(v_0**2)))
        return (j/f) *exp
    # differential WIMP-nucleus cross-section
    def cross_section_differential_wimp_nucleus(v, energy_nuclear_recoil):
        return (mass_target_nucleus *cross_section_integrated_wimp_nucleus_spin_independent *nuclear_form_factor(energy_nuclear_recoil=energy_nuclear_recoil)**2) /(2 *redmass_wimp_nucleus**2 *v**2)
    # integrand function
    # NOTE: You might ask why there is a factor v**3 instead of just v in the integrand function.
    # The reason is that you are integrating over f(v) in three spatial dimensions.
    # Hence (using spherical coordinates) you also pick up a factor of r**2 *sin(theta).
    # Integrating sin(theta) over dtheta and dphi gives you a factor of 4*np.pi and then you still have to additionally integrate r**2.
    def integrand_function(v, energy_nuclear_recoil):
        return wimp_velocity_distribution(v) *v *cross_section_differential_wimp_nucleus(v, energy_nuclear_recoil=energy_nuclear_recoil)
    # differential recoil rate in DRU (i.e. events/kg/d/keV)
    def differential_recoil_rate_dru(energy_nuclear_recoil):
        scaling_factor = (1/(mass_detector_target)) *(60 *60 *24) *(1/((1/1000) *1.60218 *10**(+19))) # conversion from events/s/J into events/kg/d/keV
        return scaling_factor *number_of_target_nuclei *(wimp_dark_matter_mass_density/mass_wimp_gev) *quad(integrand_function, velocity_min, velocity_escape +velocity_circular, args=(energy_nuclear_recoil))[0]
    # differential recoil rate adapted to detector settings (i.e. events/detector_mass/exposure_time/keV)
    def differential_recoil_rate_det(energy_nuclear_recoil):
        scaling_factor = time_exposure *(1/((1/1000) *1.60218 *10**(+19))) # conversion from events/s/J into events/kg/d/keV
        return scaling_factor *number_of_target_nuclei *(wimp_dark_matter_mass_density/mass_wimp_gev) *quad(integrand_function, velocity_min, velocity_escape +velocity_circular, args=(energy_nuclear_recoil))[0]

    ### generating output
    # returning absolute rates by integrating the differential energy spectrum; i.e. energy bin centers, absolute counts per energy bin
    if flag_output == "histogram":
        binwidth = (energy_nuclear_recoil_max -energy_nuclear_recoil_min)/number_of_bins_or_samples
        energy_bin_centers = np.linspace(start=energy_nuclear_recoil_min+0.5*binwidth, stop=energy_nuclear_recoil_max-0.5*binwidth, num=number_of_bins_or_samples, endpoint=True)
        counts_per_energy_bin = np.zeros_like(energy_bin_centers)
        for i in range(len(energy_bin_centers)):
            counts_per_energy_bin[i] = quad(differential_recoil_rate_det, energy_bin_centers[i]-0.5*binwidth, energy_bin_centers[i]+0.5*binwidth)[0]
        return energy_bin_centers, counts_per_energy_bin
    # returning the differential recoil spectrum in DRU (events/kg/d/keV)
    elif flag_output == "rate":
        energy_nuclear_recoil_list = np.linspace(start=energy_nuclear_recoil_min, stop=energy_nuclear_recoil_max, num=number_of_bins_or_samples, endpoint=True)
        diff_rate_list = np.zeros_like(energy_nuclear_recoil_list)
        for i in range(len(energy_nuclear_recoil_list)):
            diff_rate_list[i] = differential_recoil_rate_dru(energy_nuclear_recoil=energy_nuclear_recoil_list[i])
        return energy_nuclear_recoil_list, diff_rate_list
    # returning a single value of the differential recoil spectrum in DRU
    elif flag_output == "single_dru_value" and e_nr_kev != None:
        return differential_recoil_rate_dru(energy_nuclear_recoil=e_nr_kev)
    else:
        print("invalid input: 'flag_output'")
        return
    

# This function is conceptualized to utilize the 'gen_wimp_recoil_spectrum()' function defined above in order to also be able to process composite detectors.
def wimp_recoil_spectrum_for_composite_detector_material(
    detector_composition_list = [ # default is natural xenon
        {
            "a" : 124,
            "m_amu" : 123.905893,
            "relative_abundance_perc" : 0.095,
        },
        {
            "a" : 126,
            "m_amu" : 125.904274,
            "relative_abundance_perc" : 0.089,
        },
        {
            "a" : 128,
            "m_amu" : 127.9035313,
            "relative_abundance_perc" : 1.910,
        },
        {
            "a" : 129,
            "m_amu" : 128.9047794,
            "relative_abundance_perc" : 26.401,
        },
        {
            "a" : 130,
            "m_amu" : 129.9035080,
            "relative_abundance_perc" : 4.071,
        },
        {
            "a" : 131,
            "m_amu" : 130.9050824,
            "relative_abundance_perc" : 21.232,
        },
        {
            "a" : 132,
            "m_amu" : 131.9041535,
            "relative_abundance_perc" : 26.909,
        },
        {
            "a" : 134,
            "m_amu" : 133.9053945,
            "relative_abundance_perc" : 10.436,
        },
        {
            "a" : 136,
            "m_amu" : 135.907219,
            "relative_abundance_perc" : 8.857,
        },
    ],
    **kwargs
):

    # cross-check: calculating the sum of the given relative abundances
    rel_ab_sum = 0
    for i in range(len(detector_composition_list)):
        rel_ab_sum = rel_ab_sum +detector_composition_list[i]["relative_abundance_perc"]
    print(f"SF_spectrum.wimp_recoil_spectrum_for_composite_detector_material: your relative abundances add up to {rel_ab_sum} %")

    # defining a function to return the composite differential recoil rate
    def differential_recoil_rate_for_composite_detector_material_in_dru(nuclearrecoilenergy):
        comp_dru_val = 0
        kwargs_mod = kwargs.copy()
        if "e_nr_kev" in kwargs_mod:
            kwargs_mod.pop("e_nr_kev")
        if "flag_output" in kwargs_mod:
            kwargs_mod.pop("flag_output")
        for i in range(len(detector_composition_list)):
            dru_val = gen_wimp_recoil_spectrum(
                mass_target_nucleus_u = detector_composition_list[i]["m_amu"],
                mass_number_target_nucleus = detector_composition_list[i]["a"],
                e_nr_kev = nuclearrecoilenergy,
                flag_output = "single_dru_value",
                **kwargs_mod
            )
            comp_dru_val = comp_dru_val +(0.01*detector_composition_list[i]["relative_abundance_perc"]*dru_val)
        return comp_dru_val

    # returning one single recoil spectrum value
    if kwargs["flag_output"] == "single_dru_value":
        return differential_recoil_rate_for_composite_detector_material_in_dru(nuclearrecoilenergy = kwargs["e_nr_kev"])

    # returning the differential recoil spectrum in DRU (events/kg/d/keV)
    elif kwargs["flag_output"] == "rate":
        energy_nuclear_recoil_list = np.linspace(start=kwargs["energy_nuclear_recoil_min"], stop=kwargs["energy_nuclear_recoil_max"], num=kwargs["number_of_bins_or_samples"], endpoint=True)
        diff_rate_list = np.zeros_like(energy_nuclear_recoil_list)
        for i in range(len(energy_nuclear_recoil_list)):
            diff_rate_list[i] = differential_recoil_rate_for_composite_detector_material_in_dru(nuclearrecoilenergy=energy_nuclear_recoil_list[i])
        return energy_nuclear_recoil_list, diff_rate_list

    # returning absolute rates by integrating the differential energy spectrum; i.e. energy bin centers, absolute counts per energy bin
    elif kwargs["flag_output"] == "histogram":
        binwidth = (kwargs["energy_nuclear_recoil_max"] -kwargs["energy_nuclear_recoil_min"])/kwargs["number_of_bins_or_samples"]
        energy_bin_centers = np.linspace(start=kwargs["energy_nuclear_recoil_min"]+0.5*binwidth, stop=kwargs["energy_nuclear_recoil_max"]-0.5*binwidth, num=kwargs["number_of_bins_or_samples"], endpoint=True)
        counts_per_energy_bin = np.zeros_like(energy_bin_centers)
        for i in range(len(energy_bin_centers)):
            counts_per_energy_bin[i] = kwargs["mass_detector_target_t"]*1000 *kwargs["time_exposure_y"] *365 *quad(differential_recoil_rate_for_composite_detector_material_in_dru, energy_bin_centers[i]-0.5*binwidth, energy_bin_centers[i]+0.5*binwidth)[0]
        return energy_bin_centers, counts_per_energy_bin

    # returning else
    else:
        return



###  Encoder Function  ############################
# This function is used to encode a function call string that can be used to generate new spectra on the go.
# INPUT:
#    You have to pass the potential 'functioncallstring' (string) and also the 'flag_encode_or_execute' (i.e. either 'encode' oder 'execute').
# FUNCTION:
#    First the functioncallstring matches a certain pattern.
#    If 'flag_encode_or_execute' is set to 'encode' just the name of the function is returned.
#    If 'flag_encode_or_execute' is set to 'execute' the corresponding function to generate a spectrum is called (e.g. gen_wimp_recoil_spectrum()).
# OUTPUT:
#    The output of this function is either the name of the function called or the output of the respective function called (typically a ndarray that can subsequently be passed on to NEST).
# USED BY:
#    ---> SF_spectrum()
# HOW TO:
#    A functioncallstring (fcs) is a concatenation of one 'identifierstring' and arbitrarily many 'parameterstrings'.
#    The 'identifierstring' is used to identify the function that is supposed to be called.
#    The 'parameterstrings' are then all passed on to this function.
#    Assume you exemplarily wanted to use gen_wimp_recoil_spectrum() to generate a WIMP spectrum for a WIMP mass of 40GeV/c^2, a crossection of 1e-47cm^2 and an exposure of 5 tonne years:
#    Then you'd need to pass on the following: fcs = "gen_wimp_recoil_spectrum__40__1e-47__5"
def encode_functioncallstring(functioncallstring, flag_encode_or_execute='encode'):

    ### Encoding
    encode_list = functioncallstring.split("__")
    # casting the parameters either into floats or leave them as strings
    param_list = []
    for i in range(1,len(encode_list)):
        try:
            param_list.append(float(encode_list[i]))
        except:
            param_list.append(encode_list[i])
    # checking whether there is a corresponding function
    if encode_list[0] not in globals():
        return False

    ### Generating Spectra by Executing the Calles Function
    # encode mode
    if flag_encode_or_execute == 'encode':
        return encode_list[0]
    # execute mode
    elif flag_encode_or_execute == 'execute':
        return globals()[encode_list[0]](*param_list)
    # exception
    else:
        raise Exception(f"SF_spectrum: ERROR\n---> wrong flag: {flag_encode_or_execute}")
        return False





########################################################
### SF_spectrum ########################################
########################################################


### SF_spectrum() ######################################
# This is the SF_spectrum main function.
# Its purpose is to generate a spectrum .npy file (that can then be passed on to the function X running NEST).
# INPUT:
#    You have to specify the input spectrum (string).
#    This string is either corresponding to a <spectrum>.npy, <spectrum>.json or <spectrum>.txt file within the './input_spectra/' folder) or encoding a function call to generate a new spectrum.
# FUNCTION:
#    If the specified <spectrum>.npy file does not alread exist, it is generated from the <spectrum>.json or <spectrum>.txt files.
#    If there is no file corresponding to the input 'spectrum' string, the string is checked whether it matches a function call and if it does, the corresponding function is called.
#    Note that this function does not employ NEST.
# OUTPUT:
#    If everything worked out this function returns a ndarray representing the spectrum passed on to , otherwise it returns the boolean value False.
def SF_spectrum(spectrum, path_sfsspectra, force=False):

    ### Initializing
    print("#######################################")
    print("SF_spectrum: initializing")
    print(f"---> {spectrum}")
    flag_spectrumokay = False

    ### Checking and/or Generating the <spectrum>.npy
    # option 1: string (could correspond to .npy, .json, .txt file or a function call)
    if type(spectrum) == str:
        # check if <spectrum>.npy exists
        if os.path.isfile(path_sfsspectra +spectrum +".npy") == True and force == False:
            print(f"SF_spectrum: '{spectrum}.npy' found")
            try:
                flag_spectrumokay = np.load(path_sfsspectra +spectrum +".npy")
                print(f"SF_spectrum: loaded '{spectrum}.npy'")
            except:
                print(f"SF_spectrum: ERROR")
                print(f"---> could not load '{spectrum}.npy'")
        # check if <spectrum>.json exists
        elif os.path.isfile(path_sfsspectra +spectrum +".json")==True:
            print(f"SF_spectrum: '{spectrum}.json' found")
            try:
                flag_spectrumokay = gen_spectrum_ndarray_from_file(spectrumfilename=spectrum +".json", path=path_sfsspectra)
                print(f"SF_spectrum: saved '{spectrum}.npy' to {path_sfsspectra}")
            except:
                print(f"SF_spectrum: ERROR")
                print(f"---> could not convert '{spectrum}.json' to '{spectrum}.npy'")
        # check if <spectrum>.txt exists
        elif os.path.isfile(path_sfsspectra +spectrum +".txt")==True:
            print(f"SF_spectrum: '{spectrum}.txt' found")
            #try:
            flag_spectrumokay = gen_spectrum_ndarray_from_file(spectrumfilename=spectrum +".txt", path=path_sfsspectra)
            print(f"SF_spectrum: saved '{spectrum}.npy' to {path_sfsspectra}")
            #except:
            print(f"SF_spectrum: ERROR")
            print(f"---> could not convert '{spectrum}.txt' to '{spectrum}.npy'")
        # check if 'spectrum' corresponds to a function call
        elif encode_functioncallstring(functioncallstring=spectrum, flag_encode_or_execute='encode') != False:
            print(f"SF_spectrum: spectrum generating function called")
            try:
                print(f"---> {encode_functioncallstring(functioncallstring=spectrum, flag_encode_or_execute='encode')}")
                flag_spectrumokay = encode_functioncallstring(functioncallstring=spectrum, flag_encode_or_execute='execute')
            except:
                print(f"SF_spectrum: ERROR")
                print(f"---> could not execute {encode_functioncallstring(functioncallstring=spectrum, flag_encode_or_execute='encode')}")
        # else: return False
        else:
            print(f"SF_detector: ERROR")
            print(f"---> '{spectrum}' neither matches a file within {path_sfsspectra} nor a function call.")
    # option 2: list (could be a custom spectrum list generated with GND)
    elif type(spectrum) == list:
        print(f"SF_spectrum: list inserted")
        try:
            flag_spectrumokay = gen_spectrum_ndarray_from_tuplelist(spectrumtuplelist) # <------------------ generate and save .npy file from list
        except:
            print(f"SF_spectrum: ERROR")
            print(f"---> could not convert the list into a ndarray")
    # anything else
    else:
        print(f"SF_spectrum: ERROR")
        print(f"---> Apocalyptic Clusterfuck!")

    ### End of Program
    if flag_spectrumokay != False:
        outcome = "Success"
    else:
        outcome = "Fail !!!!!!!!!!!!!!!!!!!!!!!!!"
    print(f"SF_spectrum: finished")
    print(f"---> {outcome}")
    print("#######################################\n")
    return flag_spectrumokay





