import sys
import textwrap
from threading import Event
import cv2
import json

from PyQt5.QtWidgets import (QApplication, QMainWindow,QHeaderView, QAbstractItemView, QTableWidgetItem, QListWidgetItem ) 

from PyQt5.QtCore import(
    QDir, Qt, pyqtSlot
)

from PyQt5.QtGui import *
import numpy as np
from app.constants.types import Filetype, LogLevel
from app.packages.Hand_Gesture_Recognizer.hand_gesture_detection import VideoDetThread
from app.scripts.helpers import convert_cv_qt



from app.qt import Ui_MainWindow
import app.classes as classes
from app.constants import paths
from app.constants.types import LogLevel, LogColor


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

        #setup logger
        self.logger = classes.Logger(level=LogLevel.INFO)
        self.logger.signalEmitter.message_logged.connect(self.update_log_window)

        self.init_modelOptions()
        self.init_CollTable()
        self.init_ModelTable()
        self.init_DeviceOptions()
        self.init_Params()
        self.init_userModels()
        self.init_ImageViewer()

        self.update_FilesList()
        self.update_resultImgList()
        self.logger.log("The MainWindow has been initialized", LogLevel.INFO)

    def connectSignalsSlots(self):
        self.Btn_ImageDet.clicked.connect(self.openImageDetection)
        self.Btn_ImageDet.setIcon(QIcon("./app/assets/image1.png"))
        self.Btn_VideoDet.clicked.connect(self.openVideoDetection)
        self.Btn_VideoDet.setIcon(QIcon("./app/assets/video1.png"))
        self.Btn_WebcamDet.clicked.connect(self.openWebcamDetection)
        self.Btn_WebcamDet.setIcon(QIcon("./app/assets/webcam1.png"))
        self.list_filenames.itemDoubleClicked.connect(self.displayImageOrig)
        self.list_resultDir.itemDoubleClicked.connect(self.list_resImages_event)
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

        self.combo_model.activated.connect(self.changeTo_MMDetModelMode)
        self.combo_collection.activated.connect(self.changeTo_MMDetModelMode)
        self.combo_usrConfig.activated.connect(self.changeTo_usrModelMode)
        self.combo_usrWeights.activated.connect(self.changeTo_usrModelMode)

        # change SizeAdjustPolicy to none instead of AdjustToContentsOnFirstShow
        # so that it doesn't adjust once the stylesheet is changed
        self.combo_collection.setSizeAdjustPolicy(5)
        self.combo_model.setSizeAdjustPolicy(5)
        self.combo_usrConfig.setSizeAdjustPolicy(5)
        self.combo_usrWeights.setSizeAdjustPolicy(5)
    
    #check which models exist in filepath and add those to dropdown 
    def init_modelOptions(self):
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

    def init_ImageViewer(self): 
        self.qGScene = QGraphicsScene()
        self.qGItemGrp = QGraphicsItemGroup()

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
        qImg = QImage(image_path).scaledToWidth(600)
        qGItemImg = QGraphicsPixmapItem(QPixmap.fromImage(qImg))
        qGItemImg.setTransform(QTransform().translate(-0.5 * qImg.width(), -0.5 * qImg.height()))
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

    def update_log_window(self, message, log_level): 
        item = QListWidgetItem(message, self.list_status)
        item.setBackground(QColor(LogColor[log_level.name].value))
        self.list_status.scrollToBottom()

    def update_ModelTable(self): 
        if(self.imageDet.model != None): 
            self.tb_modelInfo.item(0,0).setText(self.imageDet.model.name)
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

    def update_userModels(self): 
        self.combo_usrConfig.clear() 
        self.combo_usrWeights.clear()
        for c in self.modelHandler.usrCheckpoints: 
            self.combo_usrWeights.addItem(c)
        for c in self.modelHandler.usrConfigs: 
            self.combo_usrConfig.addItem(c)
        self.combo_usrWeights.setCurrentIndex(0)
        self.combo_usrConfig.setCurrentIndex(0)

    def coll_changed(self): 
        if(self.combo_collection.currentIndex() >=0):
            self.imageDet.collection = self.modelHandler.find_collection(self.combo_collection.currentText())
            self.update_CollTable()
            self.update_models()
    
    def device_changed(self): 
        self.imageDet.device = self.modelHandler.devices[self.combo_chooseDevice.currentIndex()].inference_string
        self.logger.log("Device changed to: " + self.imageDet.device, LogLevel.INFO)
    
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
            self.logger.log("model changed to " + self.combo_model.currentText(), LogLevel.INFO)
            self.update_ModelTable()
            self.update_CollTable()
    
    def usrWeights_changed(self): 
        try: 
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
                self.logger.log("weights changed to " + weightsFile, LogLevel.INFO)
                self.update_ModelTable()
                self.update_CollTable()
        except Exception as err: 
            self.logger.log(f"Something went wrong updating the User Config\n: {err}", LogLevel.WARNING)
    
    def usrConfig_changed(self): 
        try: 
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
                self.logger.log("model changed to " + configFile, LogLevel.INFO)
                self.update_ModelTable()
                self.update_CollTable()
        except Exception as err: 
            self.logger.log(f"Something went wrong updating the User Config\n: {err}", LogLevel.WARNING)
    
    def api_changed(self): 
        self.imageDet.api = self.combo_api.currentText()
        self.logger.log("API changed to " + self.combo_api.currentText(), LogLevel.INFO)

    def batchSize_changed(self): 
        self.imageDet.batch_size = float(self.ln_batchSize.text())
        self.logger.log("Batchsize changed to " + str(self.imageDet.batch_size), LogLevel.DEBUG)
    
    def threshhold_changed(self): 
        self.imageDet.score_thr = float(self.ln_threshhold.text())
        self.logger.log("Thresshold changed to "+ str(self.imageDet.score_thr), LogLevel.DEBUG)
    
    def outputDir_changed(self): 
        self.imageDet.out_dir = self.ln_outputDir.text()
        self.logger.log("outputDir changed to " + self.imageDet.out_dir, LogLevel.DEBUG)

    def open_FileDialog_Image(self ): 
        classes.FileDialog(self, Filetype.IMAGE)
        self.update_FilesList() 

    def open_FileDialog_Weights(self): 
        classes.FileDialog(self, Filetype.WEIGHTS)
        self.modelHandler.get_UserModels()
        self.update_userModels()

    def open_FileDialog_Configs(self): 
        classes.FileDialog(self, Filetype.CONFIG)
        self.modelHandler.get_UserModels()
        self.update_userModels()


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
        
        try: 
            #assume the directory exists and contains some files and you want all jpg and JPG files
            dir = QDir(paths.IMAGES)
            filters = ["*.jpg", "*.JPG"]
            dir.setNameFilters(filters)
            for filename in dir.entryList(): 
                self.list_filenames.addItem(filename)
        except Exception as err: 
            return
    
    def update_resultImgList(self): 
        self.list_resultDir.clear()
        path = paths.IMAGES_RES + "/vis/"
        dir = QDir(path)
        #print(path)
        filters = ["*.jpg", "*.JPG"]
        dir.setNameFilters(filters)
        for filename in dir.entryList(): 
            self.list_resultDir.addItem(filename)

    def displayImageOrig(self): 
        path = paths.IMAGES + self.list_filenames.currentItem().text()
        im_cv = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
        self.lb_image_orig.setPixmap(convert_cv_qt(im_cv))

    def list_resImages_event(self): 
        path_img =  paths.IMAGES_RES + "/vis/" + self.list_resultDir.currentItem().text()
        self.update_ResImg(path_img)
        path_pred = paths.IMAGES_RES + "/preds/" +  self.list_resultDir.currentItem().text().replace(".jpg", ".json")
        
        # Load the JSON data from the file
        with open(path_pred) as f:
            data = json.load(f)
            predTable = self.imageDet.getPredTable(data)
            self.update_predTable(predTable)

    def processImage(self): 
        path = ""
        try: 
            path = paths.IMAGES + self.list_filenames.currentItem().text()
        except Exception as err: 
            self.logger.log("Specified Imagepath could not be read", LogLevel.WARNING)
            return
        self.logger.log("Processing Image from Path: {path}", LogLevel.INFO)

        ret = self.imageDet.processImage(path)
        if ret[0] == -1:
            #an error occured 
            err = ret[1]
            self.logger.log(err, LogLevel.ERROR)
            return
        elif(ret[1] != None): 
            self.logger.log(f"Predictions Results for image {path}:\n {ret[1]}", LogLevel.DEBUG)
            self.displayImageRes()
            self.update_predTable(ret[1])
            self.update_resultImgList()
        else: 
            self.logger.log("No objects detected", LogLevel.WARNING )

    def update_predTable(self, predTable): 
        self.ln_ObjectCount.setText("Objects detected: " + str(len(predTable)))
        for r in range(self.tb_predictions.rowCount()): 
            self.tb_predictions.removeRow(0)
        for i, r in enumerate(predTable): 
            self.tb_predictions.insertRow(self.tb_predictions.rowCount())
            self.tb_predictions.setItem(self.tb_predictions.rowCount()-1, 
                        0, QTableWidgetItem(str(r['labelno']),0))
            self.tb_predictions.setItem(self.tb_predictions.rowCount()-1, 
                        1, QTableWidgetItem("{:.2f}%".format(float(r['score'])*100),0))
            self.tb_predictions.setItem(self.tb_predictions.rowCount()-1, 
                        2, QTableWidgetItem(r['labelclass'], 0))
            self.update_resultImgList()

    def displayImageRes(self): 
        path =  self.imageDet.out_dir + "/vis/" + self.list_filenames.currentItem().text()
        self.logger.log("displaying result image at " + path, LogLevel.DEBUG)
        self.update_ResImg(path)
        self.tabWidget.setCurrentIndex(2)

    def openImageDialog(self): 
        Imagedialog = classes.ImageLarge(self)
        Imagedialog.setImage(self)
        Imagedialog.exec()

    
    def changeTo_usrModelMode(self): 
        try: 
            if( not self.imageDet.usrModelMode):
                self.imageDet.usrModelMode = True
                self.combo_collection.setStyleSheet("color: rgba(255, 255, 255, 0.3); \
                                                    border: 1px solid rgba(255, 255, 255, 0.12);")
                self.combo_model.setStyleSheet("color: rgba(255, 255, 255, 0.3); \
                                                border: 1px solid rgba(255, 255, 255, 0.12);")
                self.combo_usrConfig.setStyleSheet("")
                self.combo_usrWeights.setStyleSheet("")

                self.usrConfig_changed()
                self.usrWeights_changed()
                self.logger.log("Swapped to User Model Mode", LogLevel.INFO)
        except Exception as e: 
            self.logger.log("Something went wrong while swapping to UserModelMode:\n{err}", LogLevel.WARNING)
        
    def changeTo_MMDetModelMode(self): 
        try: 
            if(self.imageDet.usrModelMode):
                self.imageDet.usrModelMode = False
                self.combo_usrConfig.setStyleSheet("color: rgba(255, 255, 255, 0.3); \
                                                    border: 1px solid rgba(255, 255, 255, 0.12);")
                self.combo_usrWeights.setStyleSheet("color: rgba(255, 255, 255, 0.3); \
                                                    border: 1px solid rgba(255, 255, 255, 0.12);")
                self.combo_collection.setStyleSheet("")
                self.combo_model.setStyleSheet("")

                self.model_changed()
                self.coll_changed()
                self.logger.log("Swapped to MMDet Model Mode", LogLevel.INFO)

        except Exception as err: 
            self.logger.log("Something went wrong while swapping to UserModelMode:\n{err}", LogLevel.WARNING)

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

    #Webcam
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.lb_webcam.setPixmap(qt_img)

    #WebcamDetection
    @pyqtSlot(np.ndarray)
    def update_imageDet(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.lb_webcamDet.setPixmap(qt_img)