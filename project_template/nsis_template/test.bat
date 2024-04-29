@echo off
setlocal enabledelayedexpansion

set "file_path=%cd%\ip.txt"

for /f "usebackq delims=" %%a in ("%file_path%") do (
    set "new_ip=%%a"
    goto :break
)

:break
echo %new_ip%
endlocal