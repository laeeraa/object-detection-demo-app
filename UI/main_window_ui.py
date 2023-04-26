# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Main_Window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1026, 890)
        MainWindow.setStyleSheet("/*\n"
"    Copyright 2013 Emanuel Claesson\n"
"\n"
"    Licensed under the Apache License, Version 2.0 (the \"License\");\n"
"    you may not use this file except in compliance with the License.\n"
"    You may obtain a copy of the License at\n"
"\n"
"        http://www.apache.org/licenses/LICENSE-2.0\n"
"\n"
"    Unless required by applicable law or agreed to in writing, software\n"
"    distributed under the License is distributed on an \"AS IS\" BASIS,\n"
"    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
"    See the License for the specific language governing permissions and\n"
"    limitations under the License.\n"
"*/\n"
"\n"
"/*\n"
"    COLOR_DARK     = #191919\n"
"    COLOR_MEDIUM   = #353535\n"
"    COLOR_MEDLIGHT = #5A5A5A\n"
"    COLOR_LIGHT    = #DDDDDD\n"
"    COLOR_ACCENT   = #3D7848\n"
"*/\n"
"\n"
"* {\n"
"    background: #191919;\n"
"    color: #DDDDDD;\n"
"    border: 1px solid #5A5A5A;\n"
"}\n"
"\n"
"QWidget::item:selected {\n"
"    background: #3D7848;\n"
"}\n"
"\n"
"QCheckBox, QRadioButton {\n"
"    border: none;\n"
"}\n"
"\n"
"QRadioButton::indicator, QCheckBox::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"}\n"
"\n"
"QRadioButton::indicator::unchecked, QCheckBox::indicator::unchecked {\n"
"    border: 1px solid #5A5A5A;\n"
"    background: none;\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked:hover, QCheckBox::indicator:unchecked:hover {\n"
"    border: 1px solid #DDDDDD;\n"
"}\n"
"\n"
"QRadioButton::indicator::checked, QCheckBox::indicator::checked {\n"
"    border: 1px solid #5A5A5A;\n"
"    background: #5A5A5A;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:hover, QCheckBox::indicator:checked:hover {\n"
"    border: 1px solid #DDDDDD;\n"
"    background: #DDDDDD;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    margin-top: 6px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    top: -7px;\n"
"    left: 7px;\n"
"}\n"
"\n"
"QScrollBar {\n"
"    border: 1px solid #5A5A5A;\n"
"    background: #191919;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    height: 15px;\n"
"    margin: 0px 0px 0px 32px;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    width: 15px;\n"
"    margin: 32px 0px 0px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
"    background: #353535;\n"
"    border: 1px solid #5A5A5A;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    border-width: 0px 1px 0px 1px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    border-width: 1px 0px 1px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    min-width: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::add-line, QScrollBar::sub-line {\n"
"    background:#353535;\n"
"    border: 1px solid #5A5A5A;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::add-line {\n"
"    position: absolute;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    width: 15px;\n"
"    subcontrol-position: left;\n"
"    left: 15px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"    height: 15px;\n"
"    subcontrol-position: top;\n"
"    top: 15px;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    width: 15px;\n"
"    subcontrol-position: top left;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 15px;\n"
"    subcontrol-position: top;\n"
"}\n"
"\n"
"QScrollBar:left-arrow, QScrollBar::right-arrow, QScrollBar::up-arrow, QScrollBar::down-arrow {\n"
"    border: 1px solid #5A5A5A;\n"
"    width: 3px;\n"
"    height: 3px;\n"
"}\n"
"\n"
"QScrollBar::add-page, QScrollBar::sub-page {\n"
"    background: none;\n"
"}\n"
"\n"
"QAbstractButton:hover {\n"
"    background: #353535;\n"
"}\n"
"\n"
"QAbstractButton:pressed {\n"
"    background: #5A5A5A;\n"
"}\n"
"\n"
"QAbstractItemView {\n"
"    show-decoration-selected: 1;\n"
"    selection-background-color: #3D7848;\n"
"    selection-color: #DDDDDD;\n"
"    alternate-background-color: #353535;\n"
"}\n"
"\n"
"QHeaderView {\n"
"    border: 1px solid #5A5A5A;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background: #191919;\n"
"    border: 1px solid #5A5A5A;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QHeaderView::section:selected, QHeaderView::section::checked {\n"
"    background: #353535;\n"
"}\n"
"\n"
"QTableView {\n"
"    gridline-color: #5A5A5A;\n"
"}\n"
"\n"
"QTabBar {\n"
"    margin-left: 2px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    border-radius: 0px;\n"
"    padding: 4px;\n"
"    margin: 4px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: #353535;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    border: 1px solid #5A5A5A;\n"
"    background: #353535;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: 1px solid #5A5A5A;\n"
"    background: #353535;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    width: 3px;\n"
"    height: 3px;\n"
"    border: 1px solid #5A5A5A;\n"
"}\n"
"\n"
"QAbstractSpinBox {\n"
"    padding-right: 15px;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {\n"
"    border: 1px solid #5A5A5A;\n"
"    background: #353535;\n"
"    subcontrol-origin: border;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-arrow, QAbstractSpinBox::down-arrow {\n"
"    width: 3px;\n"
"    height: 3px;\n"
"    border: 1px solid #5A5A5A;\n"
"}\n"
"\n"
"QSlider {\n"
"    border: none;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    height: 5px;\n"
"    margin: 4px 0px 4px 0px;\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    width: 5px;\n"
"    margin: 0px 4px 0px 4px;\n"
"}\n"
"\n"
"QSlider::handle {\n"
"    border: 1px solid #5A5A5A;\n"
"    background: #353535;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    width: 15px;\n"
"    margin: -4px 0px -4px 0px;\n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    height: 15px;\n"
"    margin: 0px -4px 0px -4px;\n"
"}\n"
"\n"
"QSlider::add-page:vertical, QSlider::sub-page:horizontal {\n"
"    background: #3D7848;\n"
"}\n"
"\n"
"QSlider::sub-page:vertical, QSlider::add-page:horizontal {\n"
"    background: #353535;\n"
"}\n"
"\n"
"QLabel {\n"
"    border: none;\n"
"}\n"
"\n"
"QProgressBar {\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    width: 1px;\n"
"    background-color: #3D7848;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"    background: #353535;\n"
"}\n"
"\n"
"QTextEdit {\n"
"    font-family:\'Segoe UI Semilight\'; \n"
"    font-size:12pt; \n"
"    font-weight:600;\n"
"     font-style:normal;\n"
"}\n"
"QPushButtont {\n"
"    font-family:\'Segoe UI Semilight\'; \n"
"    font-size:9.75pt; \n"
"    font-weight:400;\n"
"     font-style:normal;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(500, 300))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_Home_2 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_Home_2.sizePolicy().hasHeightForWidth())
        self.tab_Home_2.setSizePolicy(sizePolicy)
        self.tab_Home_2.setStyleSheet("border: none")
        self.tab_Home_2.setObjectName("tab_Home_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_Home_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.txt_tryVideo = QtWidgets.QTextEdit(self.tab_Home_2)
        self.txt_tryVideo.setLineWidth(0)
        self.txt_tryVideo.setObjectName("txt_tryVideo")
        self.gridLayout_7.addWidget(self.txt_tryVideo, 3, 1, 1, 1)
        self.Btn_VideoDet_2 = QtWidgets.QPushButton(self.tab_Home_2)
        self.Btn_VideoDet_2.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.Btn_VideoDet_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("video1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Btn_VideoDet_2.setIcon(icon)
        self.Btn_VideoDet_2.setIconSize(QtCore.QSize(300, 300))
        self.Btn_VideoDet_2.setObjectName("Btn_VideoDet_2")
        self.gridLayout_7.addWidget(self.Btn_VideoDet_2, 4, 1, 1, 1)
        self.Btn_WebcamDet_2 = QtWidgets.QPushButton(self.tab_Home_2)
        self.Btn_WebcamDet_2.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.Btn_WebcamDet_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("webcam1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Btn_WebcamDet_2.setIcon(icon1)
        self.Btn_WebcamDet_2.setIconSize(QtCore.QSize(300, 300))
        self.Btn_WebcamDet_2.setObjectName("Btn_WebcamDet_2")
        self.gridLayout_7.addWidget(self.Btn_WebcamDet_2, 4, 2, 1, 1)
        self.txt_Home = QtWidgets.QTextEdit(self.tab_Home_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_Home.setFont(font)
        self.txt_Home.setLineWidth(0)
        self.txt_Home.setObjectName("txt_Home")
        self.gridLayout_7.addWidget(self.txt_Home, 1, 0, 1, 3)
        self.Btn_ImageDet_2 = QtWidgets.QPushButton(self.tab_Home_2)
        self.Btn_ImageDet_2.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.Btn_ImageDet_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("image1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Btn_ImageDet_2.setIcon(icon2)
        self.Btn_ImageDet_2.setIconSize(QtCore.QSize(300, 300))
        self.Btn_ImageDet_2.setObjectName("Btn_ImageDet_2")
        self.gridLayout_7.addWidget(self.Btn_ImageDet_2, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(80, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem, 2, 0, 1, 3)
        self.txt_tryImage = QtWidgets.QTextEdit(self.tab_Home_2)
        self.txt_tryImage.setLineWidth(0)
        self.txt_tryImage.setObjectName("txt_tryImage")
        self.gridLayout_7.addWidget(self.txt_tryImage, 3, 0, 1, 1)
        self.txt_tryWebcam = QtWidgets.QTextEdit(self.tab_Home_2)
        self.txt_tryWebcam.setLineWidth(0)
        self.txt_tryWebcam.setObjectName("txt_tryWebcam")
        self.gridLayout_7.addWidget(self.txt_tryWebcam, 3, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 100, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem1, 5, 0, 1, 3)
        self.tabWidget.addTab(self.tab_Home_2, "")
        self.tab_ImageDet = QtWidgets.QWidget()
        self.tab_ImageDet.setObjectName("tab_ImageDet")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_ImageDet)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lb_image_res = QtWidgets.QLabel(self.tab_ImageDet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_image_res.sizePolicy().hasHeightForWidth())
        self.lb_image_res.setSizePolicy(sizePolicy)
        self.lb_image_res.setMinimumSize(QtCore.QSize(600, 400))
        self.lb_image_res.setMaximumSize(QtCore.QSize(1000, 500))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        self.lb_image_res.setFont(font)
        self.lb_image_res.setText("")
        self.lb_image_res.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_image_res.setObjectName("lb_image_res")
        self.gridLayout_8.addWidget(self.lb_image_res, 15, 1, 1, 1)
        self.combo_model = QtWidgets.QComboBox(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        self.combo_model.setFont(font)
        self.combo_model.setObjectName("combo_model")
        self.combo_model.addItem("")
        self.combo_model.addItem("")
        self.combo_model.addItem("")
        self.combo_model.addItem("")
        self.gridLayout_8.addWidget(self.combo_model, 2, 1, 1, 1)
        self.list_filenames = QtWidgets.QListWidget(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(11)
        self.list_filenames.setFont(font)
        self.list_filenames.setLineWidth(0)
        self.list_filenames.setObjectName("list_filenames")
        self.gridLayout_8.addWidget(self.list_filenames, 4, 1, 1, 1)
        self.btn_process = QtWidgets.QPushButton(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btn_process.setFont(font)
        self.btn_process.setStyleSheet("font:\"Segoe UI Semilight\"; \n"
"font-size: 12\n"
"")
        self.btn_process.setObjectName("btn_process")
        self.gridLayout_8.addWidget(self.btn_process, 6, 1, 1, 1)
        self.textEdit_6 = QtWidgets.QTextEdit(self.tab_ImageDet)
        self.textEdit_6.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.textEdit_6.setFont(font)
        self.textEdit_6.setObjectName("textEdit_6")
        self.gridLayout_8.addWidget(self.textEdit_6, 14, 0, 1, 1)
        self.textEdit_7 = QtWidgets.QTextEdit(self.tab_ImageDet)
        self.textEdit_7.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.textEdit_7.setFont(font)
        self.textEdit_7.setStyleSheet("")
        self.textEdit_7.setObjectName("textEdit_7")
        self.gridLayout_8.addWidget(self.textEdit_7, 14, 1, 1, 1)
        self.lb_image_orig = QtWidgets.QLabel(self.tab_ImageDet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_image_orig.sizePolicy().hasHeightForWidth())
        self.lb_image_orig.setSizePolicy(sizePolicy)
        self.lb_image_orig.setMinimumSize(QtCore.QSize(600, 400))
        self.lb_image_orig.setMaximumSize(QtCore.QSize(1000, 500))
        self.lb_image_orig.setText("")
        self.lb_image_orig.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_image_orig.setObjectName("lb_image_orig")
        self.gridLayout_8.addWidget(self.lb_image_orig, 15, 0, 1, 1)
        self.txt_ImageDet = QtWidgets.QTextEdit(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_ImageDet.setFont(font)
        self.txt_ImageDet.setLineWidth(0)
        self.txt_ImageDet.setObjectName("txt_ImageDet")
        self.gridLayout_8.addWidget(self.txt_ImageDet, 0, 0, 1, 2)
        self.textEdit_4 = QtWidgets.QTextEdit(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.textEdit_4.setFont(font)
        self.textEdit_4.setObjectName("textEdit_4")
        self.gridLayout_8.addWidget(self.textEdit_4, 3, 1, 1, 1)
        self.ln_ObjectCount = QtWidgets.QLineEdit(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        self.ln_ObjectCount.setFont(font)
        self.ln_ObjectCount.setObjectName("ln_ObjectCount")
        self.gridLayout_8.addWidget(self.ln_ObjectCount, 16, 1, 1, 1)
        self.btn_addImage = QtWidgets.QPushButton(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btn_addImage.setFont(font)
        self.btn_addImage.setStyleSheet("")
        self.btn_addImage.setObjectName("btn_addImage")
        self.gridLayout_8.addWidget(self.btn_addImage, 4, 0, 1, 1)
        self.list_status = QtWidgets.QListWidget(self.tab_ImageDet)
        self.list_status.setObjectName("list_status")
        self.gridLayout_8.addWidget(self.list_status, 2, 0, 2, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_8.addWidget(self.lineEdit, 6, 0, 1, 1)
        self.btn_openImageDialog = QtWidgets.QPushButton(self.tab_ImageDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_openImageDialog.setFont(font)
        self.btn_openImageDialog.setObjectName("btn_openImageDialog")
        self.gridLayout_8.addWidget(self.btn_openImageDialog, 8, 1, 1, 1)
        self.tabWidget.addTab(self.tab_ImageDet, "")
        self.tab_VideoDet = QtWidgets.QWidget()
        self.tab_VideoDet.setObjectName("tab_VideoDet")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_VideoDet)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.textEdit = QtWidgets.QTextEdit(self.tab_VideoDet)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_9.addWidget(self.textEdit, 0, 0, 1, 1)
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_VideoDet)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout_9.addWidget(self.textEdit_2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_VideoDet, "")
        self.tab_WebcamDet = QtWidgets.QWidget()
        self.tab_WebcamDet.setObjectName("tab_WebcamDet")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_WebcamDet)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btn_startWebcamDet = QtWidgets.QPushButton(self.tab_WebcamDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_startWebcamDet.setFont(font)
        self.btn_startWebcamDet.setObjectName("btn_startWebcamDet")
        self.gridLayout.addWidget(self.btn_startWebcamDet, 2, 1, 1, 1)
        self.lb_webcam = QtWidgets.QLabel(self.tab_WebcamDet)
        self.lb_webcam.setMinimumSize(QtCore.QSize(600, 400))
        self.lb_webcam.setText("")
        self.lb_webcam.setObjectName("lb_webcam")
        self.gridLayout.addWidget(self.lb_webcam, 3, 0, 1, 1)
        self.lb_webcamDet = QtWidgets.QLabel(self.tab_WebcamDet)
        self.lb_webcamDet.setMinimumSize(QtCore.QSize(600, 400))
        self.lb_webcamDet.setText("")
        self.lb_webcamDet.setObjectName("lb_webcamDet")
        self.gridLayout.addWidget(self.lb_webcamDet, 3, 1, 1, 1)
        self.txt_WebcamHeading = QtWidgets.QTextEdit(self.tab_WebcamDet)
        self.txt_WebcamHeading.setObjectName("txt_WebcamHeading")
        self.gridLayout.addWidget(self.txt_WebcamHeading, 0, 0, 1, 2)
        self.btn_startWebcam = QtWidgets.QPushButton(self.tab_WebcamDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_startWebcam.setFont(font)
        self.btn_startWebcam.setStyleSheet("")
        self.btn_startWebcam.setObjectName("btn_startWebcam")
        self.gridLayout.addWidget(self.btn_startWebcam, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.tab_WebcamDet)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout, 3, 2, 1, 1)
        self.tabWidget.addTab(self.tab_WebcamDet, "")
        self.gridLayout_6.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionVideo_Detection = QtWidgets.QAction(MainWindow)
        self.actionVideo_Detection.setObjectName("actionVideo_Detection")
        self.actionImage_Detection = QtWidgets.QAction(MainWindow)
        self.actionImage_Detection.setObjectName("actionImage_Detection")
        self.actionLive_Webcam_Detection = QtWidgets.QAction(MainWindow)
        self.actionLive_Webcam_Detection.setObjectName("actionLive_Webcam_Detection")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DemonstrationNeuronalNetworks"))
        self.txt_tryVideo.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:400;\">try object detection on videos</span></p></body></html>"))
        self.txt_Home.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">HOME</span></p></body></html>"))
        self.txt_tryImage.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:400;\">try object detection on images</span></p></body></html>"))
        self.txt_tryWebcam.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:400;\">try object detection on your webcam</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Home_2), _translate("MainWindow", "Start"))
        self.combo_model.setItemText(0, _translate("MainWindow", "Choose a model"))
        self.combo_model.setItemText(1, _translate("MainWindow", "Yolov3 with OpenMMLab"))
        self.combo_model.setItemText(2, _translate("MainWindow", "Faster rcnn r50 with OpenMMLab"))
        self.combo_model.setItemText(3, _translate("MainWindow", "Yolov4 with Tensorflow"))
        self.btn_process.setText(_translate("MainWindow", "Process Image"))
        self.textEdit_6.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:400;\">Original Image:</span></p></body></html>"))
        self.textEdit_7.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9.75pt; font-weight:400;\">Processed Image:</span></p></body></html>"))
        self.txt_ImageDet.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">Image Detection</span></p></body></html>"))
        self.textEdit_4.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9.75pt; font-weight:400;\">Choose a picture...</span></p></body></html>"))
        self.ln_ObjectCount.setText(_translate("MainWindow", "Objects Detected: "))
        self.btn_addImage.setText(_translate("MainWindow", "Add Image from filesystem"))
        self.lineEdit.setText(_translate("MainWindow", "Image chosen: "))
        self.btn_openImageDialog.setText(_translate("MainWindow", "Open result in Dialog"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ImageDet), _translate("MainWindow", "Image Detection"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_VideoDet), _translate("MainWindow", "Video Detection"))
        self.btn_startWebcamDet.setText(_translate("MainWindow", "Start Detection"))
        self.txt_WebcamHeading.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semilight\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Live Webcam Detection</p></body></html>"))
        self.btn_startWebcam.setText(_translate("MainWindow", "Start Webcam"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Choose a type of Detection"))
        self.comboBox.setItemText(1, _translate("MainWindow", "TechVidvan Hand Gesture Detection"))
        self.comboBox.setItemText(2, _translate("MainWindow", "OpenMMLab Video Detection YOLOV3"))
        self.comboBox.setItemText(3, _translate("MainWindow", "OpenMMLab Video Detection FasterRCNN"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_WebcamDet), _translate("MainWindow", "Live-Webcam Detection"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionVideo_Detection.setText(_translate("MainWindow", "Video Detection"))
        self.actionImage_Detection.setText(_translate("MainWindow", "Image Detection"))
        self.actionLive_Webcam_Detection.setText(_translate("MainWindow", "Live-Webcam Detection"))

