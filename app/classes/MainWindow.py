import sys
from threading import Event
import cv2

from PyQt5.QtWidgets import (QApplication, QMainWindow,QHeaderView, QAbstractItemView ) 

from PyQt5.QtCore import(
    QDir, pyqtSlot
)

from PyQt5.QtGui import *
import numpy as np
from packages.Hand_Gesture_Recognizer.hand_gesture_detection import VideoDetThread
from scripts.helpers import convert_cv_qt



from qt import Ui_MainWindow
import classes
from constants import paths
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
        self.combo_model.currentIndexChanged.connect(self.model_changed)
        self.combo_collection.currentIndexChanged.connect(self.coll_changed)
        self.combo_api.currentIndexChanged.connect(self.api_changed)
        self.btn_addImage.clicked.connect(self.open_FileDialog)
        self.btn_startWebcam.clicked.connect(self.startWebcam)
        self.btn_startWebcamDet.clicked.connect(self.startHandGestureRecog)
        self.btn_stopWebcamDet.clicked.connect(lambda x: self.stopHandGestureRecogEvent.set())
        self.combo_chooseDevice.currentIndexChanged.connect(self.device_changed)
        self.ln_batchSize.editingFinished.connect(self.batchSize_changed)
        self.ln_outputDir.editingFinished.connect(self.outputDir_changed)
        self.ln_threshhold.editingFinished.connect(self.threshhold_changed)
    
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
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerV = self.tb_collInfo.verticalHeader()
        headerV.setDefaultSectionSize(37)
        headerV.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_collInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        

    def init_ModelTable(self): 
        header = self.tb_modelInfo.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
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
            self.list_status.addItem("-model changed to " + self.combo_model.currentText())
            self.update_ModelTable()
    
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

    def open_FileDialog(self): 
        app = classes.FileDialog(self)
        #sys.exit(app.exec_())

    #    app = QApplication(sys.argv)
    #    ex = classes.FileDialog(self)
    #    sys.exit(app.exec_())

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

        self.list_status.addItem("processing Image...")
        ret = self.imageDet.processImage(path)
        if(ret != None): 
            self.displayImageRes()
            self.ln_ObjectCount.setText("Objects detected: " + str(len(ret)))
            self.txt_PredDump.setText("Predictions: " + str(ret))
        else: self.list_status.addItem("processing Image didnt work")
        

    def displayImageRes(self): 
        path =  paths.IMAGES_RES + "/vis/" + self.list_filenames.currentItem().text()
        im_cv = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
        self.lb_image_res.setPixmap(convert_cv_qt(im_cv))
        self.list_status.addItem("trying to display Result image")

    def openImageDialog(self): 
        Imagedialog = classes.ImageLarge(self)
        Imagedialog.setImage(self)
        Imagedialog.exec()


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