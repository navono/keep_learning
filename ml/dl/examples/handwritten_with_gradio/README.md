# Handwritten Web

## 依赖安装

[cuda](https://docs.nvidia.com/deeplearning/cudnn/support-matrix/index.html) 版本查看。

> conda install -c conda-forge cudatoolkit=11.8 cudnn=8.9.2
>
> conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
>
> conda install -c conda-forge gradio

或者使用 `pip`
> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
>
> pip3 install gradio onnx onnxruntime opencv-python
