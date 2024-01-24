#source:  https://pythonspot.com/pyqt5-file-dialog/


import sys
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from app.constants import paths

from app.constants.types import Filetype

class FileDialog(QDialog):

    def __init__(self, parent=None, type = Filetype.IMAGE):
        super().__init__()
        self.parent = parent
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.type = type
        self.initUI()
        
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        self.openFileNamesDialog()

        #self.show()
    
    def openFileNamesDialog(self):
        copyTo = paths.IMAGES

        typesString = "Image files (*.png *.xpm *.jpg)"
        if (self.type == Filetype.IMAGE):
            copyTo = paths.IMAGES
            typesString = "Image files (*.png *.xpm *.jpg)"
        elif(self.type == Filetype.CONFIG): 
            copyTo = paths.USER_CONFIGS
            typesString = "Config files (*.py)"
        elif(self.type == Filetype.WEIGHTS): 
            copyTo = paths.USER_WEIGHTS
            typesString = "Checkpoint files (*.pth)"

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "",typesString, options=options)
        
        #called when open button is pushed in file dialog
        if files:
            self.parent.logger.log("Adding files to data directory", LogLevel.INFO)
            try: 
                for f in files: 
                    shutil.copy2(f, copyTo)
                self.done(1)
                self.parent.update_FilesList()
                return 0
            except Exception as e: 
                self.parent.logger.WARNING("Something went wrong copying the pictures into the specified directory %s\n %s", {self.copyTo, e})
                return -1

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     #ex = fileDialog()
#     sys.exit(app.exec_())