#!/usr/bin/env bash

# SED: Stream editor

# 默认情况下，sed 输出整个文件，功能与 cat test.conf 一致
if [[ $1 = 1 ]]; then
  sed '' test.conf
fi

if [[ $1 = 2 ]]; then
  echo "this is some input" | sed ''
fi

# 删除所有内容。默认情况下，sed 修改的是缓存，而不是源文件
if [[ $1 = 3 ]]; then
  sed 'd' test.conf
fi

# 删除第一行，打印出结果
if [[ $1 = 4 ]]; then
  sed '1d' test.conf
fi

# 删除第一行，打印出结果
if [[ $1 = 5 ]]; then
  sed '1d' test.conf > test.new.conf
fi

# sed 也可以直接修改源文件
if [[ $1 = 6 ]]; then
  cp test.conf test.conf.back
  sed -i '1d' test.conf
fi

