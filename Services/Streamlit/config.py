import os

from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

BASE_DIR = os.environ.get("BASE_DIR")

S3_CONFIG = {
    "endpoint_url": os.environ.get("S3_CONFIG_ENDPOINT_URL"),
    "aws_access_key_id": os.environ.get("S3_CONFIG_AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.environ.get("S3_CONFIG_AWS_SECRET_ACCESS_KEY"),
    "bucket": os.environ.get("S3_CONFIG_BUCKET")
}
