from django.conf import settings
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = settings.COS_SECRET_ID
secret_key = settings.COS_SECRET_KEY


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


def delete_file(bucket, region, key):
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
    client.delete_object(
        Bucket=bucket,
        Key=key,  # 筒内保存的文件名
    )


def delete_file_list(bucket, region, key_list):
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)
    objects = {
        'Quiet': 'true',
        'object': key_list
    }

    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
    client.delete_objects(
        Bucket=bucket,
        Delete=objects
    )
