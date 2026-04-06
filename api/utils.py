import os
from datetime import datetime

import boto3


def upload_error(html_content, url):
    client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    clean_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    key = f"errors/{clean_url}/{timestamp}.html"

    client.put_object(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        Key=key,
        Body=html_content.encode("utf-8"),
        ContentType="text/html",
    )

    return key


def get_error_url(key):
    client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": os.getenv("AWS_BUCKET_NAME"), "Key": key},
        ExpiresIn=600,
    )

    return url
