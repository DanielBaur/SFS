# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/nest

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/build

# Include any dependencies generated for this target.
include CMakeFiles/execNEST.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/execNEST.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/execNEST.dir/flags.make

CMakeFiles/execNEST.dir/src/execNEST.cpp.o: CMakeFiles/execNEST.dir/flags.make
CMakeFiles/execNEST.dir/src/execNEST.cpp.o: /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/nest/src/execNEST.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/execNEST.dir/src/execNEST.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/execNEST.dir/src/execNEST.cpp.o -c /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/nest/src/execNEST.cpp

CMakeFiles/execNEST.dir/src/execNEST.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/execNEST.dir/src/execNEST.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/nest/src/execNEST.cpp > CMakeFiles/execNEST.dir/src/execNEST.cpp.i

CMakeFiles/execNEST.dir/src/execNEST.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/execNEST.dir/src/execNEST.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/nest/src/execNEST.cpp -o CMakeFiles/execNEST.dir/src/execNEST.cpp.s

CMakeFiles/execNEST.dir/src/execNEST.cpp.o.requires:

.PHONY : CMakeFiles/execNEST.dir/src/execNEST.cpp.o.requires

CMakeFiles/execNEST.dir/src/execNEST.cpp.o.provides: CMakeFiles/execNEST.dir/src/execNEST.cpp.o.requires
	$(MAKE) -f CMakeFiles/execNEST.dir/build.make CMakeFiles/execNEST.dir/src/execNEST.cpp.o.provides.build
.PHONY : CMakeFiles/execNEST.dir/src/execNEST.cpp.o.provides

CMakeFiles/execNEST.dir/src/execNEST.cpp.o.provides.build: CMakeFiles/execNEST.dir/src/execNEST.cpp.o


# Object files for target execNEST
execNEST_OBJECTS = \
"CMakeFiles/execNEST.dir/src/execNEST.cpp.o"

# External object files for target execNEST
execNEST_EXTERNAL_OBJECTS =

execNEST: CMakeFiles/execNEST.dir/src/execNEST.cpp.o
execNEST: CMakeFiles/execNEST.dir/build.make
execNEST: libCore.a
execNEST: CMakeFiles/execNEST.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable execNEST"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/execNEST.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/execNEST.dir/build: execNEST

.PHONY : CMakeFiles/execNEST.dir/build

CMakeFiles/execNEST.dir/requires: CMakeFiles/execNEST.dir/src/execNEST.cpp.o.requires

.PHONY : CMakeFiles/execNEST.dir/requires

CMakeFiles/execNEST.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/execNEST.dir/cmake_clean.cmake
.PHONY : CMakeFiles/execNEST.dir/clean

CMakeFiles/execNEST.dir/depend:
	cd /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/nest /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/nest /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/build /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/build /home/daniel/Desktop/arbeitsstuff/20180706__sfs/NEST__20200828__v2_1_0/build/CMakeFiles/execNEST.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/execNEST.dir/depend
