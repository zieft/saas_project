# day01 前期工作

## 今日概要

- 虚拟环境（项目环境）
- django项目框架：local_settings
- git实战应用
- 通过python 和 腾讯云 发送短信

## 今日详细

### 1 虚拟环境 virtualenv

1. 安装

   ```shell
   pip3 install virtualenv
   ```

2. 创建虚拟环境

   ```
   virtualenv 环境名称
   ```

   ```
   假设：目前电脑有 py27
   virtualenv 环境名称 --python==python3.6
   ```

3. 进入虚拟环境

   ```
   source ./saas/bin/active
   ```

   进入虚拟环境本质上是用source命令去执行虚拟环境文件夹bin目录里的active文件

### 2 搭建django环境

1. 先创建虚拟环境，再在pycharm里创建项目（可能是django1的缘故）

2. 实战使用python3.6和django1.11.7时，遇到下面的错误

   ```
   TypeError: unsupported operand type(s) for /: 'str' and 'str'
   ```

   解决办法就是把setting里的DIR 的 / 放到字符串里面。

3. mysqlclient要使用1.3.14之前的版本，因为这个版本的django实在是太老了
4. mac安装mysqlclient有困难的，可以看这一篇https://stackoverflow.com/questions/1857861/libmysqlclient15-dev-on-macs

### 3 本地配置local_settings.py

3.1 在setting.py中导入local_settings.py

```python
try:
    from .local_settings import *
except ImportError:
    pass

```

3.2 创建自己的local_settings.py

3.3 提交代码的时候

