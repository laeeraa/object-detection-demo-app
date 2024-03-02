from PyQt5.QtCore import QObject, pyqtSignal

from app.constants.types import LogLevel


class LoggerEmitter(QObject):
    # Define a custom signal with a value
    message_logged = pyqtSignal(str, LogLevel, object)


class Logger:
    def __init__(self, level=LogLevel.DEBUG):
        """
        Initializes a new instance of the Logger class.

        Parameters:
        level (LogLevel): The log level to be used (default is LogLevel.DEBUG).

        Returns:
        None
        """
        self.level = level
        self.signalEmitter = LoggerEmitter()

    def log(self, err, log_level, det_type=None):
        """
        Logs the given error message with the specified log level.

        Parameters:
        err (str): The error message to be logged.
        log_level (LogLevel): The log level of the message.
        tab (int): The tab on which the log message shall be displayed (default is 0 for all tabs).

        Returns:
        None
        """
        message = f"[{log_level.name}] [{det_type.value if det_type else ''}] {err}"
        if log_level.value > LogLevel.ERROR.value:
            message = f"Unexpected Error {err} of type: {type(err)}"
        if log_level.value >= self.level.value:
            self.signalEmitter.message_logged.emit(message, log_level, det_type)
        print(message)


logger = Logger(level=LogLevel.INFO)
