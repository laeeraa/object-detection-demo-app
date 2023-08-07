from threading import Event
import cv2

from PyQt5.QtWidgets import (QMainWindow,QHeaderView ) 

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
        self.loadImages()
        self.initModelOptions()
        self.init_CollTable()
        self.init_ModelTable()

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
        self.combo_api.currentIndexChanged.connect(self.apichanged)
        self.btn_addImage.clicked.connect(self.addImage)
        self.btn_startWebcam.clicked.connect(self.startWebcam)
        self.btn_startWebcamDet.clicked.connect(self.startHandGestureRecog)
        self.btn_stopWebcamDet.clicked.connect(lambda x: self.stopHandGestureRecogEvent.set())
    
    #check which models exist in filepath and add those to dropdown 
    def initModelOptions(self):
        #init Collections Combo Box
        self.combo_collection.clear()
        for c in self.modelHandler.collections: 
            self.combo_collection.addItem(c.name)
        self.combo_collection.setCurrentIndex(-1)
        self.combo_collection.setCurrentText("Choose a collection")
       
        #init Model ComboBox
        self.combo_model.clear()
        
        for c in self.modelHandler.collections:
            for m in c.models: 
                self.combo_model.addItem(m.name)

        self.combo_model.setCurrentIndex(-1)
        self.combo_model.setCurrentText("Choose a model")
        self.combo_api.setCurrentIndex(-1)
        self.combo_api.setCurrentText("Choose an API")

    def openImageDetection(self):
        self.tabWidget.setCurrentIndex(1)
        self.loadImages()

    def openVideoDetection(self):
        self.tabWidget.setCurrentIndex(2)
    
    def openWebcamDetection(self):
        self.tabWidget.setCurrentIndex(3)
    
    def loadImages(self):
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

    def init_CollTable(self): 
        header = self.tb_collInfo.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def init_ModelTable(self): 
        header = self.tb_modelInfo.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
    
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
        self.tb_modelInfo.item(0,0).setText(self.imageDet.model.name)
        self.tb_modelInfo.item(1,0).setText(self.imageDet.model.config)
        self.tb_modelInfo.item(2,0).setText(str(self.imageDet.model.metadata))
        self.tb_modelInfo.item(3,0).setText(str(self.imageDet.model.results))
        self.tb_modelInfo.item(4,0).setText(self.imageDet.model.weights)

    def coll_changed(self): 
        if(self.combo_collection.currentIndex() >=0):
            self.imageDet.collection = self.modelHandler.find_collection(self.combo_collection.currentText())
            self.update_CollTable()
    
    def model_changed(self): 
        if(self.combo_model.currentIndex() >= 0):
            self.imageDet.model = self.modelHandler.find_model(self.combo_model.currentText())
            self.list_status.addItem("-model changed to " + self.combo_model.currentText())
            self.update_ModelTable()

    def modelchanged(self): 
        #self.imageDet.changemodelconfig(self.modelHandler.models[self.combo_model.currentIndex()])
        self.update
        #self.tb_collInfo.setItem("")
        self.list_status.addItem("-model changed to " + self.combo_model.currentText())
    
    def apichanged(self): 
        self.imageDet.api = self.combo_api.currentText()
        self.list_status.addItem("-API changed to " + self.combo_api.currentText())

    def addImage(self): 
        app = classes.FileDialog(self)
        app.exec()
        #sys.exit(app.exec_())

    # def updateModelInfo(){
    #     metafile_json = self.modelHandler.models[self.combo_model.currentIndex()].configpath
    # }

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