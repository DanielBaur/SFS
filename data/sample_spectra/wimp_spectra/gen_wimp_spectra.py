


##################################################################
##### Imports ####################################################
##################################################################


import numpy as np
import datetime
import os
import subprocess





##################################################################
##### Running the C++ File #######################################
##################################################################


# sourcing root
#subprocess.call("rootybooty", shell=True)


# executing the .cpp file using root
subprocess.call("root -q -l 'xenon_limits_mod.cpp(40.,1e-47)'", shell=True)





