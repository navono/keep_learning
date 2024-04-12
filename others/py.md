# 版本管理

## pyenv

# 虚拟环境管理

## pipenv

```
pipenv create 

# 更新 Pipfile
pipenv update
pipenv lock

pipenv install xx
```

进入虚拟环境：
> pipenv shell

退出虚拟环境：
> exit

### 安装包

- 在虚拟环境中，可用 `pip` 安装包
- 在 `Pipfile` 中添加包名，然后执行 `pipenv install`
- 在命令行， `pipenv install xx`
