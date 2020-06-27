from urllib.request import urlopen

import cv2
import numpy as np
from build.python.openpose import pyopenpose as op
from examples.apis.s3_upload.helpers import get_image_numpy_from_S3


def get_image_byte_io_by_url(url):
    """

    :param url:
    :return: return bytes of an image
    """
    resp = urlopen(url=url)
    return resp.read()


def get_25_key_points(url):
    # TODO Catch exception in this function
    image_input = get_image_numpy_from_S3(url)

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "/openpose/models"

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    datum.cvInputData = image_input
    opWrapper.emplaceAndPop([datum])

    return datum.poseKeypoints.astype('int')

