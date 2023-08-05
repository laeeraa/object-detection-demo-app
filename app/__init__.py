import sys
# import os

from PyQt5.QtWidgets import (
    QApplication
)

# from PyQt5.uic import loadUi
# from PyQt5 import QtGui
# from PyQt5.QtGui import *


# #for webcam detection
# import numpy as np 
# from threading import Event

# scriptpath = "C:\cust\Studium_local\Studienprojekt\Hand_Gesture_Recognizer"
# sys.path.append(os.path.abspath(scriptpath))

# from hand_gesture_detection import VideoDetThread

import classes

if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = classes.MainWindow()
    #win.resize(1800, 1000)
    win.show()

    sys.exit(app.exec())