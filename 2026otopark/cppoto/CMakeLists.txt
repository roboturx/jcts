cmake_minimum_required(VERSION 3.10)
project(CppOtopark)

set(CMAKE_CXX_STANDARD 17)

# Find SQLite3
find_package(SQLite3 REQUIRED)

# Add executable
add_executable(${PROJECT_NAME} main.cpp)

# Link libraries
target_link_libraries(${PROJECT_NAME} SQLite::SQLite3)