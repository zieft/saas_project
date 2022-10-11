# 概要

- wiki删除
- wiki编辑
- markdown编辑器
    - 添加、编辑
    - 预览
- 上传图片

# 详细

1. ### wiki删除

2. ### Wiki编辑

3. ### 应用markdown编辑器插件

    - 富文本编辑器，ckeditor

    - markdown编辑器，mdeditor

    - 项目中应用markdown编辑器

        - 添加和编辑页面中的textarea输入框 -> 转换为markdown编辑器

          ```
          - 应用css
          <link rel="stylesheet" href="{% static 'plugin/editor-md/css/editormd.min.css' %}">
          - 应用js
          <script src="{% static 'plugin/editor-md/editormd.min.js' %}"></script>
          ```

          官网下载插件，https://github.com/pandao/editor.md，直接download ZIP

      解压以后放到项目的静态文件夹中即可。

        ```
        1. textarea矿通过div包裹以便以后查找并转化成编辑器
        	<div id="editor">
        		{{ field }}
        	</div>
        2. 初始化编辑器
                function initEditorMd() {
                    // 第一个参数就是需要应用editor的标签id
                    editormd('editor', {
                        placeholder: "请输入内容",
                        height: 500,
                        path: "{% static 'plugin/editor-md/lib/' %}",
                    })
                }
        ```

   - 使用markdown进行预览

``` 

1. 内容区域使用div标签包裹，并设置id
<div id="previewMarkdown">
	<textarea name="" id="" cols="30" rows="10">
		{{ wiki_object.content }}
	</textarea>
</div>

2.引入css，js
<link rel="stylesheet" href="{% static 'plugin/editor-md/css/editormd.preview.min.css' %}">

<script src="{% static 'plugin/editor-md/editormd.min.js' %}"></script>
<script src="{% static 'plugin/editor-md/lib/marked.min.js' %}"></script>
<script src="{% static 'plugin/editor-md/lib/prettify.min.js' %}"></script>
<script src="{% static 'plugin/editor-md/lib/raphael.min.js' %}"></script>
<script src="{% static 'plugin/editor-md/lib/underscore.min.js' %}"></script>
<script src="{% static 'plugin/editor-md/lib/sequence-diagram.min.js' %}"></script>
<script src="{% static 'plugin/editor-md/lib/flowchart.min.js' %}"></script>
<script src="{% static 'plugin/editor-md/lib/jquery.flowchart.min.js' %}"></script>

3.初始化
function initPreviewMarkdown () {
	editormd.markdownToHTML('previewMarkdown',{
		htmlDebode: 'style,script,iframe',  // 防止script攻击等
});
}
```

- 从本地上传图片，暂未实现

### 4 腾讯云对象存储 cos

以下代码来自文档：https://cloud.tencent.com/document/product/436/12269

``` 
pip install -U cos-python-sdk-v5
```

初始化：

``` python
# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys


# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = 'SecretId'     # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
secret_key = 'SecretKey'   # 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
region = 'eu-frankfurt'      # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)
```

创建桶：

```python
response = client.create_bucket(
    Bucket='examplebucket-1250000000'，
    ACL = 'public-read' # private, public-read, public-read-write
)
```

上传对象：

```python
#### 高级上传接口（推荐）
# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
response = client.upload_file(
    Bucket='saasbucket-1314123611',
    LocalFilePath='local.txt', // 本地文件路径
    Key='picture.jpg', // 上传到桶内的文件名
    PartSize=1,
    MAXThread=10,
    EnableMD5=False
)
print(response['ETag'])
```

### 5 项目中继承cos

向往我们的项目中用到的图片可以放在cos中，防止我们的服务器处理图片时压力过大。

5.1 创建项目时创建桶

```python
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        porject_name = form.cleaned_data.get('name')
        # 验证通过: 项目名、颜色、描述 + 创建者（当前登录的用户）
        # 为项目创建一个桶
        bucket = '{}-{}-{}-{}'.format(request.tracer.user.mobile_phone,
                                      porject_name,
                                      str(int(time.time() * 1000)),
                                      settings.COS_BUCKET_NAME_NR
                                      )
        region = settings.COS_REGION
        create_bucket(bucket)

        form.instance.region = region
        form.instance.bucket = bucket

        # 直接在form实例里添加creator
        form.instance.creator = request.tracer.user

        # 创建项目
        form.save()
```

5.2 markdown上传图片到cos

- cos上传文件：接受markdown上传的文件，再传到cos上
- markdown 上传图片

