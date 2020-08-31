#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "NEST::Core" for configuration ""
set_property(TARGET NEST::Core APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(NEST::Core PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libCore.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS NEST::Core )
list(APPEND _IMPORT_CHECK_FILES_FOR_NEST::Core "${_IMPORT_PREFIX}/lib/libCore.a" )

# Import target "NEST::testNEST" for configuration ""
set_property(TARGET NEST::testNEST APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(NEST::testNEST PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/testNEST"
  )

list(APPEND _IMPORT_CHECK_TARGETS NEST::testNEST )
list(APPEND _IMPORT_CHECK_FILES_FOR_NEST::testNEST "${_IMPORT_PREFIX}/bin/testNEST" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
