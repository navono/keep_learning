@echo off
setlocal enabledelayedexpansion

set "base_dir=%cd%"
set NSSM="nssm-2.24\\win64\\nssm.exe"
set WEED_DATA_HOME=%CONFIGGEN_HOME%

set "file_path=%cd%\ip.txt"
set "SED=%cd%\tools\sed.exe"
set "RM"=%cd%\tools\rm.exe"

set "file_path=%cd%\ip.txt"
for /f "usebackq delims=" %%a in ("%file_path%") do (
    set "new_ip=%%a"
    goto :break
)

:break

REM 如果 CONFIGGEN_HOME 为空，则设置 WEED_DATA_HOME 为 ProgramData 目录
if "%WEED_DATA_HOME%"=="" (
    set "WEED_DATA_HOME=%ProgramData%\ConfigGen\weed"
) else (
    set "WEED_DATA_HOME=%CONFIGGEN_HOME%\weed"
)

mkdir %WEED_DATA_HOME%
mkdir %WEED_DATA_HOME%\log

REM 定义服务的启动参数
set "APP_PARAMS=-logdir=\"%WEED_DATA_HOME%\log\" server -ip=%new_ip% -filer=true -dir=\"%WEED_DATA_HOME%\""
%NSSM% install ConfigGenFileServer "%cd%\\FileServer\\weed.exe"
%NSSM% set ConfigGenFileServer AppDirectory "%cd%\\FileServer
%NSSM% set ConfigGenFileServer AppParameters %APP_PARAMS%
%NSSM% start ConfigGenFileServer

REM update nginx config
set "nginx_conf=nginx-1.24.0\\conf\\nginx.conf"
set "new_root=\"%base_dir:\=\\%\\ConfigGenWeb\""
rem 使用sed命令更新nginx.conf中的root配置行
%SED% -i "s@^\s*listen.*;@            listen  18086;@" %nginx_conf%
%SED% -i "s@^\s*root.*;@            root %new_root%;@" %nginx_conf%

REM update web config
set "web_conf=%base_dir%\\ConfigGenWeb\\static\\config.js"
%SED% -i "s/http:\/\/*.*.*.*:*/http:\/\/%new_ip%:18680';/g" %web_conf%

REM install nginx service
%NSSM% install ConfigGenNginx "%cd%\\nginx-1.24.0\\nginx.exe"
%NSSM% start ConfigGenNginx

REM update web server config
set "web_server_config=%base_dir%\\ConfigGenServer\\config\\web_server_config.json"
%SED% -i "7s/.*/    \"port\": 15432,/" %web_server_config%
%SED% -i "12s/.*/  \"client_file_server_addr\": \"http:\/\/%new_ip%:8888\",/" %web_server_config%

%NSSM% install ConfigGenServer "%base_dir%\\ConfigGenServer\\ConfigGenServer.exe"
%NSSM% set ConfigGenServer AppDirectory "%base_dir%\\ConfigGenServer
%NSSM% start ConfigGenServer

%NSSM% install ConfigGenInfer "%base_dir%\\ConfigGenInfer\\ConfigGenInfer.exe"
%NSSM% set ConfigGenInfer AppDirectory "%base_dir%\\ConfigGenInfer
%NSSM% start ConfigGenInfer

%RM% "-f sed*"

endlocal