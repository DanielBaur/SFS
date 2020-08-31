#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "NEST" for configuration ""
set_property(TARGET NEST APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(NEST PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "/home/daniel/Desktop/arbeitsstuff/NEST4/install/lib/libNEST.so"
  IMPORTED_SONAME_NOCONFIG "libNEST.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS NEST )
list(APPEND _IMPORT_CHECK_FILES_FOR_NEST "/home/daniel/Desktop/arbeitsstuff/NEST4/install/lib/libNEST.so" )

# Import target "testNEST" for configuration ""
set_property(TARGET testNEST APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(testNEST PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "/home/daniel/Desktop/arbeitsstuff/NEST4/install/testNEST"
  )

list(APPEND _IMPORT_CHECK_TARGETS testNEST )
list(APPEND _IMPORT_CHECK_FILES_FOR_testNEST "/home/daniel/Desktop/arbeitsstuff/NEST4/install/testNEST" )

# Import target "bareNEST" for configuration ""
set_property(TARGET bareNEST APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(bareNEST PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "/home/daniel/Desktop/arbeitsstuff/NEST4/install/bareNEST"
  )

list(APPEND _IMPORT_CHECK_TARGETS bareNEST )
list(APPEND _IMPORT_CHECK_FILES_FOR_bareNEST "/home/daniel/Desktop/arbeitsstuff/NEST4/install/bareNEST" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
