#source:  https://pythonspot.com/pyqt5-file-dialog/


import sys
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from constants import paths

class FileDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setWindowFlags(Qt.WA_DeleteOnClose)
    
        #self.openFileNameDialog()
        self.openFileNamesDialog()
        #self.saveFileDialog()

        #self.show()
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","Image files (*.png *.xpm *.jpg)", options=options)
        #called when open button is pushed in file dialog
        if files:
            print("Adding files to data directory")
            print(files)
            for f in files: 
                shutil.copy2(f, paths.IMAGES)
        self.done(1)
        self.parent.update_FilesList()
        return 0
        
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     #ex = fileDialog()
#     sys.exit(app.exec_())