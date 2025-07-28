import os
from urllib.parse import urlparse
from awsConfig import s3, S3_BUCKET_NAME

TEMP_FOLDER = "temp"
os.makedirs("temp", exist_ok=True)

def get_s3_key(s3_url):
    parsed_url = urlparse(s3_url)
    return parsed_url.path.lstrip('/')

def downloadFromS3(message):
    file_name = message["file_name"]
    s3_url = message["s3_url"]

    local_file_path = os.path.join(TEMP_FOLDER, file_name)
    s3_key = get_s3_key(s3_url)
    s3.download_file(S3_BUCKET_NAME, s3_key, local_file_path)

    print(local_file_path)
    return local_file_path