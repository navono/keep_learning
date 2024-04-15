删除、拷贝文件夹

```batch
rmdir /s /q "../out/VFConfigGen"
mkdir "../out"
xcopy /s /e /i "./bin" "../out/VFConfigGen"
```

压缩文件夹

```batch
chcp 65001
@echo off
setlocal

rem 使用 wmic 命令获取标准化日期格式
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do (
    set "datetime=%%i"
    goto :parse_date
)

:parse_date
set "date=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%"

set CURRENT_TIME=%TIME%
set HOUR=%CURRENT_TIME:~0,2%
set MINUTE=%CURRENT_TIME:~3,2%

if %HOUR% LSS 10 set HOUR=0%HOUR%

set latestZipName="ConfigGen_%date%-%HOUR%%MINUTE%.zip"
cd ../out
"../tools/7z/7z.exe" a -tzip %latestZipName% "./ConfigGen/ConfigGenServer" "./ConfigGen/ConfigGenWeb"

set latestZipDir="./latest"
rmdir /s /q %latestZipDir%
mkdir %latestZipDir%

xcopy %latestZipName% %latestZipDir%
del %latestZipName%

set LATEST_FILE=latest_web

rem 将最新的压缩包文件名写入到 latest 文件
echo %latestZipName% > %LATEST_FILE%

endlocal
```

上传文件到 FTP 服务

```
chcp 65001
@echo off
setlocal

set FTP_HOST=10.30.28.170
set FTP_PORT=12121
set FTP_USER=admin
set FTP_PASS=admin
set FTP_DIR=ConfigGen
set LATEST_ZIP_FILE="../out/latest/*.zip"
set LATEST_FILE="../out/latest_web"

rem 上传最新的压缩包到 FTP 服务器
set FTP_COMMAND_FILE=%TEMP%\ftp.txt
echo open %FTP_HOST% %FTP_PORT% > %FTP_COMMAND_FILE%
echo user %FTP_USER% %FTP_PASS% >> %FTP_COMMAND_FILE%
echo cd %FTP_DIR% >> %FTP_COMMAND_FILE%
echo put %LATEST_FILE% >> %FTP_COMMAND_FILE%
echo put %LATEST_ZIP_FILE% >> %FTP_COMMAND_FILE%
echo bye >> %FTP_COMMAND_FILE%
ftp -n -s:%FTP_COMMAND_FILE%

rem 清理临时文件
del %FTP_COMMAND_FILE%

endlocal
```

从 FPT 服务下载 latest 文件中指定的文件：

```
echo off

set FTP_HOST=10.30.76.161
set FTP_USER=admin
set FTP_PASS=admin
set FTP_DIR=ConfigGen
set LATEST_FILE=latest
set TEMP_DIR=%TEMP%\ConfigGen

:: 创建临时目录
mkdir "%TEMP_DIR%" 2>nul

call:downloadFile %LATEST_FILE%

rem 读取 latest 文件中的内容
set /p LATEST_FILE_NAME=<%LATEST_FILE%
echo %LATEST_FILE_NAME%

call:downloadFile %LATEST_FILE_NAME%

del "%LATEST_FILE%"
goto :EOF

:downloadFile
echo user %FTP_USER% %FTP_PASS% > "%TEMP_DIR%\ftp.txt"
echo cd %FTP_DIR% >> "%TEMP_DIR%\ftp.txt"
echo get %1 >> "%TEMP_DIR%\ftp.txt"
echo bye >> "%TEMP_DIR%\ftp.txt"
ftp -n -s:"%TEMP_DIR%\ftp.txt" %FTP_HOST%
del "%TEMP_DIR%\ftp.txt"
goto:eof
```