import sys
from PyQt5.QtWidgets import (
    QApplication
)

project_home = 'C:\cust\Studium_local\Studienprojekt'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
print(sys.path)


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