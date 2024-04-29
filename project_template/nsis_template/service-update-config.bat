@echo on
setlocal

set IP=%1
echo %IP% > "ip.txt"

set zip="7z\\7z.exe"

@REM 解压 zip
%zip% x "build.7z" -o"./"

del "build.7z"
rmdir /s /q "7z"

endlocal