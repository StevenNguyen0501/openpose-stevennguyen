import boto3
import logging
import io
import numpy as np
import cv2

from s3_upload.config import S3_BUCKET, S3_LOCATION, S3_SECRET_ACCESS_KEY, S3_ACCESS_KEY_ID
from s3_upload.s3_url import S3Url
from PIL import Image
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)
log.info("Connecting to S3")
s3 = boto3.resource('s3',
                    aws_access_key_id=S3_ACCESS_KEY_ID,
                    aws_secret_access_key=S3_SECRET_ACCESS_KEY)

s3_bucket = s3.Bucket(S3_BUCKET)
log.info("initialize s3 bucket")


def get_image_numpy_from_S3(s3_link, mode=1):
    """
    returns an numpy image from S3 with key
    :param s3_link:
    :param mode:
    :return:
    """
    s3_key = S3Url(s3_link).key
    object = s3_bucket.Object(s3_key)
    nparr = np.fromstring(object.get()['Body'].read(), np.uint8)

    img_np = cv2.imdecode(nparr, mode)

    return img_np


def convert_numpy_array_to_file(numpy_image, key_format):
    """

    :param numpy_image:
    :return: an Image object
    """
    img = []
    out_img = io.BytesIO()

    # TODO fix the format
    if key_format == "jpg":
        key_format = "JPEG"
        img = Image.fromarray(numpy_image).convert('RGB')

    elif key_format == "png":

        img = Image.fromarray(numpy_image).convert('RGBA')

    img.save(out_img, format=key_format)

    out_img.seek(0)
    return out_img


def get_s3_link_with_key(key):
    """

    :param key:
    :return:
    """

    return S3_LOCATION + key


def upload_numpy_array_to_s3(numpy_image, key, key_format):
    """

    :param numpy_image:
    :param key:
    :param key_format:
    :return: the url of the object after uploading to S3
    """

    output_image = convert_numpy_array_to_file(numpy_image, key_format)

    try:
        s3_bucket.put_object(Key=key, Body=output_image)

        url = S3_LOCATION + key

    except ClientError as e:
        error_msg = "Could not uploaded tried on image due to: {}".format(str(e))
        logging.error(error_msg)
        raise Exception(error_msg)
    return url


def download_image_from_s3(image_url, image_path_to_local_storage):
    """

    :param folder_path:
    :return:
    """

    try:
        s3_bucket.download_file(image_url, image_path_to_local_storage)

    except ClientError as e:
        error_msg = "Could not uploaded tried on image due to: {}".format(str(e))
        logging.error(error_msg)
        raise Exception(error_msg)