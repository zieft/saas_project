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

    client.delete_object(
        Bucket=bucket,
        Key=key,  # 桶内保存的文件名
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


def credential(bucket, region):
    # 生成一个临时凭证，并给前端返回
    # 1. 安装一个生成临时凭证的python模块 pip install -U qcloud-python-sts
    from sts.sts import Sts

    config = {
        'duration_seconds': 1800,
        'secret_id': secret_id,
        'secret_key': secret_key,
        'bucket': bucket,
        'region': region,
        'allow_prefix': '*',
        # 密钥的权限列表：
        'allow_actions': [
            # 'name/cosLPostObject',
            # 'name/cos:DeleteObject',
            # 'name/cos:UploadPart',
            # 'name/cos:UploadPartCopy',
            # 'name/cos:CompleteMultipartUpload',
            # 'name/cos:AbortMultipartUpload',
            "*",  # 所有的操作权限都支持
        ]
    }
    sts = Sts(config)

    result_dict = sts.get_credential()
    return result_dict


def check_file(bucket, region, key):
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    data = client.head_object(
        Bucket=bucket,
        Key=key,  # 桶内保存的文件名
    )

    return data


def delete_bucket(bucket, region):
    """ 删除桶 """

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    # 删除所有文件
    while True:
        part_object = client.list_objects(bucket)  # 单次最多只能返回1000个文件
        contents = part_object.get('Contents')  # contents有值说明还能从同能拿到待删除文件

        if not contents:
            # contents中没有值了，说明删干净了
            break

        objects = {
            'Quiet': 'true',
            'Object': [{'Key': item['Key']} for item in contents]
        }
        client.delete_objects(bucket, objects)

        if part_object['IsTruncated'] == 'false':
            break

    # 删除所有碎片
    while True:
        part_uploads = client.list_multipart_uploads(bucket)
        uploads = part_uploads.get('upload')
        if not uploads:
            break
        for i in uploads:
            client.abort_multipart_upload(bucket, i['Key'], i['UploadId'])
        if part_uploads['IsTrancated'] == 'false':
            break

    # 删除桶
    client.delete_bucket(bucket)
