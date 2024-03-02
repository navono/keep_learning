#!/bin/bash

set -e
set -x

BASEDIR=$(dirname "$0")
pushd "$BASEDIR"

## 指定环境名称
env_name="learning"

# 检查 conda 是否已经安装
if command -v conda &> /dev/null
then
    echo "conda 已安装"
else
    echo "conda 未安装"
    # 如果 conda 未安装，可以在此处添加安装 conda 的代码
fi

# 检查环境是否已经存在
if conda env list | grep -F "$env_name" | grep -v "ml-learning"
then
    echo "环境 $env_name 已存在"
else
    echo "环境 $env_name 不存在，正在创建..."
    conda create -n $env_name python=3.10 -y
fi

eval "$(conda shell.bash hook)" 2>&1 > /dev/null
conda activate $env_name

# 依赖包
pip install jupyterlab
pip install jupyter
pip install pandas
pip install pyarrow
pip install "psycopg[binary,pool]"
pip install opencv-python
pip install shapely
pip install pillow
pip install svgpathtools
pip install matplotlib

popd
