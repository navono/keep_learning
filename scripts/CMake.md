# CMake

## 参数

```
-DCMAKE_INSTALL_PREFIX=D:\data\lib
-DCMAKE_TOOLCHAIN_FILE=%VCPKG_ROOT%/scripts/buildsystems/vcpkg.cmake

cmake .. -G "Visual Studio 17 2022" -DBUILD_SHARED_LIBS=SHARED -DCMAKE_BUILD_TYPE=Debug
cmake .. -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Debug
```

## 命令

```
cmake --build . --config Debug
cmake --build . --config Release
```

```
macro(RemoveDebugCXXFlag flag)
string(REPLACE "${flag}" "" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
string(REPLACE "${flag}" "" CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG}")
endmacro()

macro(RemoveReleaseCXXFlag flag)
string(REPLACE "${flag}" "" CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE}")
string(REPLACE "${flag}" "" CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE}")
endmacro()

RemoveDebugCXXFlag("/RTCs")
RemoveDebugCXXFlag("/RTC1")
RemoveDebugCXXFlag("/RTCc")
RemoveDebugCXXFlag("/RTCu")

RemoveReleaseCXXFlag("/RTCs")
RemoveReleaseCXXFlag("/RTC1")
RemoveReleaseCXXFlag("/RTCc")
RemoveReleaseCXXFlag("/RTCu")
```