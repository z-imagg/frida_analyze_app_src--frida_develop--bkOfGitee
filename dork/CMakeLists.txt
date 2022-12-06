cmake_minimum_required(VERSION 3.0)
project(experiment)

set(CMAKE_CXX_STANDARD 14)
#set(CMAKE_BUILD_TYPE RELEASE)
set(CMAKE_BUILD_TYPE DEBUG)
add_executable(dork main.cpp ZUser.cpp ZUser.h)
