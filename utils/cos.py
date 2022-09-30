from django.conf import settings
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


def create_bucket(bucket, region=settings.COS_REGION):
    secret_id = settings.COS_SECRET_ID
    secret_key = settings.COS_SECRET_KEY
    region = region

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    response = client.create_bucket(
        Bucket=bucket,
        ACL='public-read',  # private, public-read, public-read-write
    )
