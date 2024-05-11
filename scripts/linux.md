# 文件操作

宿主机从服务器下载文件
> scp user@xxx:/path/to/file /path/to/local
>

上传文件到服务器
> "build-push": "yarn build && scp -r ./build/* user@1.1.1.1:/home/xx/sourcecode/build",