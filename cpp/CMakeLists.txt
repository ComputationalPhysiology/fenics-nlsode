cmake_minimum_required(VERSION 3.16)

# Set the version
project(Nlsode VERSION "0.1.0" LANGUAGES C CXX)
include(GNUInstallDirs)

if (SKBUILD)
  # Always use lib/ in the Python root. Otherwise, environment used for
  # wheels might place in lib64/, which CMake on some systems will not
  # find.
  set(CMAKE_INSTALL_LIBDIR lib)
endif()

include(FeatureSummary)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if (APPLE)
  set(CMAKE_MACOSX_RPATH ON)
endif (APPLE)


# Options
option(BUILD_SHARED_LIBS "Build nlsode with shared libraries." ON)
add_feature_info(BUILD_SHARED_LIBS BUILD_SHARED_LIBS "Build nlsode with shared libraries.")
option(BUILD_TESTS "Build the test suite." OFF)

# find_package(dolfin REQUIRED)
# find_package(goss REQUIRED)
# include(${DOLFIN_USE_FILE})

feature_summary(WHAT ALL)


# Headers included from dolfin
include_directories(SYSTEM ${DOLFIN_INCLUDE_DIRS} 
  ${DOLFIN_3RD_PARTY_INCLUDE_DIRS})


add_library(nlsode)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/nlsode/version.h.in ${CMAKE_CURRENT_SOURCE_DIR}/nlsode/version.h)

set(HEADERS_nlsode
${CMAKE_CURRENT_SOURCE_DIR}/nlsode/NewtonSolver.h
${CMAKE_CURRENT_SOURCE_DIR}/nlsode/version.h)

target_sources(nlsode PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/nlsode/NewtonSolver.cpp)


# Configure the library
set_target_properties(nlsode PROPERTIES PRIVATE_HEADER "${HEADERS_nlsode}")
target_include_directories(nlsode PUBLIC $<INSTALL_INTERFACE:include> "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR};${CMAKE_CURRENT_SOURCE_DIR}>")


# target_link_libraries(nlsode PUBLIC OpenMP::OpenMP_CXX)
target_link_libraries(nlsode PRIVATE ${DOLFIN_LIBRARIES})

# Set compiler flags
list(APPEND NLSODE_DEVELOPER_FLAGS -O2;-g;-pipe)
list(APPEND nlsode_compiler_flags -Wall;-Werror;-Wextra;-Wno-comment;-pedantic)
target_compile_options(nlsode PRIVATE "$<$<OR:$<CONFIG:Debug>,$<CONFIG:Developer>>:${nlsode_compiler_flags}>")
target_compile_options(nlsode PRIVATE $<$<CONFIG:Developer>:${NLSODE_DEVELOPER_FLAGS}>)

# Set debug definitions (private)
target_compile_definitions(nlsode PRIVATE $<$<OR:$<CONFIG:Debug>,$<CONFIG:Developer>>:DEBUG>)

# Install the nlsode library
install(TARGETS nlsode
  EXPORT NlsodeTargets
  PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/nlsode
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT RuntimeExecutables
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT RuntimeLibraries
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT Development)

# Configure CMake helpers
include(CMakePackageConfigHelpers)
write_basic_package_version_file(NlsodeConfigVersion.cmake VERSION ${PACKAGE_VERSION}
  COMPATIBILITY AnyNewerVersion)
configure_package_config_file(NlsodeConfig.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/NlsodeConfig.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/nlsode)

# Install CMake files
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/NlsodeConfig.cmake ${CMAKE_CURRENT_BINARY_DIR}/NlsodeConfigVersion.cmake
  DESTINATION  ${CMAKE_INSTALL_LIBDIR}/cmake/nlsode COMPONENT Development)
install(EXPORT NlsodeTargets FILE NlsodeTargets.cmake NAMESPACE Nlsode::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/nlsode)

if (BUILD_TESTS)
    enable_testing()
    add_subdirectory(${CMAKE_SOURCE_DIR}/tests)
endif()
