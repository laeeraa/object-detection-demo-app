# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ImageLarge.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1107, 834)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lb_ImageLarge = QtWidgets.QLabel(Dialog)
        self.lb_ImageLarge.setText("")
        self.lb_ImageLarge.setObjectName("lb_ImageLarge")
        self.gridLayout.addWidget(self.lb_ImageLarge, 1, 0, 1, 1)
        self.ln_heading = QtWidgets.QLineEdit(Dialog)
        self.ln_heading.setEnabled(False)
        self.ln_heading.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.ln_heading.setStyleSheet("border: none;\n"
"font-family:\'Segoe UI Semilight\';\n"
"font-size:9.75pt; \n"
"font-weight:400; \n"
"font-style:normal")
        self.ln_heading.setAlignment(QtCore.Qt.AlignCenter)
        self.ln_heading.setObjectName("ln_heading")
        self.gridLayout.addWidget(self.ln_heading, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ln_heading.setText(_translate("Dialog", "Processed Picture mit Model: "))

