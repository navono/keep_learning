@echo off
setlocal

set NSSM="nssm-2.24\\win64\\nssm.exe"


REM install service
%NSSM% install ConfigGenServer "%cd%\\cpp-demo\\cppTemplate.exe"
%NSSM% set ConfigGenServer AppDirectory "%cd%\\cpp-demo"
%NSSM% start ConfigGenServer

REM install nginx service
%NSSM% install ConfigGenNginx "%cd%\\nginx-1.24.0\\nginx.exe"
%NSSM% start ConfigGenNginx

endlocal