cmake_minimum_required(VERSION 3.24)
project(otclient_tibia_runtime_bridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Qt6 6.4 REQUIRED COMPONENTS Core)
find_package(Threads REQUIRED)

add_library(otclient_tibia_runtime_bridge SHARED bridge.cpp)
target_link_libraries(otclient_tibia_runtime_bridge PRIVATE Qt6::Core Threads::Threads ${CMAKE_DL_LIBS})
target_compile_options(otclient_tibia_runtime_bridge PRIVATE -Wall -Wextra -Wpedantic -Werror)
set_target_properties(otclient_tibia_runtime_bridge PROPERTIES
    PREFIX ""
    OUTPUT_NAME "otclient-tibia-runtime-bridge"
)
