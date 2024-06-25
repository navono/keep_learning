# 开发用脚本

# C++

## 包管理器

### conan

### vcpkg

> vcpkg x-update-baseline --add-initial-baseline
>

CMake 设置
> -DCMAKE_TOOLCHAIN_FILE=%VCPKG_ROOT%/scripts/buildsystems/vcpkg.cmake
>
> -DCMAKE_INSTALL_PREFIX=D:\data\lib
>

# CI\CD

## Jenkins

```
pipeline {
    agent any

    stages {
        stage('Web 界面') {
            steps {
                echo '构建 Web 组态'
                build 'ConfigurationPlatform'
            }
        }
        stage('Web 服务') {
            steps {
                echo '构建 Web 服务'
                build 'WebServer'
            }
        }
        stage('VF 生成服务') {
            steps {
                echo '构建 VF 生成服务'
                build 'VFConfigGen'
            }
        }
    }
}
```

# Open CV

```python
cv2.imread(image_path)
```

无法加载中文路径图片，改为：

```python
cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
```

# PowerShell

远程安装 `.ps1` 没有权限失败

> Set-ExecutionPolicy RemoteSigned -Scope LocalMachine
>