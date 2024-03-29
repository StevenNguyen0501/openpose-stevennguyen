# s3_upload/config.py

import os

S3_SECRET_ACCESS_KEY     = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_ACCESS_KEY_ID         = os.environ.get("S3_ACCESS_KEY_ID")

S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
S3_LOCATION               = 'https://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 5000

