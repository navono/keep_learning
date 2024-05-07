# Poetry

## 安装

参考官方文档

## 使用

### 指定 py 版本

指定 `Python` 存在时：

> poetry env use 3.12
>

不存在时，先用 `pyenv` 进行本地安装

> pyenv install 3.11
>
> pyenv local 3.11
>

再使用 `poetry` 指定:
>
> poetry env use 3.11

### 空工程初始化

> poetry init
>

或者全部默认：

> poetry init -q

### 带 poetry.lock 工程初始化

> poetry install
>

### 添加依赖

> poetry add requests
>

### 导出为 requirements.txt

> poetry export -f requirements.txt -o requirements.txt --without-hashes
>

dev 依赖

> poetry export -f requirements.txt -o requirements.txt --without-hashes --dev
>

非 `package` 模式：
> [tool.poetry]
>
> package-mode = false


其他命令参考官方文档。

## poetry 全局设置

查看全局配置

> poetry config --list
>

更新全局配置，例如将 `env` 设置为项目路径内，默认是在全局地址。

> poetry config virtualenvs.in-project true
>

## 问题

1. 在 `Ubuntu` 系统上，出现过安装依赖包时，一直处于 `pendding` 状态，解决方法是：
   > 使用 -vvv 查看具体情况，如果是网络问题，可以尝试更换网络环境；如果显示中出现 `kering` 字眼，则
   >
   > export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
   >
   > 后再进行安装

2. 如果碰到依赖包的 `Python` 版本不符合的时候，可以将依赖包的 `Python` 版本指定为要求的版本，例如：
   > numpy = {version = "^1.26.0", python="^3.10,<3.13"}