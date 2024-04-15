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
rem 从标准化日期中提取日期部分
set "date=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%"

rem 输出标准化日期格式
echo Standardized date: %date%

REM 获取当前时间
set CURRENT_TIME=%TIME%

REM 提取小时和分钟
REM 假设时间格式为 HH:MM:SS.SS
REM 使用 %TIME:~0,2% 来提取前两个字符（小时）
set HOUR=%CURRENT_TIME:~0,2%
REM 使用 %TIME:~3,2% 来提取后两个字符（分钟）
set MINUTE=%CURRENT_TIME:~3,2%

REM 如果小时不足两位数，则在前面添加零
if %HOUR% LSS 10 set HOUR=0%HOUR%

cd ../out
"../tools/7z/7z.exe" a -tzip "ConfigGen_%date%-%HOUR%%MINUTE%.zip" "./ConfigGen"

endlocal
```

上传文件到 FTP 服务

```
@echo off

rem 设置变量
set FTP_HOST=10.30.76.161
set FTP_USER=admin
set FTP_PASS=1234
set FTP_DIR=ConfigGen
set LATEST_FILE=latest
set LATEST_FILE_NAME="include.7z"

rem 将最新的压缩包文件名写入到 latest 文件
echo %LATEST_FILE_NAME% > %LATEST_FILE%

rem 上传最新的压缩包到 FTP 服务器
echo user %FTP_USER% %FTP_PASS% > %TEMP%\ftp.txt
echo cd %FTP_DIR% >> %TEMP%\ftp.txt
echo put %LATEST_FILE_NAME% >> %TEMP%\ftp.txt
echo put %LATEST_FILE% >> %TEMP%\ftp.txt
echo bye >> %TEMP%\ftp.txt
ftp -n -s:%TEMP%\ftp.txt %FTP_HOST%

rem 清理临时文件
del %TEMP%\ftp.txt
del latest.txt
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