import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import uuid
from typing import Optional


def get_s3_client():
    """Get configured S3 client."""
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL or None,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION,
    )


async def upload_photo(file_content: bytes, filename: str, content_type: str) -> str:
    """
    Upload a photo to S3 and return the URL.
    """
    try:
        s3_client = get_s3_client()

        # Generate unique filename
        file_extension = filename.split(".")[-1]
        unique_filename = f"photos/{uuid.uuid4()}.{file_extension}"

        # Upload to S3
        s3_client.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=unique_filename,
            Body=file_content,
            ContentType=content_type,
            ACL="public-read",  # Adjust based on your security requirements
        )

        # Generate URL
        if settings.S3_ENDPOINT_URL:
            url = f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{unique_filename}"
        else:
            url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.S3_REGION}.amazonaws.com/{unique_filename}"

        return url
    except ClientError as e:
        raise Exception(f"Failed to upload photo: {str(e)}")


async def delete_photo(url: str) -> bool:
    """
    Delete a photo from S3.
    """
    try:
        s3_client = get_s3_client()

        # Extract key from URL
        key = url.split(f"{settings.S3_BUCKET_NAME}/")[-1]

        s3_client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=key)

        return True
    except ClientError as e:
        print(f"Failed to delete photo: {str(e)}")
        return False
