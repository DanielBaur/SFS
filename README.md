
<h1><center> Signal Formation Simulation </center></h1>
<br>
<br>
<br>

Last Modified: By Daniel Baur on 13th February 2020

Signal Formation Simulation (SFS) is a Python (Python3) script meant process (arbitrary/MC/WIMP/etc...) recoil spectra (i.e. either generated manually or via MC simulations) into the S1/S2 signature within a LXe TPC detector such as DARWIN (in PE/phd) utilizing NEST (NESTv2.0.1). It consists of three main components:
* Master Signal Formation (MSF.py): coordinate the SF instance
* Signal Formation (SF.py): main code, process specified spectra within a specified detector using NEST
* Process Signal Formation (PSF.ipynb): analyse the data generated with SF
<br>
<br>

### Table of Contents

0. **[Setup](#0.-Setup)**<br>
    0.1 [NEST](#0.1-NEST)<br>
    0.2 [SFS](#0.2-SFS)


1. **[Introduction](#1.-Introduction)**<br>


2. **[Usage](#2.-Usage)**<br>
    2.1 [Detector Modification](#2.1-Detector-Modification)<br>
    2.2 [Spectra Generation](#2.2-Spectra-Generation)<br>
    2.3 [Processing](#2.3-Processing)


3. **[Troubleshooting](#3.-Troubleshooting)**<br>

<br>
<br>
<br>

# 0. Setup

The following sections are meant to provide documentation on how to set up both NEST and also the SFS wrapper.

<br>

## 0.1 NEST

NEST (Noble Element Simulation Technique) is a simulation tool for scintillation, ionization and electroluminescence processes. Its main applications are various simulation capabilities for experimental dark matter searches. The working principle is based on parameterizing expressions for physical quantities (e.g. charge yield, relative scintillation efficiency, etcg.) based on current experimental results. The code is written in C++ and maintained by the NEST collaboration (see: [--> the official NEST website <--](http://nest.physics.ucdavis.edu/)). SFS is essentially a framework so NEST can be used to automatically process arbitrary recoil spectra.

For the installation check out [--> the NEST repository on GitHub <--](https://github.com/NESTCollaboration/nest) along with [--> the documentation on GitHub <--](https://github.com/NESTCollaboration/nest/blob/master/README.md).

1. First create a new directory and within that git clone the repository:<br>`$ git clone https://personal_username@github.com/NESTCollaboration/nest.git`

2. Then create the `build` and `install` directories - but make sure they are on the same level as the `nest` directory. I.e. from within the git cloned `nest` directory execute:<br>`$ mkdir ../build; mkdir ../install; cd ../build`

3. From within the 'build' directory configure cmake:<br>`$ cmake -DCMAKE_INSTALL_PREFIX=./../install ../nest`

4. And finally execute the following within the build directory:<br>`$ make; make install`

<br>

## 0.2 SFS

Download the program from [--> the SFS GitHub repository <--](https://github.com/DanielBaur/SFS) by executing

`$ git clone https://github.com/DanielBaur/SFS.git`

within your target folder. All you still need to do is to enter the path to your instance of the `testNEST` executable in `SF.py`. The `testNEST` executable should be in the `install` folder within your instance of NEST; i.e. change the following line in `SF.py`

`# ---> Insert the path to your testNEST executable here! <---
path_testnest = "/scratch/db1086/NEST2/install/"`

<br>
<br>
<br>
<br>

# 1. Introduction

<br>
<br>
<br>
<br>

# 2. Usage

Execute the `SF.py` file by

`$ Python3 SF.py -d <detectorname> -s <spectrumname>` .

The detector specified by `<detectorname>` (in the `input_detecotrs` folder) is implemented in NEST and afterwards the spectrum specified by `<spectrumname>` (in the `input_spectra`) is forwarded and processed by NEST. The output is stored in the `output_sf` folder.

<br>

## 2.1 Detector Modification

In NEST a detector is specified by modifying the `Detector.hh` and implementing it into the NEST source code. The `SF.py` code does that automatically: In the `input_detectors` folder just generate a new detector file from the `detector_template.txt` file, edit the parameters therein and forward its (altered and unique (!)) name to the `SF.py` call (see above) as the `<detectorname>` flag.

<br>

## 2.2 Spectra Generation

Processing some arbitrary spectrum with NEST.

<br>

## 2.3 Processing

<br>
<br>
<br>
<br>

# 3. Troubleshooting

Please note that the SFS script was neither conceptualized specifically for the DARWIN collaboration nor the broad public. It was developed for my personal work in the context of my Ph.D. studies. Accordingly all credit should be adressed directly towards the NEST collaboration (please also note the appropriate citation on [--> the documentation on GitHub <--](https://github.com/NESTCollaboration/nest/blob/master/README.md)). Also I cannot guarantee a fully functional program in any way, shape or form. For bug reports, general questions or other suggestions please contact me directly via email: <daniel.baur@physik.uni-freiburg.de>.

