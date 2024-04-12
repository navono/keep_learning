# Jenkins

`Jenkins` 在 Windows 中以二进制方式运行，如何修改默认的工作目录。

在安装目录下（一般是 `C:\Program Files\Jenkins`），找到 `jenkins.xml`，在 `arguments` 的 `-jar` 前，加上

```
-DJENKINS_HOME=D:\\data\\
```

重启服务。