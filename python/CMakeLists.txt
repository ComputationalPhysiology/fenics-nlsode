cmake_minimum_required(VERSION 3.16)

project(nlsode_pybind11 VERSION "0.1.0"  LANGUAGES CXX)

include(GNUInstallDirs)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Python3
if(${CMAKE_VERSION} VERSION_GREATER_EQUAL "3.18.0")
  find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)
else()
  find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
endif()

# Find DOLFIN
find_path(dolfin_INCLUDE_DIR dolfin.h)
message(STATUS "dolfin header found at: ${dolfin_INCLUDE_DIR}")
include_directories(${DOLFIN_INCLUDE_DIR})

find_library(dolfin_LIB dolfin)
message(STATUS "libdolfin found at: ${dolfin_LIB}")

mark_as_advanced(dolfin_INCLUDE_DIR dolfin_LIB)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(dolfin REQUIRED_VARS
  dolfin_INCLUDE_DIR
  dolfin_LIB
  )

# Find UFC (part of FFC)
execute_process(
  COMMAND ${Python3_EXECUTABLE} -c
  "import ffc, sys; sys.stdout.write(ffc.backends.ufc.get_include_path())"
  OUTPUT_VARIABLE UFC_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)

message(STATUS "libufc found at: ${UFC_INCLUDE_DIR}")
include_directories(${UFC_INCLUDE_DIR})

if (UFC_INCLUDE_DIR)
  set(UFC_INCLUDE_DIRS ${UFC_INCLUDE_DIR} CACHE STRING "Where to find ufc.h")
  mark_as_advanced(UFC_INCLUDE_DIRS)

  execute_process(
    COMMAND ${Python3_EXECUTABLE} -c "import ffc, sys; sys.stdout.write(ffc.__version__)"
    OUTPUT_VARIABLE UFC_VERSION
    )
  mark_as_advanced(UFC_VERSION)

  if (UFC_FIND_VERSION)
    # Check if version found is >= required version
    if (NOT "${UFC_VERSION}" VERSION_LESS "${UFC_FIND_VERSION}")
      set(UFC_VERSION_OK TRUE)
    endif()
  else()
    # No specific version requested
    set(UFC_VERSION_OK TRUE)
  endif()
  mark_as_advanced(UFC_VERSION_OK)

  execute_process(
    COMMAND ${Python3_EXECUTABLE} -c "import ffc, sys; sys.stdout.write(ffc.ufc_signature())"
    OUTPUT_VARIABLE UFC_SIGNATURE
    )
  mark_as_advanced(UFC_SIGNATURE)

endif()

# Standard package handling
find_package_handle_standard_args(UFC
                                  "UFC could not be found."
                                  UFC_INCLUDE_DIRS
                                  UFC_VERSION
                                  UFC_VERSION_OK
                                  UFC_SIGNATURE)

# set_package_properties(UFC PROPERTIES TYPE REQUIRED
#   DESCRIPTION "Unified language for form-compilers (part of FFC)"
#   URL "https://bitbucket.org/fenics-project/ffc")
# include_directories(${UFC_INCLUDE_DIRS})

# See https://gitlab.kitware.com/cmake/cmake/-/issues/16414
if (TARGET nlsode)
  add_library(Nlsode::nlsode ALIAS nlsode)
else()
  # Find Goss (C++)
  find_package(Nlsode REQUIRED)
endif()

if(SKBUILD)
  # Scikit-Build does not add your site-packages to the search path
  # automatically, so we need to add it or the pybind11 specific
  # directory here.
  
  execute_process(
    COMMAND
      "${Python3_EXECUTABLE}" -c
      "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _tmp_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
endif()

find_package(pybind11 REQUIRED CONFIG HINTS ${PYBIND11_DIR} ${PYBIND11_ROOT}
  $ENV{PYBIND11_DIR} $ENV{PYBIND11_ROOT})

set(python_module_name _nlsodecpp)

# Headers included from dolfin
#include_directories(${DOLFIN_INCLUDE_DIRS})
#include_directories(SYSTEM ${DOLFIN_3RD_PARTY_INCLUDE_DIRS})

# Create the binding library
pybind11_add_module(_nlsodecpp MODULE wrapper.cpp)
target_link_libraries(_nlsodecpp PRIVATE Nlsode::nlsode)
#target_link_libraries(_nlsodecpp PRIVATE ${DOLFIN_LIBRARIES})

# Add strict compiler flags
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-Wall -Werror  -Wextra -Wno-comment -pedantic" HAVE_PEDANTIC)
if (HAVE_PEDANTIC)
  target_compile_options(_nlsodecpp PRIVATE -Wall;-Wextra;-Werror;-Wno-comment;-pedantic)
endif()

# In Debug mode override pybind11 symbols visibility. Symbols must be
# visible to backtrace_symbols() to produce nice logs
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
  target_compile_options(_nlsodecpp PRIVATE "-fvisibility=default")
endif()

# scikit-build specific steps
if (SKBUILD)
  # Add relative rpath so _nlsodecpp can find the Nlsode::nlsode libray
  # when the build is relocated
  if (APPLE)
    set_target_properties(_nlsodecpp PROPERTIES INSTALL_RPATH "@loader_path/lib")
  else()
    set_target_properties(_nlsodecpp PROPERTIES INSTALL_RPATH "$ORIGIN/lib")
  endif()

  install(TARGETS _nlsodecpp DESTINATION .)
endif()
