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


# This function is used to draw an energy contour line onto a signature data plot in the log(cS2/cS1) vs. cS1/g1 observable space.
def draw_energy_contour_line(
    ax,
    param_e_keV, # in keV
    param_g1,
    param_g2,
    param_w = SF.W,
    number_of_samples = 150,
    fmt_rel_annotation_height_y = 0.04,
    fmt_color = "#8c8c8b",
    fmt_linewidth = 0.8,
    fmt_fontsize = 7,
    fmt_x_offset = 0.01,
    flag_annotateenergyval = True):

    # general stuff
    param_e = param_e_keV *1000

    # calculating the data points to be plotted as countour line
    contour_tuplelist = []
    contour_dtype = np.dtype([
        ("s1", np.float64),
        ("s1_g1", np.float64),
        ("s2", np.float64),
        ("log_s2_s1", np.float64)])
    max_x_val = param_e/param_w
    for i in np.linspace(start=0, stop=max_x_val, num=number_of_samples, endpoint=True):
        s1 = i*param_g1
        s2 = param_g2*(max_x_val - i)
        appendtuple = (
            s1,
            i,
            s2,
            np.log10(s2/s1))
        if i != 0 and i != max_x_val:
            contour_tuplelist.append(appendtuple)
    contour_data = np.array(contour_tuplelist, contour_dtype)

    # plotting the contour line
    plt.plot(
        contour_data["s1_g1"],
        contour_data["log_s2_s1"],
        color = fmt_color,
        linewidth = fmt_linewidth)
    
    # annotating the energy value
    x_axis_limits = plt.gca().get_xlim() # retrieving the x-axis boundaries
    y_axis_limits = plt.gca().get_ylim() # retrieving the y-axis boundaries
    approximate_y_val = y_axis_limits[0] +fmt_rel_annotation_height_y*(y_axis_limits[1]-y_axis_limits[0]) # calculating a y-axis value that is corresponds to a fraction of 'fmt_rel_annotation_height' times the  whole y-axis scale
    best_y_val = [np.sqrt((contour_data["log_s2_s1"][i]-approximate_y_val)**2) for i in range(len(contour_data))] # determining the value from 'contour_data["log_s2_s1"]' that deviates the least from the one defined above
    min_dev_index = best_y_val.index(np.min(best_y_val)) # determining the index of the value defined above
    extracted_x_val = contour_data["s1_g1"][min_dev_index] # extract the corresponding x, i.e. 's1/g1', value
    fmt_rel_annotation_height_x = (extracted_x_val-x_axis_limits[0])/(x_axis_limits[1]-x_axis_limits[0]) # converting the absolute x value to a relative one
    if flag_annotateenergyval == True:
        plt.text(
            y = fmt_rel_annotation_height_y,
            x = fmt_rel_annotation_height_x +fmt_x_offset,
            transform = ax1.transAxes,
            s =  r"$" +f"{param_e_keV:.1f}" +r"\,\mathrm{keV_{ee}}$",
            color = fmt_color,
            fontsize = fmt_fontsize,
            verticalalignment = 'center',
            horizontalalignment = 'left')

    return


# This function is used to extract discrimination data from simulated input ER and NR signatures.
# I.e. the input signatures are sliced into bins (according to 'flag_slicing') and every subset of data is then analyzed in terms of leakage.
def get_discrdata_from_simdata(
    input_er_data,
    input_nr_data,
    bin_edges,
    threshold_events_per_bin = 20,
    nr_acceptances = [50, 85], # former: leakage_fraction_percentile
    savestring = "",
    flag_slicing = ["s1_g1", "er_ee"][1],
    flag_returnsubdatasets = True,
    **kwargs
):

    # definitions
    # bins
    bin_width = bin_edges[1] -bin_edges[0]
    bin_centers = [bin_edges[i] +0.5*(bin_edges[i+1] -bin_edges[i]) for i in range(len(bin_edges)-1)]
    # output data
    popdata_dtype = [
        ("bin_center", np.float64)]
    for i in range(len(nr_acceptances)):
        nracc_add_string = "nracc_" +f"{nr_acceptances[i]:.1f}".replace(".","_") +"__"
        popdata_dtype = popdata_dtype +[
            (nracc_add_string +"threshold_value", np.float64),
            (nracc_add_string +"discriminationline_x_left", np.float64),
            (nracc_add_string +"discriminationline_x_right", np.float64),
            (nracc_add_string +"n_nr_events_in_bin", np.uint64),
            (nracc_add_string +"n_er_events_in_bin", np.uint64),
            (nracc_add_string +"n_er_events_below_threshold", np.uint64),
            (nracc_add_string +"leakage_fraction_in_bin", np.float64),
            (nracc_add_string +"leakage_fraction_in_bin_error", np.float64)]
    popdata_tuple_list = []
    sliced_data_er = []
    sliced_data_nr = []

    # looping over the bins/slices to generate 'popdata' data and add it to the 'popdata_tuple_list'
    for j in range(len(bin_edges)-1):

        # selecting the data corresponding to the current bin/slice
        if flag_slicing == "er_ee":
            er_bin_data = input_er_data[
                (input_er_data["s2_phe"] >= ((kwargs["g2"]/kwargs["w"])*bin_edges[j]*1000) -((kwargs["g2"]/kwargs["g1"])*input_er_data["s1_phe"]) ) &
                (input_er_data["s2_phe"] <= ((kwargs["g2"]/kwargs["w"])*bin_edges[j+1]*1000) -((kwargs["g2"]/kwargs["g1"])*input_er_data["s1_phe"]))]
            nr_bin_data = input_nr_data[
                (input_nr_data["s2_phe"] >= ((kwargs["g2"]/kwargs["w"])*bin_edges[j]*1000) -((kwargs["g2"]/kwargs["g1"])*input_nr_data["s1_phe"]) ) &
                (input_nr_data["s2_phe"] <= ((kwargs["g2"]/kwargs["w"])*bin_edges[j+1]*1000) -((kwargs["g2"]/kwargs["g1"])*input_nr_data["s1_phe"]))]
        elif flag_slicing == "s1_g1": # this I still need to implement
            er_bin_data = input_er_data
            nr_bin_data = input_nr_data
        else:
            raise Exception("undefined 'flag_slicing'")
            
        # extracting data from to the current bin/slice
        n_nr = len(nr_bin_data) # <--- popdata: "n_nr_events_in_bin"
        n_er = len(er_bin_data) # <--- popdata: "n_er_events_in_bin"

        # checking whether there are sufficient events within the current bin/slice
        if (n_er > threshold_events_per_bin) and (n_nr > threshold_events_per_bin):

            # looping over all NR acceptances
            popdata_tuple = (bin_edges[j]+0.5*bin_width, )
            for k in range(len(nr_acceptances)):

                # calculating the leakage beneath the threshold
                percentile_index = int(len(nr_bin_data)*(nr_acceptances[k]/100)) # number of events for an NR acceptance of 'nr_acceptances[k]'
                percentile_threshold_value = sorted(list(nr_bin_data["log_s2_s1"]))[percentile_index] # 'log_s2_s1' value corresponding to the NR acceptance defined above
                n_er_below_threshold = len(er_bin_data[(er_bin_data["log_s2_s1"] <= percentile_threshold_value)]) # <--- popdata: "n_er_events_below_threshold"
                leakage_fraction_within_current_bin = n_er_below_threshold/n_er # <--- popdata: "leakage_fraction_in_bin"
                leakage_fraction_within_current_bin_error = np.sqrt(n_er_below_threshold)/n_er # <--- popdata: "leakage_fraction_in_bin_error"

                # calculating the x values of the discrimination line for the log_s2_s1 over s1_g1 observable space
                if flag_slicing == "er_ee":
                    c_star = 10**(percentile_threshold_value)
                    first_factor_low = (1/c_star) *(kwargs["g2"]/(kwargs["w"]*kwargs["g1"])) *bin_edges[j]*1000
                    first_factor_high = (1/c_star) *(kwargs["g2"]/(kwargs["w"]*kwargs["g1"])) *bin_edges[j+1]*1000
                    second_factor = 1/(1 +(1/c_star)*(kwargs["g2"]/kwargs["g1"]))
                    discrline_x_left = first_factor_low *second_factor
                    discrline_x_right = first_factor_high *second_factor
                elif flag_slicing == "s1_g1":
                    a = 3
                else:
                    raise Exception("invalid 'flag_slicing'")

                # adding data to the 'popdata_tuple'
                popdata_tuple = popdata_tuple +(
                    percentile_threshold_value,
                    discrline_x_left,
                    discrline_x_right,
                    n_nr,
                    n_er,
                    n_er_below_threshold,
                    leakage_fraction_within_current_bin,
                    leakage_fraction_within_current_bin_error)

            # adding data to the 'popdata_tuple_list'
            popdata_tuple_list.append(popdata_tuple)

        # saving the subdatasets
        if flag_returnsubdatasets == True:
            sliced_data_nr.append(nr_bin_data)
            sliced_data_er.append(er_bin_data)

    # generating the output 'popdata' ndarray
    popdata_ndarray = np.array(popdata_tuple_list, popdata_dtype)
    if savestring != "":
        np.save(savestring, popdata_ndarray)

    # end of program: returning stuff
    if flag_returnsubdatasets == True:
        return popdata_ndarray, sliced_data_nr, sliced_data_er
    else:
        return popdata_ndarray


# This function is used to calculate the total rejection for a given set of popdata.
def calc_total_rejection_from_simdata(
    input_popdata,
    nr_acceptance,
    flag_definition = [
        "total_number_of_ers_above_discrimination_line",
        "number_of_ers_above_discrimination_line_weighted_by_nrs_in_bin"]
        [1]):
    
    # determining the dataset corresponding to the given NR acceptance
    nr_acc_addstring = "nracc_" +f"{nr_acceptance:.1f}".replace(".","_") +"__"

    # calculating the total ER rejection depending on the given 'flag_definition'
    total_er_rejection = 0

    if flag_definition == "total_number_of_ers_above_discrimination_line":
        n_ers_in_total = 0
        for i in range(len(input_popdata)):
            n_ers_in_total = n_ers_in_total +input_popdata[i][nr_acc_addstring +"n_er_events_in_bin"]
            total_er_rejection = total_er_rejection +(input_popdata[i][nr_acc_addstring +"n_er_events_in_bin"] -input_popdata[i][nr_acc_addstring +"n_er_events_below_threshold"])
        total_er_rejection = total_er_rejection/n_ers_in_total *100
        return total_er_rejection
        
    elif flag_definition == "number_of_ers_above_discrimination_line_weighted_by_nrs_in_bin":
        n_nrs_in_total = 0
        for i in range(len(input_popdata)):
            n_nrs_in_total = n_nrs_in_total +input_popdata[i][nr_acc_addstring +"n_nr_events_in_bin"]
            total_er_rejection = total_er_rejection +((input_popdata[i][nr_acc_addstring +"n_er_events_in_bin"]-input_popdata[i][nr_acc_addstring +"n_er_events_below_threshold"])/input_popdata[i][nr_acc_addstring +"n_er_events_in_bin"]*input_popdata[i][nr_acc_addstring +"n_nr_events_in_bin"])
        total_er_rejection = total_er_rejection/n_nrs_in_total *100
        return total_er_rejection

    else:
        raise Exception("invalid 'flag_definition'")


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



