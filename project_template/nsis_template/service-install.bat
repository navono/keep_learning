@echo off
setlocal enabledelayedexpansion

set "file_path=%cd%\ip.txt"
for /f "usebackq delims=" %%a in ("%file_path%") do (
    set "new_ip=%%a"
    goto :break
)

:break

set NSSM="nssm-2.24\\win64\\nssm.exe"
set WEED_DATA_HOME=%CONFIGGEN_HOME%

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
set "new_root=\"%cd:\=\\%\\ConfigGenWeb\""
rem 使用sed命令更新nginx.conf中的root配置行
sed -i "s@^\s*listen.*;@            listen  18086;@" %nginx_conf%
sed -i "s@^\s*root.*;@            root %new_root%;@" %nginx_conf%

REM update web config
set "web_conf=ConfigGenWeb\\static\\config.js"
sed -i "s/http:\/\/*.*.*.*:*/http:\/\/%new_ip%:18680';/g" %web_conf%

REM install nginx service
%NSSM% install ConfigGenNginx "%cd%\\nginx-1.24.0\\nginx.exe"
%NSSM% start ConfigGenNginx

REM update web server config
set "web_server_config=ConfigGenServer\\config\\web_server_config.json"
sed -i "7s/.*/    \"port\": 15432,/" %web_server_config%
sed -i "12s/.*/  \"file_server_addr\": \"http:\/\/%new_ip%:8888\",/" %web_server_config%

%NSSM% install ConfigGenServer "%cd%\\ConfigGenServer\\ConfigGenServer.exe"
%NSSM% set ConfigGenServer AppDirectory "%cd%\\ConfigGenServer
%NSSM% start ConfigGenServer

%NSSM% install ConfigGenInfer "%cd%\\ConfigGenInfer\\ConfigGenInfer.exe"
%NSSM% set ConfigGenInfer AppDirectory "%cd%\\ConfigGenInfer
%NSSM% start ConfigGenInfer

endlocal