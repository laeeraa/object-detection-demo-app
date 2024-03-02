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

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

# for Apple
# import AppKit
# [(screen.frame().size.width, screen.frame().size.height)
#     for screen in AppKit.NSScreen.screen


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # the code to start to create and start a timer every 100 milliseconds.
    # This way we can safely terminate our application with Ctrl-C from the command line.
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    win = MainWindow()
    win.resize(w, h - 50)
    win.show()

    sys.exit(app.exec())
