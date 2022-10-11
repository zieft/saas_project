from boto3.session import Session
from botocore.config import Config
from botocore.utils import fix_s3_host
from django.conf import settings

my_config = Config(
    region_name='',

    s3={
        'addressing_style': 'path'
    },
    retries={
        'max_attempts': 2,
        'mode': 'standard'
    }
)

key = settings.S3_KEY
secret_key = settings.S3_SECRET_KEY
upload_path = settings.S3_UPLOAD_PATH
bucket = settings.S3_BUCKET

session = Session(
    aws_access_key_id=key,
    aws_secret_access_key=secret_key
)
s3 = session.resource(
    service_name="s3",
    config=my_config,
    endpoint_url=settings.S3_ENDPOINT
)
s3.meta.client.meta.events.unregister('before-sign.s3', fix_s3_host)

client = s3.meta.client
