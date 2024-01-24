from enum import Enum, auto

from app.constants.types import LogLevel, LogColor
from PyQt5.QtCore import pyqtSignal, QObject

class LoggerEmitter(QObject):
    # Define a custom signal with a value
    message_logged = pyqtSignal(str, LogLevel)

class Logger:
    def __init__(self, level=LogLevel.DEBUG):
        self.level = level
        self.signalEmitter = LoggerEmitter()

    def log(self, err, log_level):
        if log_level.value >= self.level.value:
            message = " "
            if log_level.value < LogLevel.ERROR.value:
                message = (f"[{log_level.name}] {err}")
            else: 
                message = (f"Unexpected Error {err} of Type: {type(err)}")
            self.signalEmitter.message_logged.emit(message, log_level)

