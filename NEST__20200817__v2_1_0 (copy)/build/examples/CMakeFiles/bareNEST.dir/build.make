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
CMAKE_SOURCE_DIR = /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/nest

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build

# Include any dependencies generated for this target.
include examples/CMakeFiles/bareNEST.dir/depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/bareNEST.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/bareNEST.dir/flags.make

examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o: examples/CMakeFiles/bareNEST.dir/flags.make
examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o: /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/nest/examples/bareNEST.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o"
	cd /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/examples && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/bareNEST.dir/bareNEST.cpp.o -c /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/nest/examples/bareNEST.cpp

examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/bareNEST.dir/bareNEST.cpp.i"
	cd /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/nest/examples/bareNEST.cpp > CMakeFiles/bareNEST.dir/bareNEST.cpp.i

examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/bareNEST.dir/bareNEST.cpp.s"
	cd /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/nest/examples/bareNEST.cpp -o CMakeFiles/bareNEST.dir/bareNEST.cpp.s

examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o.requires:

.PHONY : examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o.requires

examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o.provides: examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o.requires
	$(MAKE) -f examples/CMakeFiles/bareNEST.dir/build.make examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o.provides.build
.PHONY : examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o.provides

examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o.provides.build: examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o


# Object files for target bareNEST
bareNEST_OBJECTS = \
"CMakeFiles/bareNEST.dir/bareNEST.cpp.o"

# External object files for target bareNEST
bareNEST_EXTERNAL_OBJECTS =

examples/bareNEST: examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o
examples/bareNEST: examples/CMakeFiles/bareNEST.dir/build.make
examples/bareNEST: libCore.a
examples/bareNEST: examples/CMakeFiles/bareNEST.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable bareNEST"
	cd /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/bareNEST.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/bareNEST.dir/build: examples/bareNEST

.PHONY : examples/CMakeFiles/bareNEST.dir/build

examples/CMakeFiles/bareNEST.dir/requires: examples/CMakeFiles/bareNEST.dir/bareNEST.cpp.o.requires

.PHONY : examples/CMakeFiles/bareNEST.dir/requires

examples/CMakeFiles/bareNEST.dir/clean:
	cd /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/examples && $(CMAKE_COMMAND) -P CMakeFiles/bareNEST.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/bareNEST.dir/clean

examples/CMakeFiles/bareNEST.dir/depend:
	cd /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/nest /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/nest/examples /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/examples /home/daniel/Desktop/arbeitsstuff/SFS/NEST__20200817__v2_1_0/build/examples/CMakeFiles/bareNEST.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/bareNEST.dir/depend
