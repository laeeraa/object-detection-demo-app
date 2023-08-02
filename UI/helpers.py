import cv2
from PyQt5 import QtGui 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


def convert_cv_qt(cv_img, height=400, width=600):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(width, height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)