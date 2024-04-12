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

