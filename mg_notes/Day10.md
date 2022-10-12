# 概览

功能：

- 文件夹

- 文件

细节：

- 模态对话框 & ajax & 后台modelForm
- 目录切换，展示文件夹及文件
- 删除文件夹的时候，同时删除嵌套在其中的其他文件夹和文件
- js上传文件到cos
  - 进度条
- 删除文件
  - 同时删除cos桶中的文件删除
- 下载文件

# 详细

### 1.功能设计

- 浏览器直接把文件上传到cos而不经过咱们的django程序，从而减少服务器的负载。
  - 后端给浏览器发送凭证，允许其向cos上传文件
  - 上传成功后将cos的返回信息发送到后端，并保存在db中

### 2.数据库设计

| ID   | 项目ID | 文件<br />文件夹名 | 类型 | 大小 | 父目录 | Key<br />cos内的文件名 | 更新者 | 更新时间 |
| ---- | ------ | ------------------ | ---- | ---- | ------ | ---------------------- | ------ | -------- |
|      |        |                    |      |      |        |                        |        |          |
|      |        |                    |      |      |        |                        |        |          |
|      |        |                    |      |      |        |                        |        |          |

### 3. 知识点

#### 3.1 URL传参、不传参

```python
url(r'^file/$', manage.file, name='file')
```

```python
# /file/
# /file/?folder_id=50
def file(request, project_id):
    folder_id = request.GET.get('folder_id')
```

#### 3.2 模态框 + 警告框

![image-20221012100529187](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20221012100529187.png)

#### 3.3 获取导航条

![image-20221012103823920](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20221012103823920.png)

![image-20221012100559711](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20221012100559711.png)

```python
# /file/
# /file/?folder_id=50
def file(request, project_id):
    folder_id = request.GET.get('folder_id')
    url_list = [
        {"id":1, "name":"文件夹名1"},
        {"id":2, "name":"文件夹名2"},
               ]
    if not folder_id:
        pass
    else:
        file_object = models.FileRepository.objects.filter(id=folder_id, file_type=2).first()
        
        row_object = file_object
        while row_object:
            url_list.insert(0, {"id":row_object.id, "name":row_object.name})
            row_object = row_object.parent
    print(url_list)
```

#### 3.4 cos上传文件：Python

```python
def upload_file(bucket, region, file_object, key):
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_object,  # 上传markdown
        Key=key,  # 筒内保存的文件名
    )

    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)

```

使用这种方法上传，密钥信息始终在后端，前端接触不到，所以非常安全

#### 3.5 cos上传文件：javaScript （直接使用原密钥，不推荐）

1. 从官网下js文件


2. 前端代码


3. 跨域问题（浏览器导致）

![image-20221012105709305](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20221012105709305.png)

![image-20221012111045850](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20221012111045850.png)

![image-20221012111058517](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20221012111058517.png)

#### 3.6 cos上传文件：临时密钥【推荐】

前端先往后端发请求获取临时凭证，再用临时凭证向cos上传文件

1. 路由

   ```python
   url(r'^demo2'/$, manage.demo2, name='demo2'),
   url(r'^cos/credential'/$, manage.cos_credential, name='cos_credential'),
   ```

2. 视图

```python
def deme2(request):
    return render(request, 'demo2.html')

def cos_credential(request):
    # 生成一个临时凭证，并给前端返回
    # 1. 安装一个生成临时凭证的python模块 pip install -U qcloud-python-sts
    from sts.sts import Sts
    config = {
        'duration_seconds' : 1800,
        'secret_id': '',
        'secret_key': '',
        'bucket': '',
        'region': 'eu-frankfurt',
        'allow_prefix': '*',
        # 密钥的权限列表：
        'allow_actions': [
            'name/cosLPostObject',
            # 'name/cos:DeleteObject',
            # 'name/cos:UploadPart',
            # 'name/cos:UploadPartCopy',
            # 'name/cos:CompleteMultipartUpload',
            # 'name/cos:AbortMultipartUpload',
            # "*", # 所有的操作权限都支持
        ]
    }
```

3. html页面

   ```html
   {% load static %}
   
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Document</title>
   </head>
   <body>
   <h1>示例2：临时凭证上传文件</h1>
   <input type="file" name="upload_file" id="uploadFile" multiple/>
   
   <script src="{% static 'js/jquery-3.6.0.min.js' %}"></script>
   <script src="{% static 'js/cos-js-sdk-v5.min.js' %}"></script>
   <script>
       var cos;
       $(function () {
           initCOS();
           bindChangeFileInput();
       });
   
       function initCOS() {
           cos = new COS({
               getAuthorization: function (options, callback) {
                   // 向django后台发送请求，获取临时凭证
                   // 相当于$.ajax({type:"GET"})
                   $.get('/cos.credential/', {
                       // 可从options取需要的参数
                   }, function (data) {
                       var credentials = data && data.credentials;
                       if (!data || !credentials) return console.error("credentials invalid");
                       callback({
                           TmpSecretId: credentials.tmpSecretId,
                           TmpSecretKey: credentials.tmpSecretKey,
                           XCosSecurityToken: credentials.sessionToken,
                           StartTime: data.startTime,
                           ExpiredTime: data.expiredTime,
                       });
                   });
               }
           })
       }
   
       function bindChangeFileInput() {
           $("#uploadFile").change(function () {
               // 获取要上传的所有文件对象列表
               var files = $(this)[0].files;
               $.each(files, function (index, fileObject) {
                   var fileName = fileObject.name;
                   // 上传文件
                   cos.putObject({
                       Bucket: '',
                       Region: '',
                       Key: fileName,
                       StorageClass: 'STANDARD',
                       Body: fileObject,
                       onProgress: function (progressData) {
                           console.log("文件上传进度---->", fileName, JSON.stringify(progressData));
                       }
                   }, function (err, data) {
                       console.log(err || data);
                   });
               })
           })
       }
   </script>
   </body>
   
   </html>
   ```


4. 跨域问题

​ 相同的解决思路，创建桶的时候配置好跨域规则。

```python
def create_bucket(bucket, region=settings.COS_REGION):
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    response = client.create_bucket(
        Bucket=bucket,
        ACL='public-read',  # private, public-read, public-read-write
    )

    cors_config = {  # 配置跨域规则
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': '*',
                'ExposeHeader': '*',
                'MaxAgeSeconds': 500
            }
        ]
    }
    client.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration=cors_config
    )
    
```

#### 总结

python直接上传

js + 临时凭证上传

#### 3.7 cos的功能 & 项目

#### 3.8 Markdown上传不受影响

#### 3.9 js 上传文件

- 临时凭证：当前项目的 桶&区域
- js上传文件：设置当前的 桶&区域

#### 3.10 this

```Javascript
var name = 'qz28'

function func() {
    var name = 'qz25'
    console.log(name) // 控制台输出qz25
}

func(); 
```

```javascript
var name = 'qz28'

function func() {
    var name = 'qz25'
    console.log(this.name) // 控制台输出qz28
}

func(); // 因为又全局来调用func函数，故this为全局，所以使用全局变量
```

```javascript
va name = 'wangyang'
info = {
    name: '陈硕',
    func: function() {
        console.log(this.name) // 控制台输出 陈硕
    }
}

info.func(); // 由info这个字典进行调用，故使用info内的局部变量
```

总结：没个韩硕都是一个作用域，在它的内部都会存在一个this，谁调用这个函数，this就是谁

```javascript
va name = 'wangyang'
info = {
    name: '陈硕',
    func: function() {
        console.log(this.name) // 控制台输出 陈硕 info.name
        function test() {
            console.log(this.name); // 控制台输出 wangyang
        }
        test() // 只要func前面没有前缀，那就是被全局调用
    }
}

info.func(); // 由info这个字典进行调用，故使用info内的局部变量
```

```javascript
va name = 'wangyang'
info = {
    name: '陈硕',
    func: function() {
        var that = this // 此处的this为info这个字典
        function test() {
            console.log(that.name); // 此处的that为上面定义的this，也就是info这个字典，所以打印一个 陈硕
        }
        test() // 故这种调用相当于 info.name
    }
}

info.func(); // 由info这个字典进行调用，故使用info内的局部变量
```

