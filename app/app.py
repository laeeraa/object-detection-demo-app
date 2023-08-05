import sys
from PyQt5.QtWidgets import (
    QApplication
)


from classes.MainWindow import MainWindow

if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = MainWindow()
    #win.resize(1800, 1000)
    win.show()

    sys.exit(app.exec())