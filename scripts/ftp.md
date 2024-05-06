# Windows Batch

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

rem 确保 HOUR 和 MINUTE 是两位数
if %HOUR% LSS 10 set HOUR=0%HOUR%
REM if %MINUTE% LSS 10 set MINUTE=0%MINUTE%

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

cd ../out

set FTP_HOST=10.30.28.170
set FTP_PORT=12121
set FTP_USER=admin
set FTP_PASS=
set FTP_DIR=ConfigGen
set LATEST_ZIP_FILE=latest
set LATEST_FILE=latest_web

rem 上传最新的压缩包到 FTP 服务器
set FTP_COMMAND_FILE=ftp.txt
echo open %FTP_HOST% %FTP_PORT% > %FTP_COMMAND_FILE%
echo user %FTP_USER% %FTP_PASS% >> %FTP_COMMAND_FILE%
echo cd %FTP_DIR% >> %FTP_COMMAND_FILE%

echo put %LATEST_FILE% /%FTP_DIR%/%LATEST_FILE% >> %FTP_COMMAND_FILE%

REM echo put %LATEST_ZIP_FILE% >> %FTP_COMMAND_FILE%
for %%f in (%LATEST_ZIP_FILE%\*.zip) do (
  echo put %%f /%FTP_DIR%/%%~nxf >> %FTP_COMMAND_FILE%
)

echo bye >> %FTP_COMMAND_FILE%
ftp -n -s:%FTP_COMMAND_FILE%

rem 清理临时文件
REM del %FTP_COMMAND_FILE%

endlocal
```

从 FPT 服务下载 latest 文件中指定的文件：

```
echo off

set FTP_HOST=10.30.28.170
set FTP_PORT=12121
set FTP_USER=admin
set FTP_PASS=admin
set FTP_DIR=ConfigGen
set LATEST_FILE=latest_web

set FTP_COMMAND_FILE=%TEMP%\ftp.txt
set DEST_FILE_DIR=ConfigGen

:: 创建临时目录
mkdir "%TEMP_DIR%" 2>nul

call:downloadFile %LATEST_FILE%

rem 读取 latest 文件中的内容
set /p LATEST_FILE_NAME=<%LATEST_FILE%
echo %LATEST_FILE_NAME%

call:downloadFile %LATEST_FILE_NAME%

del "%LATEST_FILE%"

"C:\Program Files\7-Zip\7z.exe" x "ConfigGen_20240415-1708.zip" -o"./"

rem 使用 xcopy 命令将源目录及其内容复制到目标目录
xcopy "ConfigGenWeb\*" "ConfigGen\ConfigGenWeb" /s /e /y /i
xcopy "ConfigGenServer\*" "ConfigGen\ConfigGenServer" /s /e /y /i
rmdir /s /q "ConfigGenWeb" "ConfigGenServer"

goto :EOF

:downloadFile
echo open %FTP_HOST% %FTP_PORT% > %FTP_COMMAND_FILE%
echo user %FTP_USER% %FTP_PASS% >> %FTP_COMMAND_FILE%
echo cd %FTP_DIR% >> %FTP_COMMAND_FILE%
echo get %1 >> %FTP_COMMAND_FILE%
echo bye >> %FTP_COMMAND_FILE%
ftp -n -s:%FTP_COMMAND_FILE%

del %FTP_COMMAND_FILE%
goto:eof

```

# Win 11 文件夹浏览器

如果在文件夹浏览器无法打开 ftp 服务，可尝试在

```
系统设置 -> 网络和 Internet ->  Internet 选项 -> 高级

将【使用被动 FTP（用于防火墙和 DSL 调制解调器的兼容）】选项去勾选
```
