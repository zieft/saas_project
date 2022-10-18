# -*- coding=utf-8
from django.conf import settings
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = settings.COS_SECRET_ID
secret_key = settings.COS_SECRET_KEY
region = settings.COS_REGION

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)

# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
response = client.upload_file(
    Bucket='saasbucket-1314123611',
    LocalFilePath='temp.py',
    Key='p1.py',

)
print(response['ETag'])

# 创建桶
response = client.create_bucket(
    Bucket='examplebucket-1250000000',
    ACL='public-read',  # private, public-read, public-read-write
)

# 删除文件
client.delete_object(
    Bucket='saasbucket-1314123611',
    Key='p1.py',
)
