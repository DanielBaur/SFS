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











########################################################
### Helper Functions ###################################
########################################################


def exponential_float_to_latex(expfloat):
    expfloatstring = str(expfloat)
    a = "" # leading float
    if expfloatstring[:expfloatstring.index("e")] != "1":
        a = expfloatstring[:expfloatstring.index("e")] +r"\cdot "
    b = "" # sign of the exponent
    if expfloatstring[expfloatstring.index("e")+1] == "-":
        b = "-"
    c = expfloatstring[expfloatstring.index("e")+2:] # exponent without sign
    output_string = a +r"10^{" +b +c +r"}"
    return output_string





########################################################
### Process Signal Formation Output ####################
########################################################


# This function is used to generate histogram data from quanta data (e.g. dataset["number_of_electrons"])
def get_histogram_data_from_primary_quanta_data(quanta_data):
    # initializing stuff
    quanta_min = np.min(quanta_data)
    quanta_max = np.max(quanta_data)
    quanta_dif = quanta_max-quanta_min
    percentage_off_limits = 20
    bins_range = np.arange(max(0,int(quanta_min-(quanta_dif*(100+percentage_off_limits)/100)))-0.5,int(quanta_max+(quanta_dif*(100+percentage_off_limits)/100)),1)
    # calculating the histrogram data via np.histogram
    counts, bin_edges = np.histogram(a=quanta_data, bins=bins_range)
    number_of_quanta = np.zeros(len(counts))
    for i in range(len(counts)):
        number_of_quanta[i] = bin_edges[i]+0.5
    return counts, number_of_quanta


# This function takes the histogram data generated with get_histogram_data_from_primary_quanta_data()
# and computes the corresponding stepized histogram data in a way such that it can be plotted in a 'stepized' way.
def stepize_primary_quanta_histogram_data(counts, number_of_quanta):
    # calculating the 'stepized' data
    counts_stepized = np.zeros(2*len(counts))
    number_of_quanta_stepized = np.zeros(2*len(number_of_quanta))
    for i in range(len(counts)):
        counts_stepized[2*i] = counts[i]
        counts_stepized[(2*i)+1] = counts[i]
        number_of_quanta_stepized[2*i] = number_of_quanta[i] -0.5
        number_of_quanta_stepized[2*i+1] = number_of_quanta[i] +0.5
    return counts_stepized, number_of_quanta_stepized


# This function is used to stepize arbitrary histogram data.
# I.e. it takes two lists representing both the bin centers and also the corresponding counts and calculates two new lists containing both the left and right edges of the bins and two instances of the counts.
def stepize_histogram_data(bincenters, counts):
    # calculating the binwidth
    binwidth = bincenters[1]-bincenters[0]
    bincenters_stepized = np.zeros(2*len(bincenters))
    counts_stepized = np.zeros(2*len(counts))
    for i in range(len(bincenters)):
        bincenters_stepized[2*i] = bincenters[i] -0.5*binwidth
        bincenters_stepized[(2*i)+1] = bincenters[i] +0.5*binwidth
        counts_stepized[2*i] = counts[i]
        counts_stepized[2*i+1] = counts[i]
    return bincenters_stepized, counts_stepized


# This function is used to rebin the histogram data.
def rebin_histogram_data(x_data, counts_data, rebin_by_number=False, set_number_of_bins=False, ret_bin_numbers_as_bin_centers=False):
    # rebinning by a specific number
    if rebin_by_number!=False and set_number_of_bins==False:
        print(f"Reducing number of bins by {rebin_by_number}.")
        length = len(x_data)//set_number_of_bins +len(x_data)%set_number_of_bins
        counts_data_rebinned = np.zeros(length)
        x_data_rebinned = np.zeros(length)
        j = 0
        ctr = 0
        for i in range(len(x_data)):
            counts_data_rebinned[j] = x_data_rebinned[j] +counts_data[i]
            x_data_rebinned[j] = x_data_rebinned[j] +x_data[i]
            ctr +=1
            if ctr==rebin_by_number:
                ctr=0
                j +=1
        return counts_data_rebinned, x_data_rebinned
    # rebinning to a certain number of bins
    elif rebin_by_number==False and set_number_of_bins!=False:
        print(f"Rebinning to {set_number_of_bins} bins.")
        # determining both the bin edges and centers
        bin_centers = np.linspace(start=np.min(x_data), stop=np.max(x_data), num=set_number_of_bins, endpoint=True)
        bin_width = bin_centers[1]-bin_centers[0]
        bin_edges = np.linspace(start=bin_centers[0]-0.5*bin_width, stop=bin_centers[len(bin_centers)-1]+0.5*bin_width, num=set_number_of_bins+1, endpoint=True)
        # filling up and returning the new ndarrays
        counts_data_rebinned = np.zeros(len(bin_centers))
        for i in range(len(x_data)):
            ctr = 0
            while x_data[i] > bin_edges[ctr]:
                ctr +=1
            j = ctr-1
            #print(j)
            counts_data_rebinned[j] = counts_data_rebinned[j] +counts_data[i]
        if ret_bin_numbers_as_bin_centers==True:
            bin_centers = np.linspace(start=1, stop=set_number_of_bins, num=set_number_of_bins, endpoint=True)
        return counts_data_rebinned, bin_centers
    # no rebin information specified
    else:
        print("No rebin information specifi")
        return counts_data, x_data


# This function is used to disjunctively seperate an sfndarray into multiple subsets that all share interaction_type, energy_deposition and field_strength
def gen_subdatasets_from_gnampfino_data(data):
    # check for all available subsets
    mask_list = []
    for i in data:
        mask_list_entry = [i["interaction_type"], i["energy_deposition"], i["field_strength"]]
        if mask_list_entry not in mask_list:        
            mask_list.append(mask_list_entry)
    print(mask_list)
    # generate and return a list of subdatasets
    subdataset_list = []
    for i in mask_list:
        subdataset_list.append(data[(data["interaction_type"]==i[0]) & (data["energy_deposition"]==i[1]) & (data["field_strength"]==i[2])])
    return mask_list, subdataset_list


# This function is used to calculate the mean number of primary quanta for a given SF dataset
def calc_mean_number_of_primary_photons_and_electrons(data):
    mean_number_of_primary_photons = np.mean(data["number_of_photons"])
    mean_number_of_primary_electrons = np.mean(data["number_of_electrons"])
    return mean_number_of_primary_photons, mean_number_of_primary_electrons


# Function to define a gaussian curve with amplitude "A", mean "mu" and sigma "sigma".
def gauss_function(x,A,mu,sigma):
    return A/np.sqrt(2*np.pi*sigma**2)*np.exp(-(x-mu)**2/(2*sigma**2))


# This function is used to fit histogram data generated with get_histogram_data_from_primary_quanta_data() with a Gaussian bell curve
# so one can infer the mean number of quanta and also the spread from the distribution.
def fit_gaussian_to_histogram_data(counts, number_of_quanta):
    guess = (5, number_of_quanta[list(counts).index(max(counts))], 1)
    p_opt, p_cov = curve_fit(gauss_function, number_of_quanta, counts, p0=guess, method='lm')
    A = p_opt[0]
    mu = p_opt[1]
    sigma = p_opt[2]
    sA = np.sqrt(np.diag(p_cov))[0]
    smu = np.sqrt(np.diag(p_cov))[1]
    ssigma = np.sqrt(np.diag(p_cov))[2]
    return A, mu, sigma,sA, smu, ssigma


# This function takes as an input a mask_list of a dataset (generated with SF.gen_subdatasets_from_gnampfino_data())
# and calculates from that the number of columns (one for each energy) and number of rows (one for each drift field)
# if you want to display the distribution of primary quanta in a cartesion arrangement of subplots
def calc_subplot_dimensions_for_subsets(mask_list):
    # How many lines are there for the ER side (corresponds to the number of different ER fields)?
    ER_field_list = []
    for i in range(len(mask_list)):
        if "ER" in mask_list[i] and mask_list[i][2] not in ER_field_list:
            ER_field_list.append(mask_list[i][2])
    # How many columns are there for the ER side (corresponds to the number of different ER energies)?
    ER_energy_list = []
    for i in range(len(mask_list)):
        if "ER" in mask_list[i] and mask_list[i][1] not in ER_energy_list:
            ER_energy_list.append(mask_list[i][1])
    # How many lines are there for the NR side (corresponds to the number of different NR fields)?
    NR_field_list = []
    for i in range(len(mask_list)):
        if "NR" in mask_list[i] and mask_list[i][2] not in NR_field_list:
            NR_field_list.append(mask_list[i][2])
    # How many columns are there for the NR side (corresponds to the number of different NR energies)?
    NR_energy_list = []
    for i in range(len(mask_list)):
        if "NR" in mask_list[i] and mask_list[i][1] not in NR_energy_list:
            NR_energy_list.append(mask_list[i][1])
    # determining the number of rows and columns
    print(f"{ER_field_list}")
    print(f"{ER_energy_list}")
    print(f"{NR_field_list}")
    print(f"{NR_energy_list}")
    n_rows = max(len(ER_field_list),len(NR_field_list))
    n_cols = len(ER_energy_list) +len(NR_energy_list)
    mask_list_dict = {
        "ER_field_list" : ER_field_list,
        "ER_energy_list" : ER_energy_list,
        "NR_field_list" : NR_field_list,
        "NR_energy_list" : NR_energy_list
    }
    return n_rows, n_cols, mask_list_dict


# This function is used to determine the coordinates of a subplot within a distribution comparison plot
# (see: ## 1.2 Distribution of Primary Quanta in PSF.ipynb)
def determine_subplot_coordinates_for_mask_list_entry_from_mask_list_dict(mask_list_dict, mask_list_entry):
    col = 0
    row = 0
    mask_list_dict["ER_energy_list"]
    mask_list_dict["NR_energy_list"]
    interaction_type = mask_list_entry[0]
    energy_deposition = mask_list_entry[1]
    field_strength = mask_list_entry[2]
    if interaction_type == "ER":
        row = mask_list_dict["ER_field_list"].index(field_strength)
        col = mask_list_dict["ER_energy_list"].index(energy_deposition)
        return col, row
    elif interaction_type == "NR":
        row = mask_list_dict["NR_field_list"].index(field_strength)
        col = mask_list_dict["NR_energy_list"].index(energy_deposition) +len(mask_list_dict["ER_energy_list"])
        return col, row
    else:
        print(f"The interaction type of the {mask_list_entry} subsample is fishy.")
        return


# This function is used to calculate the root mean square (RMS) of a list of floats
def qmean(data):
    ld = len(data)
    s = np.float128(0)
    for i in range(ld):
        s = np.float128(s +np.multiply(data[i],data[i]), dtype=np.float128)
        #print(f"multiplication: {i}")
        #print(f"{data[i]}*{data[i]}={data[i]*data[i]} ---> s={s}\n")
    return np.float64(np.sqrt(s/ld))


# This function is used to summarize the output .npy files (either multiple ones or one concatenated file if flag_saveasonearray is set to True).
# I.e.: all events with the same properties (i.e. interaction_type, energy_deposition, drift_field) in the end make up one line within the output file that also contains information such as:
# mean, rms, spread, etc...
def gen_summarized_ndarray(input_folder, ndarray, output_folder):

    ### retrieving the data
    raw_ndarray = np.load(input_folder +ndarray)
    mask_list, subdataset_list = gen_subdatasets_from_gnampfino_data(data=raw_ndarray)

    ### processing
    processed_ndarray_tuplelist = []
    # defining the dtype
    store_dtype = np.dtype([
        ("number_of_events", np.uint64),
        ("interaction_type", np.unicode_, 16),
        ("energy_deposition", np.float64),
        ("field_strength", np.float64),
        ("mean_number_of_photons", np.float64),
        ("rms_number_of_photons", np.float64),
        ("mean_number_of_photons_sigma", np.float64),
        ("mean_number_of_electrons", np.float64),
        ("rms_number_of_electrons", np.float64),
        ("mean_number_of_electrons_sigma", np.float64),
        ("mean_s1_phe", np.float64),
        ("mean_s1_phe_sigma", np.float64),
        ("mean_s2_phe", np.float64),
        ("mean_s2_phe_sigma", np.float64),
    ])
    for i in range(len(subdataset_list)):
        # calculations
        number_of_events = len(subdataset_list[i])
        interaction_type = subdataset_list[i]["interaction_type"][0]
        energy_deposition = subdataset_list[i]["energy_deposition"][0]
        field_strength = subdataset_list[i]["field_strength"][0]
        mean_number_of_photons = np.mean(subdataset_list[i]["number_of_photons"])
        rms_number_of_photons = qmean(subdataset_list[i]["number_of_photons"])
        mean_number_of_photons_sigma = np.std(subdataset_list[i]["number_of_photons"], ddof=1, dtype=np.float64) #/np.sqrt(number_of_events, dtype=np.float128)
        mean_number_of_electrons = np.mean(subdataset_list[i]["number_of_electrons"])
        rms_number_of_electrons = qmean(subdataset_list[i]["number_of_electrons"])
        # modified on 27th May 2020
        # Mariana needs to know the spread of the distribution of primary electrons.
        # Unfortunately there appears to be some kind of 'feature' in NEST (for higher energies and fields) that sometimes yields zero primary electrons (probably some geometry effect).
        # But this heavily distorts the spread of the distribution.
        # Accordingly the subdataset defined in the line below is supposed to no contain these data points.
        sigma_electrons_subdataset = subdataset_list[i]["number_of_electrons"][(subdataset_list[i]["number_of_electrons"] != 0) | ((subdataset_list[i]["number_of_electrons"] == 0) & (subdataset_list[i]["energy_deposition"] <= 5))]
        mean_number_of_electrons_sigma = np.std(sigma_electrons_subdataset, ddof=1, dtype=np.float64) #/np.sqrt(number_of_events, dtype=np.float128)
        mean_s1_phe = np.mean(subdataset_list[i]["s1_phe"])
        mean_s1_phe_sigma = np.std(subdataset_list[i]["s1_phe"], ddof=1, dtype=np.float64)
        mean_s2_phe = np.mean(subdataset_list[i]["s2_phe"])
        mean_s2_phe_sigma = np.std(subdataset_list[i]["s2_phe"], ddof=1, dtype=np.float64)
        # appending to the tuple list
        processed_ndarray_tuplelist.append((
            number_of_events,
            interaction_type,
            energy_deposition,
            field_strength,
            mean_number_of_photons,
            rms_number_of_photons,
            mean_number_of_photons_sigma,
            mean_number_of_electrons,
            rms_number_of_electrons,
            mean_number_of_electrons_sigma,
            mean_s1_phe,
            mean_s1_phe_sigma,
            mean_s2_phe,
            mean_s2_phe_sigma
        ))

    ### generating the processed ndarray
    processed_ndarray = np.array(processed_ndarray_tuplelist, store_dtype)
    np.save(output_folder +ndarray[:-4] +"__PROCESSED" +".npy", processed_ndarray)
    return processed_ndarray





########################################################
### ER/NR Discrimination Studies #######################
########################################################


# This function is used to return the value (as int or float) corresponding to 'parametername' from the 'filename'.
# If neither parameter nor value can be found 'False' is returned.
def get_parameter_val_from_filename(filename, parametername):
    ### generating a list from the input filename
    filename_mod = filename.replace("__","_")
    if "." in filename_mod:
        filename_mod = filename_mod[:filename_mod.index(".")]
    filename_list = list(filename_mod.split("_"))
    ### converting all strings to ints if possible
    for i in range(len(filename_list)):
        try:
            filename_list[i] = int(filename_list[i])
        except:
            pass
    ### looping over the modified filename list and writing everything into a dictionary
    filename_dict = {}
    ctr = 0
    while ctr < len(filename_list):
        new_key = ""
        new_val = 0
        if type(filename_list[ctr]) == str:
            if (ctr+1) < len(filename_list):
                if type(filename_list[ctr+1]) == str:
                    new_key = filename_list[ctr] +"_" +filename_list[ctr+1]
                    ctr += 2
                else:
                    new_key = filename_list[ctr]
                    ctr += 1
            else:
                new_key = filename_list[ctr]
                ctr += 1
            # checking for subsequent ints
            if type(filename_list[ctr]) == int:
                if (ctr+1) < len(filename_list):
                    if type(filename_list[ctr+1]) == int:
                        new_val = float(str(filename_list[ctr]) +"." +str(filename_list[ctr+1]))
                        ctr += 2
                    else:
                        new_val = filename_list[ctr]
                        ctr += 1
                else:
                    new_val = filename_list[ctr]
                    ctr += 1
            # updating the dict
            filename_dict.update({new_key : new_val})
        else:
            ctr += 1
    ### printing the dict
    for key, val in filename_dict.items():
        print(key, val)
    ### returning the parameter value from the dictionary
    return filename_dict[parametername]



