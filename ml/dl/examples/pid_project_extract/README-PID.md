# Project Extract

## 整体过程

- 图片裁剪
- ocr 识别
- 对象处理
- xml 生成

## 开发环境

安装 `conan` 依赖管理工具，新建环境。

> conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
>
> pip install paddlepaddle-gpu==2.5.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
>
> pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
>
> pip install "paddleocr>=2.0.1"
>

### PyCharm 调试

1、新增 `FastAPI` 调试项

2、在 `Application file` 中指定当前创建 `FastAPI` 实例的文件

3、在 `Application name` 中指定当上述文件中的 `FastAPI` 实例的名称

4、uvicorn 参数设置 `--reload` 即会在文件修改后自动重载调试会话
