# Booster Robotics SDK
Booster Robotics SDK aims to provide a simple and easy-to-use interface for developers to control the Booster Robotics products. 

## Prebuild environment
* OS  (Ubuntu 22.04 LTS)  
* CPU  (aarch64 and x86_64)   
* Compiler  (gcc version 11.4.0) 

## Installation
```bash
sudo ./install.sh
```

## Install python package for building python binding locally
```bash
pip3 install pybind11
pip3 install pybind11-stubgen
```

## Build examples
```bash
mkdir build
cd build
cmake ..
make
```

## For Python
```bash
# BUILD_PYTHON_BINDING=on 表示会编译python sdk，如果需要编译python sdk，需要手动安装以下依赖
pip3 install pybind11
# （安装后,如果cmake找不到pybind11, 可以通过sudo apt install pybind11-dev手动安装）
pip3 install pybind11-stubgen 
# （如果pybind11-stubgen安装在~/.local下，
# 需要手动export PATH=/home/[username]/.local/bin:/$PATH）
export PATH=~/.local/bin:/$PATH
cd /home/booster/Workspace/booster_robotics_sdk
mkdir build
cd build
cmake .. -DBUILD_PYTHON_BINDING=on
make
sudo make install #这一步主要用来将编译完成的pythonbind.so安装到python环境中
```

## Run examples
### 1. run b1_arm_sdk_example_client locally
```
cd build
./b1_arm_sdk_example_client 127.0.0.1
```
### 2. run b1_7dof_arm_sdk_example_client locally
```
cd build
./b1_7dof_arm_sdk_example_client 127.0.0.1
```
### 3. run other example xxx locally
```
cd build
./xxx 127.0.0.1
```

## Build python binding api and install
```bash
mkdir build
cd build
cmake .. -DBUILD_PYTHON_BINDING=on
make
sudo make install
```

if pybind11-stubgen cannot be found even after pip install, export PATH
```bash
export PATH=/home/[user name]/.local/bin:$PATH
```

## License

This project is licensed under the Apache License, Version 2.0. See the LICENSE file for details.

This project uses the following third-party libraries:
- fastDDS (Apache License 2.0)
- pybind11 (BSD 3-Clause License)
- pybind11-stubgen (MIT License)