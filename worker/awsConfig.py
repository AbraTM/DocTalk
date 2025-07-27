import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

aws_config = Config(
    region_name = os.getenv("AWS_REGION"),
    retries = {
        "max_attempts": 3,
        "mode": "standard"
    }
)

s3 = boto3.client(
    "s3",
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    config = aws_config
)

sqs = boto3.client(
    "sqs",
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    config = aws_config
)
