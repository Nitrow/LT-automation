cmake_minimum_required(VERSION 3.0.0)
project(testcode5 VERSION 0.1.0)

include(CTest)
enable_testing()

find_package(ur_rtde REQUIRED)

add_executable(testcode5 main.cpp)

target_link_libraries(testcode5 PRIVATE ur_rtde::rtde)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
