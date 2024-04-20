# 版本管理

## pyenv

# 虚拟环境管理

## pipenv

创建虚拟开发环境：

```
> pipenv --python 3.12
```

如果要将虚拟机环境目录创建在当前项目目录下，可以使用：

```
> export PIPENV_VENV_IN_PROJECT=1
> pipenv --python 3.12
```

如果已经存在 `Pipfile` 文件，可以使用：

```
> pipenv install
```

安装依赖包：

```
> pipenv install xx
```

更新 Pipfile:

```
> pipenv update
> pipenv lock
```

进入虚拟环境：
> pipenv shell

退出虚拟环境：
> exit

### 安装包

- 在虚拟环境中，可用 `pip` 安装包
- 在 `Pipfile` 中添加包名，然后执行 `pipenv install`
- 在命令行， `pipenv install xx`
