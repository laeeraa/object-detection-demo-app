from PyQt5.uic import loadUi

from PyQt5.QtWidgets import (
    QDialog
)

import cv2
from constants import paths

from scripts.helpers import convert_cv_qt

class ImageLarge(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(paths.IMAGELARGE_UI, self)

    def setImage(self, parent): 
        path = paths.IMAGES_RES + "/vis/" + parent.list_filenames.currentItem().text()
        im_cv = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
        print(im_cv.shape)
        if(im_cv != []): 
            self.lb_ImageLarge.setPixmap(convert_cv_qt(im_cv, width=1000, height=750))
        else: 
            parent.list_status.addItem("Picture cannot be displayed")

        #Model sollte anders übergeben werden, Combo-Box könnte ja schon geändert sein 
        self.ln_heading.setText("Processed Picture with " + parent.combo_model.currentText())
        print("Set Image \n")