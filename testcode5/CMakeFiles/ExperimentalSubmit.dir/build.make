# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

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
CMAKE_SOURCE_DIR = /home/asger/arbejde/testcode5

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/asger/arbejde/testcode5

# Utility rule file for ExperimentalSubmit.

# Include the progress variables for this target.
include CMakeFiles/ExperimentalSubmit.dir/progress.make

CMakeFiles/ExperimentalSubmit:
	/usr/bin/ctest -D ExperimentalSubmit

ExperimentalSubmit: CMakeFiles/ExperimentalSubmit
ExperimentalSubmit: CMakeFiles/ExperimentalSubmit.dir/build.make

.PHONY : ExperimentalSubmit

# Rule to build all files generated by this target.
CMakeFiles/ExperimentalSubmit.dir/build: ExperimentalSubmit

.PHONY : CMakeFiles/ExperimentalSubmit.dir/build

CMakeFiles/ExperimentalSubmit.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ExperimentalSubmit.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ExperimentalSubmit.dir/clean

CMakeFiles/ExperimentalSubmit.dir/depend:
	cd /home/asger/arbejde/testcode5 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/asger/arbejde/testcode5 /home/asger/arbejde/testcode5 /home/asger/arbejde/testcode5 /home/asger/arbejde/testcode5 /home/asger/arbejde/testcode5/CMakeFiles/ExperimentalSubmit.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ExperimentalSubmit.dir/depend

