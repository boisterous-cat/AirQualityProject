import os

from dotenv import load_dotenv

load_dotenv()

S3_CONFIG = {
    "endpoint_url": os.environ.get("S3_CONFIG_ENDPOINT_URL"),
    "aws_access_key_id": os.environ.get("S3_CONFIG_AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.environ.get("S3_CONFIG_AWS_SECRET_ACCESS_KEY"),
    "bucket": os.environ.get("S3_CONFIG_BUCKET")
}
