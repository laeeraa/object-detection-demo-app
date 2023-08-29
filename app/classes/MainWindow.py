import sys
import textwrap
from threading import Event
import cv2

from PyQt5.QtWidgets import (QApplication, QMainWindow,QHeaderView, QAbstractItemView, QTableWidgetItem ) 

from PyQt5.QtCore import(
    QDir, Qt, pyqtSlot
)

from PyQt5.QtGui import *
import numpy as np
from app.constants.types import Filetype
from app.packages.Hand_Gesture_Recognizer.hand_gesture_detection import VideoDetThread
from app.scripts.helpers import convert_cv_qt



from app.qt import Ui_MainWindow
import app.classes as classes
from app.constants import paths


from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItemGroup, QWidget, QVBoxLayout, QSlider, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtCore import Qt, QObject

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        self.imageDet = classes.ImageDet()
        self.modelHandler = classes.ModelHandler()
        self.stopHandGestureRecogEvent = Event()

        super().__init__(parent)

        self.setupUi(self)
        self.connectSignalsSlots()
        self.update_FilesList()
        self.initModelOptions()
        self.init_CollTable()
        self.init_ModelTable()
        self.init_DeviceOptions()
        self.init_Params()
        self.init_userModels()
        self.init_ImageViewer()

    def connectSignalsSlots(self):
        self.Btn_ImageDet_2.clicked.connect(self.openImageDetection)
        self.Btn_ImageDet_2.setIcon(QIcon("./app/assets/image1.png"))
        self.Btn_VideoDet_2.clicked.connect(self.openVideoDetection)
        self.Btn_VideoDet_2.setIcon(QIcon("./app/assets/video1.png"))
        self.Btn_WebcamDet_2.clicked.connect(self.openWebcamDetection)
        self.Btn_WebcamDet_2.setIcon(QIcon("./app/assets/webcam1.png"))
        self.list_filenames.itemDoubleClicked.connect(self.displayImageOrig)
        self.btn_process.clicked.connect(self.processImage)
        self.btn_openImageDialog.clicked.connect(self.openImageDialog)

        self.btn_addImage.clicked.connect(self.open_FileDialog_Image)
        self.btn_startWebcam.clicked.connect(self.startWebcam)
        self.btn_startWebcamDet.clicked.connect(self.startHandGestureRecog)
        self.btn_stopWebcamDet.clicked.connect(lambda x: self.stopHandGestureRecogEvent.set())
        self.combo_chooseDevice.currentIndexChanged.connect(self.device_changed)
        self.ln_batchSize.editingFinished.connect(self.batchSize_changed)
        self.ln_outputDir.editingFinished.connect(self.outputDir_changed)
        self.ln_threshhold.editingFinished.connect(self.threshhold_changed)
        self.btn_uploadConfig.clicked.connect(self.open_FileDialog_Configs)
        self.btn_uploadWeights.clicked.connect(self.open_FileDialog_Weights)


        # Comboboxes
        self.combo_api.currentIndexChanged.connect(self.api_changed)


        self.combo_model.currentIndexChanged.connect(self.model_changed)
        self.combo_collection.currentIndexChanged.connect(self.coll_changed)
        self.combo_usrConfig.currentIndexChanged.connect(self.usrConfig_changed)
        self.combo_usrWeights.currentIndexChanged.connect(self.usrWeights_changed)

        self.combo_model.highlighted.connect(self.changeTo_MMDetModelMode)
        self.combo_collection.highlighted.connect(self.changeTo_MMDetModelMode)
        self.combo_usrConfig.highlighted.connect(self.changeTo_usrModelMode)
        self.combo_usrWeights.highlighted.connect(self.changeTo_usrModelMode)

        # change SizeAdjustPolicy to none instead of AdjustToContentsOnFirstShow
        # so that it doesn't adjust once the stylesheet is changed
        self.combo_collection.setSizeAdjustPolicy(5)
        self.combo_model.setSizeAdjustPolicy(5)
        self.combo_usrConfig.setSizeAdjustPolicy(5)
        self.combo_usrWeights.setSizeAdjustPolicy(5)

    
    #check which models exist in filepath and add those to dropdown 
    def initModelOptions(self):
        #init Collections Combo Box
        self.combo_collection.clear()
        for c in self.modelHandler.collections: 
            self.combo_collection.addItem(c.name)
        self.combo_collection.setCurrentIndex(-1)
       
        #init Model ComboBox
        self.combo_model.clear()
        
        for c in self.modelHandler.collections:
            for m in c.models: 
                self.combo_model.addItem(m.name)
        

#Init functions
    def init_CollTable(self): 
        header = self.tb_collInfo.horizontalHeader()
        #header.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerV = self.tb_collInfo.verticalHeader()
        headerV.setDefaultSectionSize(37)
        headerV.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_collInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        

    def init_ModelTable(self): 
        header = self.tb_modelInfo.horizontalHeader()
        #header.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerV = self.tb_modelInfo.verticalHeader()
        headerV.setDefaultSectionSize(37)
        headerV.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_modelInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def init_DeviceOptions(self): 
        self.combo_chooseDevice.clear() 
        for g in self.modelHandler.devices: 
            self.combo_chooseDevice.addItem(g.name)
            
    def init_Params(self): 
        self.imageDet.batch_size = 1 
        self.imageDet.score_thr = 0.3
        self.imageDet.out_dir = paths.IMAGES_RES
        self.ln_batchSize.setText(str(self.imageDet.batch_size))
        self.ln_threshhold.setText(str(self.imageDet.score_thr))
        self.ln_outputDir.setText(str(self.imageDet.out_dir))
    
    def init_userModels(self): 
        for c in self.modelHandler.usrCheckpoints: 
            self.combo_usrWeights.addItem(c)
        for c in self.modelHandler.usrConfigs: 
            self.combo_usrConfig.addItem(c)
        self.combo_usrWeights.setCurrentIndex(0)
        self.combo_usrConfig.setCurrentIndex(0)
        self.imageDet.usrModelMode = True

    def init_ImageViewer(self): 
        self.qGScene = QGraphicsScene()
        self.qGItemGrp = QGraphicsItemGroup()
        qImgCat = QImage("C:\cust\Studium_local\Studienprojekt\data\images\\7.jpg").scaledToWidth(600)
        qGItemImg = QGraphicsPixmapItem(QPixmap.fromImage(qImgCat))
        qGItemImg.setTransform(QTransform().translate(-0.5 * qImgCat.width(), -0.5 * qImgCat.height()))
        self.qGItemGrp.addToGroup(qGItemImg)
        self.qGScene.addItem(self.qGItemGrp)

        qGView = QGraphicsView()
        qGView.setScene(self.qGScene)
        self.box_imageRes.addWidget(qGView, 1)
        qSlider = QSlider(Qt.Horizontal)
        qSlider.setRange(-100, 100)
        self.box_imageRes.addWidget(qSlider)
        qSlider.valueChanged.connect(self.scaleImg)
    
    def update_ResImg(self, image_path): 
        self.qGScene.clear()
        self.qGItemGrp = QGraphicsItemGroup()
        qImgCat = QImage(image_path).scaledToWidth(600)
        qGItemImg = QGraphicsPixmapItem(QPixmap.fromImage(qImgCat))
        qGItemImg.setTransform(QTransform().translate(-0.5 * qImgCat.width(), -0.5 * qImgCat.height()))
        self.qGItemGrp.addToGroup(qGItemImg)
        self.qGScene.addItem(self.qGItemGrp)

    def scaleImg(self,value):
        exp = value * 0.01
        scl = 10.0 ** exp
        self.qGItemGrp.setTransform(QTransform().scale(scl, scl))

#update Functions
    def update_CollTable(self): 
        self.tb_collInfo.item(0,0).setText(self.imageDet.collection.name)
        self.tb_collInfo.item(1,0).setText(self.imageDet.collection.metadata.training_data)
        self.tb_collInfo.item(2,0).setText(self.imageDet.collection.metadata.training_techniques)
        self.tb_collInfo.item(3,0).setText(self.imageDet.collection.metadata.training_resources)
        self.tb_collInfo.item(4,0).setText(self.imageDet.collection.metadata.architecture)
        self.tb_collInfo.item(5,0).setText(str(self.imageDet.collection.paper))
        self.tb_collInfo.item(6,0).setText(self.imageDet.collection.readme)
        self.tb_collInfo.item(7,0).setText(str(self.imageDet.collection.code))


    def update_ModelTable(self): 
        if(self.imageDet.model != None): 
            self.tb_modelInfo.item(0,0).setText(self.imageDet.model.name)
            # print(self.tb_modelInfo.columnWidth(1))
            # print(self.tb_modelInfo.columnWidth(0))

            # configText = '\n'.join(textwrap.wrap(self.imageDet.model.config, self.tb_modelInfo.columnWidth(0)))
            # print(configText)
            self.tb_modelInfo.item(1,0).setText(self.imageDet.model.config)
            self.tb_modelInfo.item(2,0).setText(str(self.imageDet.model.metadata))
            results_string = "\n".join([f"- {result}" for result in self.imageDet.model.results])
            self.tb_modelInfo.item(3,0).setText(results_string)
            self.tb_modelInfo.item(4,0).setText(self.imageDet.model.weights)
        else: 
            self.tb_modelInfo.item(0,0).setText(" ")
            self.tb_modelInfo.item(1,0).setText(" ")
            self.tb_modelInfo.item(2,0).setText(" ")
            self.tb_modelInfo.item(3,0).setText(" ")
            self.tb_modelInfo.item(4,0).setText(" ")


    def coll_changed(self): 
        if(self.combo_collection.currentIndex() >=0):
            self.imageDet.collection = self.modelHandler.find_collection(self.combo_collection.currentText())
            self.update_CollTable()
            self.update_models()
    
    def device_changed(self): 
        self.imageDet.device = self.modelHandler.devices[self.combo_chooseDevice.currentIndex()].inference_string
        print("Device changed to: " + self.imageDet.device)
    
    def update_models(self): 
         #init Model ComboBox
        self.combo_model.clear()
        self.imageDet.model = None; 
        for m in self.imageDet.collection.models:
            self.combo_model.addItem(m.name)

    def model_changed(self): 
        if(self.combo_model.currentIndex() >= 0):
            self.imageDet.model = self.modelHandler.find_model(self.combo_model.currentText())
            self.imageDet.collection = self.modelHandler.find_collection(self.imageDet.model.collection)
            self.list_status.addItem("-model changed to " + self.combo_model.currentText())
            self.update_ModelTable()
            self.update_CollTable()
    
    def usrWeights_changed(self): 
        if(self.combo_usrWeights.currentIndex() >= 0):
            
            weightsFile = self.combo_usrWeights.currentText()

            if(self.imageDet.model.collection != "User"): 
                self.imageDet.collection = classes.Collection("USER")
                self.imageDet.model = classes.Model(
                                        name = "", 
                                        collection = "User", 
                                        metadata=None, 
                                        config = None,
                                        weights = paths.USER_WEIGHTS + weightsFile)
            else:
                self.imageDet.model.weights = paths.USER_WEIGHTS + weightsFile
            self.list_status.addItem("-model changed to " + weightsFile)
            self.update_ModelTable()
            self.update_CollTable()

    
    def usrConfig_changed(self): 
        if(self.combo_usrConfig.currentIndex() >= 0):

            configFile = self.combo_usrConfig.currentText()
            name = configFile.strip(".py")

            if(self.imageDet.model != None and self.imageDet.model.collection != "User"): 
                self.imageDet.collection = classes.Collection("USER")

                self.imageDet.model = classes.Model(name = name, 
                                    collection = "User", 
                                    metadata=None, 
                                    config = paths.USER_CONFIGS + configFile,
                                    weights = None)
            else: 
                self.imageDet.model.name = name
                self.imageDet.model.config = paths.USER_CONFIGS+ configFile
            self.list_status.addItem("-model changed to " + configFile)
            self.update_ModelTable()
            self.update_CollTable()
    
    def api_changed(self): 
        self.imageDet.api = self.combo_api.currentText()
        self.list_status.addItem("-API changed to " + self.combo_api.currentText())

    def batchSize_changed(self): 
        self.imageDet.batch_size = float(self.ln_batchSize.text())
        print("Batchsize changed to " + str(self.imageDet.batch_size))
    
    def threshhold_changed(self): 
        self.imageDet.score_thr = float(self.ln_threshhold.text())
        print("Thresshold changed to "+ str(self.imageDet.score_thr))
    
    def outputDir_changed(self): 
        self.imageDet.out_dir = self.ln_outputDir.text()
        print("outputDir changed to " + self.imageDet.out_dir)

    def open_FileDialog_Image(self ): 
        classes.FileDialog(self, Filetype.IMAGE) 
    def open_FileDialog_Weights(self): 
        classes.FileDialog(self, Filetype.WEIGHTS)
    def open_FileDialog_Configs(self): 
        classes.FileDialog(self, Filetype.CONFIG)


#Sonstige Funktionen 
    def openImageDetection(self):
        self.tabWidget.setCurrentIndex(1)
        self.update_FilesList()

    def openVideoDetection(self):
        self.tabWidget.setCurrentIndex(2)
    
    def openWebcamDetection(self):
        self.tabWidget.setCurrentIndex(3)
    
    def update_FilesList(self):
        #clear list: 
        self.list_filenames.clear()
        #assume the directory exists and contains some files and you want all jpg and JPG files
        dir = QDir(paths.IMAGES)
        filters = ["*.jpg", "*.JPG"]
        dir.setNameFilters(filters)
        for filename in dir.entryList(): 
            self.list_filenames.addItem(filename)
        

    def displayImageOrig(self): 
        path = paths.IMAGES + self.list_filenames.currentItem().text()
        im_cv = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
        self.lb_image_orig.setPixmap(convert_cv_qt(im_cv))

    def processImage(self): 
        #Bild in Funktion reinwerfen
        path = paths.IMAGES + self.list_filenames.currentItem().text()
        
        #stop sorting 
        self.tb_predictions.sortByColumn(-1, 0)
        self.list_status.addItem("processing Image...")
        ret = None
        ret = self.imageDet.processImage(path)
        if(ret != None): 
            self.displayImageRes()
            self.ln_ObjectCount.setText("Objects detected: " + str(len(ret)))
            self.tb_predictions.clear()
            for i, r in enumerate(ret): 
                self.tb_predictions.insertRow(self.tb_predictions.rowCount())
                self.tb_predictions.setItem(self.tb_predictions.rowCount()-1, 
                         0, QTableWidgetItem(str(r['labelno']),0))
                self.tb_predictions.setItem(self.tb_predictions.rowCount()-1, 
                         1, QTableWidgetItem("{:.2f}%".format(float(r['score'])*100),0))
                self.tb_predictions.setItem(self.tb_predictions.rowCount()-1, 
                         2, QTableWidgetItem(r['labelclass'], 0))

            self.tb_predictions.sortByColumn(0, 0)

        else: self.list_status.addItem("processing Image didnt work")
        

    def displayImageRes(self): 
        path =  self.imageDet.out_dir + "/vis/" + self.list_filenames.currentItem().text()
        self.list_status.addItem("...displaying result image at "+ path)
        self.update_ResImg(path)
        #im_cv = cv2.imread(path, cv2.IMREAD_ANYCOLOR)   
        #self.lb_image_res.setPixmap(convert_cv_qt(im_cv))
        self.tabWidget.setCurrentIndex(2)

    def openImageDialog(self): 
        Imagedialog = classes.ImageLarge(self)
        Imagedialog.setImage(self)
        Imagedialog.exec()

    def addToStatusList(self, string): 
        self.list_status.addItem(string)
    
    def changeTo_usrModelMode(self): 
        if( not self.imageDet.usrModelMode):
            self.imageDet.usrModelMode = True
            self.list_status.addItem("-Swapped to User Model Mode ")
            self.combo_collection.setStyleSheet("color: rgba(255, 255, 255, 0.3); \
                                                border: 1px solid rgba(255, 255, 255, 0.12);")
            self.combo_model.setStyleSheet("color: rgba(255, 255, 255, 0.3); \
                                            border: 1px solid rgba(255, 255, 255, 0.12);")
            self.combo_usrConfig.setStyleSheet("")
            self.combo_usrWeights.setStyleSheet("")
        
    def changeTo_MMDetModelMode(self): 
        if(self.imageDet.usrModelMode):
            self.imageDet.usrModelMode = False
            self.list_status.addItem("-Swapped to MMDet Model Mode ")

            self.combo_usrConfig.setStyleSheet("color: rgba(255, 255, 255, 0.3); \
                                                border: 1px solid rgba(255, 255, 255, 0.12);")
            self.combo_usrWeights.setStyleSheet("color: rgba(255, 255, 255, 0.3); \
                                                border: 1px solid rgba(255, 255, 255, 0.12);")
            self.combo_collection.setStyleSheet("")
            self.combo_model.setStyleSheet("")
            


#Webcam Detection
    def startWebcam(self): 
        # create the video capture thread
        self.thread = classes.VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def stopWebcam(self): 
        self.thread.stop()


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.lb_webcam.setPixmap(qt_img)
    

    def startHandGestureRecog(self): 
        self.stopHandGestureRecogEvent.clear()
        # create the video capture thread
        self.thread = VideoDetThread(self.stopHandGestureRecogEvent)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_imageDet)
        # start the thread
        self.thread.start()
    
    def stopHandGestureRecog(self):
        self.thread.stop()

    @pyqtSlot(np.ndarray)
    def update_imageDet(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.lb_webcamDet.setPixmap(qt_img)