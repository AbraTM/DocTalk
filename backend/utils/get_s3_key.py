from urllib.parse import urlparse

def get_s3_key(s3_url):
    parsed_url = urlparse(s3_url)
    return parsed_url.path.lstrip('/')