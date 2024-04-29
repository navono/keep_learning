@echo off
setlocal

set NSSM="nssm-2.24\\win64\\nssm.exe"

%NSSM% stop ConfigGenNginx
%NSSM% remove ConfigGenNginx confirm

%NSSM% stop ConfigGenServer
%NSSM% remove ConfigGenServer confirm

%NSSM% stop ConfigGenInfer
%NSSM% remove ConfigGenInfer confirm

%NSSM% stop ConfigGenFileServer
%NSSM% remove ConfigGenFileServer confirm

endlocal