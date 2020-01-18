from oracle import mainapp
import boto3
import logging
from botocore.exceptions import ClientError
from oracle.local_config import AWS_SETTINGS
import re

logger = logging.getLogger(__name__)


def build_s3_client():
    return boto3.client("s3", region_name="ap-south-1")


def upload_to_s3_filename(filename, key):
    bucket_name = AWS_SETTINGS["AWS_S3_BUCKET"]
    s3_client = build_s3_client()
    try:
        s3_client.upload_file(
            Filename=filename, Bucket=bucket_name, Key=normalize_s3_key(key)
        )
    except ClientError as e:
        logger.error("S3 File Upload Failed {}".format(e))
        raise e
    

def normalize_s3_key(key):
    """
    remove leading / from key if present as the signing key uses it but the browser
     swallows the // to make it / which gives a download error
    :param key: str
    :return: transformed_key: str

    >>> _normalize_s3_key('/tmp/abc.xml')
    'tmp/abc.xml'

    >>> _normalize_s3_key('tmp/xyz.xml')
    'tmp/xyz.xml'

    >>> _normalize_s3_key('/')
    ''
    """
    leading_slashes = r"^//*"

    compiled_pattern = re.compile(leading_slashes)

    return key[1:] if compiled_pattern.match(key) else key


def build_s3_read_client():
    """
    Build S3 Client with read access credentials only.
    :return:
    """
    return boto3.client(
        "s3",
        region_name="ap-south-1",
        aws_access_key_id=AWS_SETTINGS["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=AWS_SETTINGS["AWS_SECRET_ACCESS_KEY"],
    )


def get_presigned_url(key, **kwargs):
    """
    Returns a presigned s3 url for given key.
    :param key: str
    :return: url
    """
    key = normalize_s3_key(key)
    s3_client = build_s3_read_client()
    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": AWS_SETTINGS["AWS_S3_BUCKET"], "Key": key},
        **kwargs
    )
    return url
