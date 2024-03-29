# 概要

- django写离线脚本

- 探讨业务

- 设计表结构

- 功能实现【任务】

  - 查看项目列表
  - 创建项目
  - 星标项目

  

# 详细

## 1. 离线脚本

```
django, 框架
web运行时：server正在运行
离线：server没在运行
```

在某个py文件中对django项目做一些处理。

示例1：使用离线脚本在用户表中插入数据

```python
from django import setup
import os
import sys

# 将本文件所在的文件夹路径添加到path，即当前文件所在目录的上一级的上一级
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# manage.py中的一行，模拟运行一下manage.py，setup各种参数，链接数据库等
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas_project.settings")
setup()

# 下面就可以导入django运行时才能调用的函数跟方法了，例如
# 像用户表里添加一行新用户数据
from web import models

models.UserInfo.objects.create(username='django离线脚本', email='example@example.com', mobile_phone='8888888888',
                               password='87654321') # 注意：这时候表单没有验证功能，且密码不会被md5加密

```

![image-20220822175620257](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20220822175620257.png)

示例2： 数据库批量录入、敏感字批量导入

示例3：不同价格策略的导入

## 2.业务逻辑

### 2.1 价格策略

| 分类     | 标题 | 价格/年 | 创建项目个数 | 每个项目成员 | 项目空间 | 单文件 |                    |
| -------- | ---- | ------- | ------------ | ------------ | -------- | ------ | ------------------ |
| 1.免费版 | 免费 | 0       | 3            | 2            | 20M      | 5M     | 用户注册时自动获得 |
| 2.收费版 | vip  | 199     | 20           | 100          | 50g      | 500M   |                    |
| 3.收费版 | vvip | 299     | 50           | 200          | 100G     | 1G     |                    |
| 其他     |      |         |              |              |          |        |                    |

新用户注册自动拥有免费版额度。

### 2.2 用户关联

| 用户名  | 手机号 | 密码 | 。。 |
| ------- | ------ | ---- | ---- |
| 1.用户1 |        |      |      |
| 2.用户2 |        |      |      |

### 2.3 交易记录

| ID   | 状态   | 用户 | 价格 | 数量 | 实际支付 | 开始         | 结束             | 日志         | 订单号 |      |
| ---- | ------ | ---- | ---- | ---- | -------- | ------------ | ---------------- | ------------ | ------ | ---- |
| 1    | 已支付 | 1    | 1    |      | 0        | 系统当前时间 | null             | 系统自动操作 |        |      |
| 2    | 已支付 | 2    | 1    |      | 0        | 系统当前时间 | null             | 系统自动操作 |        |      |
| 3    | 已支付 | 2    | 2    | 1    | 199      | 系统当前时间 | 系统当前时间+1年 |              |        |      |

每次用户登录的时候，可以把该用户的交易对象保存在 request.tracer里面

### 2.4 创建存储

基于腾讯对象存储COS存储数据。  亚马逊 AWS S3也可以。

### 2.5 项目

| ID   | 名称 | 颜色  | 描述 | 星标       | 参与人数 | 创建者 | 已使用空间 |      |      |
| ---- | ---- | ----- | ---- | ---------- | -------- | ------ | ---------- | ---- | ---- |
| 1    | CRM  | #dddd |      | true/false |          | 2      | 1G         |      |      |
| 2    | SAAS | #uuu7 |      |            |          |        | 5M         |      |      |
| 3    | EFT  |       |      |            |          |        |            |      |      |

### 2.6 项目参与者

| ID   | 项目 | 用户 | 星标  | 邀请人 | 角色 |      |      |      |      |
| ---- | ---- | ---- | ----- | ------ | ---- | ---- | ---- | ---- | ---- |
| 1    | 1    | 1    | true  |        |      |      |      |      |      |
| 2    | 1    | 2    | false |        |      |      |      |      |      |
|      |      |      |       |        |      |      |      |      |      |

每次项目关联一个用户的时候创建一条记录，本表中，项目和用户是1对1关系。

## 3.任务

### 3.1 创建相应表结构

### 3.2 离线脚本创建价格策略 （免费版）

### 3.3 用户注册

- 之前：注册成功时，只在用户表中加记录
- 现在：还要再交易记录里加记录，关联免费版

### 3.4 新建项目功能

### 3.5 展示项目

- 星标
- 是否是我创建的项目

### 3.6 给项目加星标

