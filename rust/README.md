# Learning rust in 30 minutes

以 `kl-` 开头的为自建的代码，其他为官方示例（submodule 形式）。

## VSCode 配置

> 安装 `rust-analyzer` 插件

设置工程配置路径：
```
  "rust-analyzer.linkedProjects": [
    "./rust/kl-learn-rust-in-30mins/Cargo.toml"
  ]
```

## 工程

```
> cargo new kl-learn-rust-in-30mins
> cd kl-learn-rust-in-30mins
``` 

运行 `cargo build` 会生成一个 `target` 目录，里面有一个 `debug` 目录，里面有一个 `kl-learn-rust-in-30mins`
文件，这就是编译后的可执行文件。
运行 `cargo run` 可以直接运行。

如果要增加依赖，可以在 `Cargo.toml` 文件中增加依赖，然后运行 `cargo build` 即可。
