cmake_minimum_required(VERSION 3.0.0)
project(testcode VERSION 0.1.0)

include(CTest)
enable_testing()

find_package(ur_rtde REQUIRED)

add_executable(testcode main.cpp)

target_link_libraries(testcode PRIVATE ur_rtde::rtde)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
