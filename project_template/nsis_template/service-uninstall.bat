@echo off
setlocal

set NSSM="nssm-2.24\\win64\\nssm.exe"

%NSSM% stop ConfigGenServer
%NSSM% remove ConfigGenServer confirm

%NSSM% stop ConfigGenNginx
%NSSM% remove ConfigGenNginx confirm

endlocal