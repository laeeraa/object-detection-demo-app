import json

import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from app.classes.CustomLogger import logger
from app.constants.types import LogLevel


def convert_cv_qt(cv_img, height=400, width=600):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(
        rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
    )
    p = convert_to_Qt_format.scaled(width, height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


def parse_metafile(json_string):
    data = json.loads(json_string)
    collections = data.get("Collections", [])
    models = data.get("Models", [])

    parsed_data = {"Collections": [], "Models": []}

    for collection in collections:
        collection_info = {
            "Name": collection["Name"],
            "Metadata": collection["Metadata"],
            "Paper": collection["Paper"],
            "Code": collection["Code"],
        }
        parsed_data["Collections"].append(collection_info)

    for model in models:
        model_info = {
            "Name": model["Name"],
            "In Collection": model["In Collection"],
            "Config": model["Config"],
            "Metadata": model["Metadata"],
            "Results": model["Results"],
            "Weights": model["Weights"],
        }
        parsed_data["Models"].append(model_info)

    return parsed_data


def get_field(json, field):
    try:
        if json[field]:
            return json[field]
    except Exception as err:
        (f"Unexpected Error: {err} of Type: {type(err)}")
        return ""


def get_available_cameras():
    available_cameras = []
    logger.log("Checking for available cameras...", LogLevel.DEBUG, None)
    for camera_id in range(3):  # Assuming maximum of 3 cameras
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            available_cameras.append(camera_id)
            cap.release()
    return available_cameras
