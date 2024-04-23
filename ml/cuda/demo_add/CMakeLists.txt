##################################################    Project     ##################################################
list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
message(STATUS "CMake module path: ${CMAKE_MODULE_PATH}")
message(STATUS "CMake source path: ${CMAKE_SOURCE_DIR}")
include(utils)
include(get_platform)
include(CPM)
include(import_library)
include(assign_source_group)

set(PROJECT_NAME demo_add)
project(${PROJECT_NAME} LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CUDA_STANDARD 17)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


# 编译选项
if (TARGET_PLATFORM_WINDOWS)
    #    add_compile_options(/W4)
    #    add_compile_options(/WX-)
else ()
    add_compile_options(-Wall -Wextra -pedantic)
endif ()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY $<1:${CMAKE_SOURCE_DIR}/bin>)
set(CMAKE_PDB_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/pdb)

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Build platform: ${CMAKE_SYSTEM_NAME}")
message(STATUS "Build output: ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")


##################################################    Sources     ##################################################
file(GLOB_RECURSE PROJECT_HEADERS
        ${PROJECT_SOURCE_DIR}/include/*.h
        ${PROJECT_SOURCE_DIR}/include/*.hpp
        ${CMAKE_SOURCE_DIR}/include/*.h
        ${CMAKE_SOURCE_DIR}/include/*.hpp
        ${CMAKE_SOURCE_DIR}/include/*.ipp)
file(GLOB_RECURSE PROJECT_SOURCES
        ${PROJECT_SOURCE_DIR}/*.c
        ${PROJECT_SOURCE_DIR}/*.cc
        ${PROJECT_SOURCE_DIR}/*.cxx
        ${PROJECT_SOURCE_DIR}/*.cpp
        ${PROJECT_SOURCE_DIR}/*.cu)
file(GLOB_RECURSE PROJECT_CMAKE_UTILS cmake/*.cmake)
file(GLOB_RECURSE PROJECT_MISC *.bat *.gitignore *.md *.py *.sh *.txt)

#if (TARGET_PLATFORM_WINDOWS)
#    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/version.rc.in ${CMAKE_CURRENT_BINARY_DIR}/version.rc @ONLY)
#    list(APPEND PROJECT_SOURCES ${CMAKE_CURRENT_BINARY_DIR}/version.rc)
#    add_compile_definitions(_WINDOWS)
#endif ()

set(PROJECT_FILES
        ${PROJECT_HEADERS}
        ${PROJECT_SOURCES}
        ${PROJECT_CMAKE_UTILS}
        ${PROJECT_MISC})
assign_source_group(${PROJECT_FILES})


##################################################  Dependencies  ##################################################
CPMAddPackage("gh:fmtlib/fmt#10.2.1")
CPMAddPackage(
        NAME spdlog
        GITHUB_REPOSITORY gabime/spdlog
        VERSION 1.13.0
        OPTIONS "SPDLOG_FMT_EXTERNAL ON")

list(APPEND PROJECT_LIBRARIES
        fmt
        spdlog::spdlog)

find_package(CUDA REQUIRED)
get_filename_component(CUDA_LIB_DIR ${CUDA_LIBRARIES} DIRECTORY)
set(CMAKE_CUDA_COMPILER ${CUDA_INCLUDE_DIRS}../bin/nvcc.exe)


#if (TARGET_PLATFORM_WINDOWS)
#    # 设置使用 MFC
#    set(CMAKE_MFC_FLAG 2) # 设置为1表示使用静态链接 MFC 库；2是共享链接 MFC 库
#    set(CMAKE_GENERATOR_PLATFORM Win32)
#
#    list(APPEND PROJECT_LIBRARIES
#            ws2_32.lib
#            psapi.lib
#            iphlpapi.lib)
#endif ()

##################################################    Targets     ##################################################
include_directories(${PROJECT_INCLUDE_DIRS})
link_directories(${PROJECT_LIB_DIR})
link_libraries(${PROJECT_LIBRARIES})

if (TARGET_PLATFORM_WINDOWS)
    # 入口类型：
    # /SUBSYSTEM:WINDOWS
    # /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup
    # /SUBSYSTEM:CONSOLE
    #    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /SUBSYSTEM:WINDOWS")
    #    add_executable(${PROJECT_NAME} WIN32 ${PROJECT_FILES})

    add_executable(${PROJECT_NAME} ${PROJECT_FILES})
else ()
    add_executable(${PROJECT_NAME} ${PROJECT_FILES})
endif ()

target_include_directories(${PROJECT_NAME} PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:include> PRIVATE ..)

target_compile_definitions(${PROJECT_NAME} PUBLIC ${PROJECT_COMPILE_DEFINITIONS})
target_compile_options(${PROJECT_NAME} PUBLIC ${PROJECT_COMPILE_OPTIONS})
set_target_properties(${PROJECT_NAME} PROPERTIES CUDA_SEPARABLE_COMPILATION ON)

if (TARGET_PLATFORM_WINDOWS)
    #    set_target_properties(${PROJECT_NAME} PROPERTIES
    #            VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/bin")
    #    target_compile_definitions(${PROJECT_NAME} PRIVATE
    #            # Prevents Windows.h from adding unnecessary includes
    #            WIN32_LEAN_AND_MEAN
    #            # Prevents Windows.h from defining min/max as macros
    #            NOMINMAX
    #            _CRT_SECURE_NO_WARNINGS)

    # 链接 MFC 库
    #    target_link_libraries(${PROJECT_NAME} PRIVATE
    #            "$<$<CONFIG:Debug>:${MFC_LIB_DEBUG}>"
    #            "$<$<CONFIG:Release>:${MFC_LIB_RELEASE}>")

    #    cmake_host_system_information(RESULT CPU_NUMBER_OF_LOGICAL_CORES QUERY NUMBER_OF_LOGICAL_CORES)
    #    add_compile_options($<$<CXX_COMPILER_ID:MSVC>:/MP${CPU_NUMBER_OF_LOGICAL_CORES}>)
endif ()


##################################################    Postbuild   ##################################################
# copy third party dll
#add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
#        COMMAND ${CMAKE_COMMAND} -E copy
#        $<TARGET_RUNTIME_DLLS:${PROJECT_NAME}>
#        $<TARGET_FILE_DIR:${PROJECT_NAME}>
#        COMMAND_EXPAND_LISTS)

#add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
#        COMMAND ${CMAKE_COMMAND} -E copy_directory
#        ${CMAKE_SOURCE_DIR}/config
#        ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/config)


##################################################  Installation  ##################################################
#install(TARGETS ${PROJECT_NAME} EXPORT ${PROJECT_NAME}-config
#        RUNTIME DESTINATION ../../bin)
#install(DIRECTORY ../../include DESTINATION ../../include)
#install(EXPORT ${PROJECT_NAME}-config DESTINATION ../../cmake)
#export(TARGETS ${PROJECT_NAME} FILE ${PROJECT_NAME}-config.cmake)