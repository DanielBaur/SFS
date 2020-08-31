
# - Config file for the NEST package
# It defines the following variables

 
# Compute paths
get_filename_component(NEST_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
set(NEST_INCLUDE_DIRS "/home/daniel/Desktop/arbeitsstuff/NEST4/nest;/home/daniel/Desktop/arbeitsstuff/NEST4/build")
 
# Our library dependencies (contains definitions for IMPORTED targets)
if(NOT NEST_BINARY_DIR)
  include("${NEST_CMAKE_DIR}/NESTTargets.cmake")
endif()
 
# These are IMPORTED targets created by NESTTargets.cmake
set(NEST_LIBRARIES NEST)
