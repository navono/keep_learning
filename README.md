# keep_learning

Just a learning repo about programming.

## Pytorch

> python -c "import torch; print(torch.cuda.get_device_name(torch.cuda.current_device()))"
>

## Notebook

增加 `notebook` 的目录插件
> poetry add notebook=6.5.7 jupyter-contrib-nbextensions jupyter-nbextensions-configurator
>
> jupyter contrib nbextension install --user
>
> jupyter nbextensions_configurator enable --user
>
> jupyter nbextension enable toc2/main
>
> pt add jupyterthemes
>

切换主题：
> jt -t chesterish
> 