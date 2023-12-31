import sys
from PyQt5.QtWidgets import (
    QApplication
)

import os

# get the current working directory
current_working_directory = os.getcwd()

# print output to the console
print(current_working_directory)
if current_working_directory not in sys.path:
    sys.path = [current_working_directory] + sys.path
#print(sys.path)


from app.classes.MainWindow import MainWindow


import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
print('Size is %d px %d px' % (w, h))

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