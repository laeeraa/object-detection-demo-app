from enum import Enum


class Filetype(Enum):
    CONFIG = 1
    WEIGHTS = 2
    IMAGE = 3


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class LogColor(Enum):
    DEBUG = "#596773"  # DarkNeutral500
    INFO = "#596773"  # DarkNeutral500
    WARNING = "#C25100"  # Orange
    ERROR = "#C9372C"  # Red
    CRITICAL = "#6E5DC6"  # Purple


class DetType(Enum):
    IMAGEDET = "Image Detection"
    WEBCAMDET = "Webcam Detection"
    VIDEODET = "Video Detection"


STYLESHEET_DISABLED = (
    "color: rgba(255, 255, 255, 0.3); border: 1px solid rgba(255, 255, 255, 0.12);"
)

STYLESHEET_ENABLED = ""
