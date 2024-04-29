chcp 65001
@echo off
setlocal


rem 使用 wmic 命令获取标准化日期格式
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do (
    set "datetime=%%i"
    goto :parse_date
)

:parse_date
set "date=%datetime:~2,2%%datetime:~4,2%%datetime:~6,2%"

set CURRENT_TIME=%TIME%
set HOUR=%CURRENT_TIME:~0,2%
set MINUTE=%CURRENT_TIME:~3,2%

:: 去除前导空格
set "HOUR=%HOUR: =%"
set "MINUTE=%MINUTE: =%"

:: 补零
if %HOUR% LSS 10 (
    set "HOUR=0%HOUR%"
)
if %MINUTE% LSS 10 (
    set "MINUTE=0%MINUTE%"
)

set LATEST_FILE="ConfigGen-Setup-%date%.exe"


set FTP_HOST=10.30.28.170
set FTP_PORT=12121
set FTP_USER=admin
set FTP_PASS=
set FTP_DIR=ConfigGen

rem 上传最新的压缩包到 FTP 服务器
set FTP_COMMAND_FILE=ftp.txt
echo open %FTP_HOST% %FTP_PORT% > %FTP_COMMAND_FILE%
echo user %FTP_USER% %FTP_PASS% >> %FTP_COMMAND_FILE%
echo cd %FTP_DIR% >> %FTP_COMMAND_FILE%

echo put %LATEST_FILE% /%FTP_DIR%/%LATEST_FILE% >> %FTP_COMMAND_FILE%

echo bye >> %FTP_COMMAND_FILE%
ftp -n -s:%FTP_COMMAND_FILE%

rem 清理临时文件
del %FTP_COMMAND_FILE%
del %LATEST_FILE%

endlocal