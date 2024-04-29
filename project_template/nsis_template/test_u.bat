@echo off
setlocal

set NSSM="bin\\nssm-2.24\\win64\\nssm.exe"

%NSSM% stop ConfigGenFileServer
%NSSM% remove ConfigGenFileServer confirm


endlocal