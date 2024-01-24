import sys
import os

from PyQt5.QtWidgets import QApplication

import ctypes



# get the current working directory and add to the system path
current_working_directory = os.getcwd()

if current_working_directory not in sys.path:
    sys.path = [current_working_directory] + sys.path

from app.classes.MainWindow import MainWindow


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

#for Apple 
# import AppKit
# [(screen.frame().size.width, screen.frame().size.height)
#     for screen in AppKit.NSScreen.screen


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = MainWindow()
    win.resize(w, h-50)
    win.show()

    sys.exit(app.exec())