删除、拷贝文件夹

```batch
rmdir /s /q "../out/VFConfigGen"
mkdir "../out"
xcopy /s /e /i "./bin" "../out/VFConfigGen"
```

压缩文件夹

```batch
REM 获取当前时间
set CURRENT_TIME=%TIME%

REM 提取小时和分钟
REM 假设时间格式为 HH:MM:SS.SS
REM 使用 %TIME:~0,2% 来提取前两个字符（小时）
set HOUR=%CURRENT_TIME:~0,2%
REM 使用 %TIME:~3,2% 来提取后两个字符（分钟）
set MINUTE=%CURRENT_TIME:~3,2%

cd ..
"VFConfigGen/third_party/7z/7z.exe" a -tzip "ConfigGen_%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%-%HOUR%%MINUTE%.zip" "./out/"
```