# Install script for directory: /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/lib/libNEST.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/lib/libNEST.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/lib/libNEST.so"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/lib/libNEST.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/lib" TYPE SHARED_LIBRARY FILES "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/libNEST.so")
  if(EXISTS "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/lib/libNEST.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/lib/libNEST.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/lib/libNEST.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/NEST.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/RandomGen.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/TestSpectra.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/analysis.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/testNEST.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/xoroshiro.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/DetectorExample_XENON10.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/VDetector.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/darwin_firsttest.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/detector_g1__0_17__eLife_us__2300.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1000_g1_0_11.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1000_g1_0_13.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1000_g1_0_133.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1000_g1_0_25.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1500_g1_0_11.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1500_g1_0_13.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1500_g1_0_15.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1500_g1_0_17.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1500_g1_0_25.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1750_g1_0_11.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1750_g1_0_13.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1750_g1_0_15.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_1750_g1_0_17.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2000_g1_0_11.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2000_g1_0_13.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2000_g1_0_15.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2000_g1_0_17.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2000_g1_0_25.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2250_g1_0_11.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2250_g1_0_13.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2250_g1_0_15.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_2250_g1_0_17.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_500_g1_0_11.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/eLife_us_500_g1_0_25.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_11__eLife_us_2200.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_11__eLife_us_2300.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_11_eLife_us_1500.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_11_eLife_us_1750.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_11_eLife_us_2000.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_11_eLife_us_2200_.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_11_eLife_us_2250.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_11_eLife_us_2300_.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_13__eLife_us_2200.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_13__eLife_us_2300.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_13_eLife_us_1500.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_13_eLife_us_1750.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_13_eLife_us_2000.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_13_eLife_us_2200_.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_13_eLife_us_2250.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_13_eLife_us_2300_.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_15__eLife_us_2200.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_15__eLife_us_2300.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_15_eLife_us_1500.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_15_eLife_us_1750.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_15_eLife_us_2000.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_15_eLife_us_2200_.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_15_eLife_us_2250.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_15_eLife_us_2300_.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_17__eLife_us_2200.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_17__eLife_us_2300.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_17_eLife_us_1500.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_17_eLife_us_1750.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_17_eLife_us_2000.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_17_eLife_us_2200_.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_17_eLife_us_2250.hh;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include/g1_0_17_eLife_us_2300_.hh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/include" TYPE FILE FILES
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/NEST/NEST.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/NEST/RandomGen.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/NEST/TestSpectra.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/NEST/analysis.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/NEST/testNEST.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/NEST/xoroshiro.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/DetectorExample_XENON10.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/VDetector.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/darwin_firsttest.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/detector_g1__0_17__eLife_us__2300.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1000_g1_0_11.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1000_g1_0_13.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1000_g1_0_133.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1000_g1_0_25.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1500_g1_0_11.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1500_g1_0_13.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1500_g1_0_15.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1500_g1_0_17.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1500_g1_0_25.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1750_g1_0_11.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1750_g1_0_13.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1750_g1_0_15.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_1750_g1_0_17.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2000_g1_0_11.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2000_g1_0_13.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2000_g1_0_15.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2000_g1_0_17.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2000_g1_0_25.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2250_g1_0_11.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2250_g1_0_13.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2250_g1_0_15.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_2250_g1_0_17.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_500_g1_0_11.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/eLife_us_500_g1_0_25.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_11__eLife_us_2200.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_11__eLife_us_2300.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_11_eLife_us_1500.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_11_eLife_us_1750.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_11_eLife_us_2000.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_11_eLife_us_2200_.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_11_eLife_us_2250.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_11_eLife_us_2300_.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_13__eLife_us_2200.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_13__eLife_us_2300.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_13_eLife_us_1500.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_13_eLife_us_1750.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_13_eLife_us_2000.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_13_eLife_us_2200_.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_13_eLife_us_2250.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_13_eLife_us_2300_.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_15__eLife_us_2200.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_15__eLife_us_2300.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_15_eLife_us_1500.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_15_eLife_us_1750.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_15_eLife_us_2000.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_15_eLife_us_2200_.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_15_eLife_us_2250.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_15_eLife_us_2300_.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_17__eLife_us_2200.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_17__eLife_us_2300.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_17_eLife_us_1500.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_17_eLife_us_1750.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_17_eLife_us_2000.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_17_eLife_us_2200_.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_17_eLife_us_2250.hh"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/nest/include/Detectors/g1_0_17_eLife_us_2300_.hh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/testNEST" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/testNEST")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/testNEST"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/testNEST")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install" TYPE EXECUTABLE FILES "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/testNEST")
  if(EXISTS "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/testNEST" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/testNEST")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/testNEST")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/bareNEST" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/bareNEST")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/bareNEST"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/bareNEST")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install" TYPE EXECUTABLE FILES "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/bareNEST")
  if(EXISTS "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/bareNEST" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/bareNEST")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/bareNEST")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTConfig.cmake;/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTConfigVersion.cmake")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install" TYPE FILE FILES
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/CMakeFiles/NESTConfig.cmake"
    "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/NESTConfigVersion.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets.cmake"
         "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/CMakeFiles/Export/_home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets.cmake")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install" TYPE FILE FILES "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/CMakeFiles/Export/_home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
     "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets-noconfig.cmake")
    if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
        message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
    endif()
    if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
        message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
    endif()
file(INSTALL DESTINATION "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install" TYPE FILE FILES "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/CMakeFiles/Export/_home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/install/NESTTargets-noconfig.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST4/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
