cmake_minimum_required(VERSION 3.23)
project(cudaBasic CUDA)
set(CMAKE_CUDA_STANDARD 14)

find_package(CUDA REQUIRED)
get_filename_component(CUDA_LIB_DIR ${CUDA_LIBRARIES} DIRECTORY)
set(CMAKE_CUDA_COMPILER ${CUDA_INCLUDE_DIRS}../bin/nvcc.exe)

add_executable(cudaBasic main.cu)
set_target_properties(cudaBasic PROPERTIES CUDA_SEPARABLE_COMPILATION ON)