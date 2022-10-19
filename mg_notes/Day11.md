# 文件管理

## 概要

- 文件夹管理
- 文件上传

## 详细

### 1.文件夹管理

#### 1.1 创建文件夹

#### 1.2 文件列表 & 进入文件夹

#### 1.3 编辑文件夹

#### 1.4 删除文件夹 （db级联删除 & 删除cos文件）

### 2. 文件上传

#### 2.1 上传按钮

#### 2.2 获取临时凭证 & 上传文件

- 全局：默认超时之后，自动再去获取（官方推荐）
- 局部：每次上传文件之前，进行临时凭证的获取

#### 2.3 容量的限制

- 单文件大小限制
- 总容量限制

注意：不合法，错误提示；合法，继续上传

#### 2.4 上传的文件保存到数据库

#### 2.5 右下角展示进度条

扩展

```
后端获取ajax数据的一般方法：
前端：
$.ajax({
...
// 对于简单的键值对&列表，后端可以直接获取
data: {name:11, age:22, xx:[11, 22, 33]}
// 对于复杂的数据如 值为字典，或者值为列表中套列表，需要用JSON.stringfy来序列化一下
data:JSON.stringfy(name:{k1:1, k2:666}, xx:[11, 22, [33, 44,55]])
})
或者：
$.post(url, JSON.stringfy(complex_data)), function (response_data) {...})

后端：
简单数据接收
request.POST.get('name')
request.POST.get('age')
request.POST.getlist('xx')
复杂数据接受：
request.body
info = json.loads(request.body.decode('utf-8'))
info['name]
info["xx"]
```

