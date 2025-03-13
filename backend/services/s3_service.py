import boto3
from botocore.exceptions import ClientError
from uuid import uuid4
import os
from dotenv import load_dotenv

load_dotenv()

KB = 1024
MB = 1024 * KB

FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg'
}

BUCKET = os.getenv('AWS_BUCKET', 'linkedin.insider')
KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
SECRET = os.getenv('AWS_SECRET')

s3 = boto3.resource('s3',
                    aws_access_key_id=KEY_ID,
                    aws_secret_access_key=SECRET
                    )
bucket = s3.Bucket(BUCKET)


async def upload_image_to_s3(img: bytes, content_type: str) -> str:
    if content_type not in FILE_TYPES:
        raise ValueError(f"Unsupported file type: {content_type}")

    fname = f'{uuid4()}.{FILE_TYPES[content_type]}'
    try:
        bucket.put_object(
            Key=fname,
            Body=img,
            ContentType=content_type
        )
        return fname
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return None


async def get_image_url(fname: str) -> str:
    if not fname:
        return None
    return f'https://{BUCKET}.s3.amazonaws.com/{fname}'
