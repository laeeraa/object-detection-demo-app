import ctypes
import os
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

# get the current working directory and add to the system path
current_working_directory = os.getcwd()

if current_working_directory not in sys.path:
    sys.path = [current_working_directory] + sys.path

from app.classes.MainWindow import MainWindow

# to make cuda work
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

if __name__ == "__main__":

    app = QApplication(sys.argv)

    availableSize = app.desktop().availableGeometry().size()
    w = availableSize.width()
    h = availableSize.height()

    # the code to start to create and start a timer every 100 milliseconds.
    # This way we can safely terminate our application with Ctrl-C from the command line.
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    win = MainWindow()
    #resize the Window to fill full screen
    win.adjustSize()
    win.resize(w, h)
    win.show()

    #start application
    sys.exit(app.exec())
