# nsis_templates

An nsis sample project.

## Project structure

```
|---- root
    |---- cpp-demo
    |---- NSIS
    |---- nssm-2.24
```

- `cpp-demo` is a software which is the package target to install.
- `NSIS` is a project that contains the basic content of the installer.
- `nssm-2.24` is a tool that can install the software as a service.

## How to use

example to make base project's installer execute:

1. move to prorject folder

```
> cd nsis_templates
```

2. make

```
> build-setup.bat
```
