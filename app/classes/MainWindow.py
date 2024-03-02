import json

import cv2
import numpy as np
from PyQt5.QtCore import QDir, Qt, pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QImage, QPixmap, QTransform
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QGraphicsItemGroup,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QHeaderView,
    QListWidgetItem,
    QMainWindow,
    QSlider,
    QTableWidgetItem,
)

import app.classes as classes
from app.classes.CustomLogger import logger
from app.constants import paths
from app.constants.types import DetType, Filetype, LogColor, LogLevel
from app.qt import Ui_MainWindow
from app.scripts.helpers import convert_cv_qt


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        self.imageDet = classes.ImageDet()
        self.webcamDet = classes.WebcamDet()
        self.videoDet = classes.VideoDet()
        self.modelHandler = classes.ModelHandler()

        super().__init__(parent)

        self.setupUi(self)

        # connect signals of frontend events to the handler Functions
        self.connectSignalsSlots_Start()
        self.connectSignalsSlots_ImageDet()
        self.connectSignalsSlots_WebcamDet()
        self.connectSignalsSlots_Results()
        self.connectSignalsSlots_VideoDet()

        logger.signalEmitter.message_logged.connect(self.update_log_window)

        self.init_modelOptions()
        self.init_CollTable()
        self.init_ModelTable()
        self.init_DeviceOptions()
        self.init_Params()
        self.init_userModels()
        self.init_ImageViewer()

        self.update_FilesList()
        self.update_resultImgList()
        logger.log("The MainWindow has been initialized", LogLevel.INFO)

    def connectSignalsSlots_Start(self):
        self.Btn_ImageDet.clicked.connect(self.openImageDetection)
        self.Btn_ImageDet.setIcon(QIcon("./app/assets/image1.png"))
        self.Btn_VideoDet.clicked.connect(self.openVideoDetection)
        self.Btn_VideoDet.setIcon(QIcon("./app/assets/video1.png"))
        self.Btn_WebcamDet.clicked.connect(self.openWebcamDetection)
        self.Btn_WebcamDet.setIcon(QIcon("./app/assets/webcam1.png"))

    def connectSignalsSlots_ImageDet(self):
        self.list_filenames.itemDoubleClicked.connect(self.displayImageOrig)
        self.btn_process.clicked.connect(self.processImage)
        self.ln_batchSize.editingFinished.connect(self.batchSize_changed)
        self.ln_outputDir.editingFinished.connect(self.outputDir_changed)
        self.ln_threshhold.editingFinished.connect(self.threshhold_changed)
        self.btn_uploadConfig.clicked.connect(self.open_FileDialog_Configs)
        self.btn_uploadWeights.clicked.connect(self.open_FileDialog_Weights)

        # Comboboxes
        self.combo_chooseDevice.currentIndexChanged.connect(
            lambda i: self.device_changed(DetType.IMAGEDET)
        )
        self.combo_api.currentIndexChanged.connect(
            lambda i: self.api_changed(DetType.IMAGEDET)
        )
        self.combo_model.currentIndexChanged.connect(
            lambda i: self.model_changed(DetType.IMAGEDET)
        )
        self.combo_collection.currentIndexChanged.connect(
            lambda i: self.coll_changed(DetType.IMAGEDET)
        )
        self.combo_usrConfig.currentIndexChanged.connect(
            lambda i: self.usrConfig_changed(DetType.IMAGEDET)
        )
        self.combo_usrWeights.currentIndexChanged.connect(
            lambda i: self.usrWeights_changed(DetType.IMAGEDET)
        )
        self.combo_model.activated.connect(
            lambda i: self.changeTo_MMDetModelMode(DetType.IMAGEDET)
        )
        self.combo_collection.activated.connect(
            lambda i: self.changeTo_MMDetModelMode(DetType.IMAGEDET)
        )
        self.combo_usrConfig.activated.connect(
            lambda i: self.changeTo_usrModelMode(DetType.IMAGEDET)
        )
        self.combo_usrWeights.activated.connect(
            lambda i: self.changeTo_usrModelMode(DetType.IMAGEDET)
        )

        # change SizeAdjustPolicy to none instead of AdjustToContentsOnFirstShow
        # so that it doesn't adjust once the stylesheet is changed
        self.combo_collection.setSizeAdjustPolicy(5)
        self.combo_model.setSizeAdjustPolicy(5)
        self.combo_usrConfig.setSizeAdjustPolicy(5)
        self.combo_usrWeights.setSizeAdjustPolicy(5)

    def connectSignalsSlots_WebcamDet(self):
        self.btn_startWebcamDet_2.clicked.connect(self.start_WebcamDet)
        self.btn_stopWebcamDet_2.clicked.connect(
            lambda x: self.webcamDet.stop_WebcamDetEvent.set()
        )
        self.combo_chooseDevice_2.currentIndexChanged.connect(
            lambda i: self.device_changed(DetType.WEBCAMDET)
        )
        self.ln_threshhold_2.editingFinished.connect(
            lambda i: self.threshhold_changed(DetType.WEBCAMDET)
        )
        self.btn_uploadConfig_2.clicked.connect(self.open_FileDialog_Configs)
        self.btn_uploadWeights_2.clicked.connect(self.open_FileDialog_Weights)
        self.combo_api_2.currentIndexChanged.connect(
            lambda i: self.api_changed(DetType.WEBCAMDET)
        )
        self.combo_model_2.currentIndexChanged.connect(
            lambda I: self.model_changed(DetType.WEBCAMDET)
        )
        self.combo_usrConfig_2.currentIndexChanged.connect(
            lambda I: self.usrConfig_changed(DetType.WEBCAMDET)
        )
        self.combo_usrWeights_2.currentIndexChanged.connect(
            lambda i: self.usrWeights_changed(DetType.WEBCAMDET)
        )
        self.combo_collection_2.currentIndexChanged.connect(
            lambda i: self.coll_changed(DetType.WEBCAMDET)
        )

        self.combo_model_2.activated.connect(
            lambda i: self.changeTo_MMDetModelMode(DetType.WEBCAMDET)
        )
        self.combo_collection_2.activated.connect(
            lambda i: self.changeTo_MMDetModelMode(DetType.WEBCAMDET)
        )
        self.combo_usrConfig_2.activated.connect(
            lambda i: self.changeTo_usrModelMode(DetType.WEBCAMDET)
        )
        self.combo_usrWeights_2.activated.connect(
            lambda i: self.changeTo_usrModelMode(DetType.WEBCAMDET)
        )

    def connectSignalsSlots_VideoDet(self):
        self.combo_chooseDevice_3.currentIndexChanged.connect(
            lambda i: self.device_changed(DetType.VIDEODET)
        )
        pass

    def connectSignalsSlots_Results(self):
        self.btn_openImageDialog.clicked.connect(self.openImageDialog)
        self.list_resultDir.itemDoubleClicked.connect(self.list_resImages_event)

    # Init functions
    # check which models exist in filepath and add those to dropdown
    def init_modelOptions(self):

        collectionCombos = [
            self.combo_collection,
            self.combo_collection_2,
            self.combo_collection_3,
        ]

        for combo in collectionCombos:
            combo.clear()

            for c in self.modelHandler.collections:
                combo.addItem(c.name)
            combo.setCurrentIndex(-1)

        modelCombos = [self.combo_model, self.combo_model_2, self.combo_model_3]

        # init Model ComboBox
        for combo in modelCombos:
            combo.clear()

            for c in self.modelHandler.collections:
                for m in c.models:
                    combo.addItem(m.name)

    # Init functions
    def init_CollTable(self):
        collectionTables = [self.tb_collInfo, self.tb_collInfo_2, self.tb_collInfo_3]
        for table in collectionTables:
            headerV = table.verticalHeader()
            headerV.setDefaultSectionSize(37)
            headerV.setSectionResizeMode(QHeaderView.ResizeToContents)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def init_ModelTable(self):
        modeltables = [self.tb_modelInfo, self.tb_modelInfo_2, self.tb_modelInfo_3]

        for table in modeltables:
            headerV = table.verticalHeader()
            headerV.setDefaultSectionSize(37)
            headerV.setSectionResizeMode(QHeaderView.ResizeToContents)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def init_DeviceOptions(self):
        deviceCombos = [
            self.combo_chooseDevice,
            self.combo_chooseDevice_2,
            self.combo_chooseDevice_3,
        ]
        for combo in deviceCombos:
            combo.clear()
            for g in self.modelHandler.devices:
                combo.addItem(g.name)

    def init_Params(self):
        self.imageDet.batch_size = 1
        self.imageDet.score_thr = 0.3
        self.imageDet.out_dir = paths.IMAGES_RES
        self.ln_batchSize.setText(str(self.imageDet.batch_size))
        self.ln_threshhold.setText(str(self.imageDet.score_thr))
        self.ln_outputDir.setText(str(self.imageDet.out_dir))

    def init_userModels(self):

        usrWeightsCombos = [
            self.combo_usrWeights,
            self.combo_usrWeights_2,
            self.combo_usrWeights_3,
        ]
        usrConfigsCombos = [
            self.combo_usrConfig,
            self.combo_usrConfig_2,
            self.combo_usrConfig_3,
        ]

        for combo in usrWeightsCombos:
            for c in self.modelHandler.usrCheckpoints:
                combo.addItem(c)
            combo.setCurrentIndex(0)

        for combo in usrConfigsCombos:
            for c in self.modelHandler.usrConfigs:
                combo.addItem(c)
            combo.setCurrentIndex(0)

    # init ImageViewer on Result Page
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

    # update ResultImage on Result Page
    def update_ResImg(self, image_path):
        self.qGScene.clear()
        self.qGItemGrp = QGraphicsItemGroup()
        qImg = QImage(image_path).scaledToWidth(600)
        qGItemImg = QGraphicsPixmapItem(QPixmap.fromImage(qImg))
        qGItemImg.setTransform(
            QTransform().translate(-0.5 * qImg.width(), -0.5 * qImg.height())
        )
        self.qGItemGrp.addToGroup(qGItemImg)
        self.qGScene.addItem(self.qGItemGrp)

    def scaleImg(self, value):
        exp = value * 0.01
        scl = 10.0**exp
        self.qGItemGrp.setTransform(QTransform().scale(scl, scl))

    # update Functions
    def update_CollTable(self):
        self.tb_collInfo.item(0, 0).setText(self.imageDet.collection.name)
        self.tb_collInfo.item(1, 0).setText(
            self.imageDet.collection.metadata.training_data
        )
        self.tb_collInfo.item(2, 0).setText(
            self.imageDet.collection.metadata.training_techniques
        )
        self.tb_collInfo.item(3, 0).setText(
            self.imageDet.collection.metadata.training_resources
        )
        self.tb_collInfo.item(4, 0).setText(
            self.imageDet.collection.metadata.architecture
        )
        self.tb_collInfo.item(5, 0).setText(str(self.imageDet.collection.paper))
        self.tb_collInfo.item(6, 0).setText(self.imageDet.collection.readme)
        self.tb_collInfo.item(7, 0).setText(str(self.imageDet.collection.code))

    def update_log_window(self, message, log_level, det_type=None):
        if det_type == DetType.IMAGEDET or det_type == None:
            item = QListWidgetItem(message, self.list_status)
            item.setBackground(QColor(LogColor[log_level.name].value))
            self.list_status.scrollToBottom()
        if det_type == DetType.WEBCAMDET or det_type == None:
            item = QListWidgetItem(message, self.list_status_2)
            item.setBackground(QColor(LogColor[log_level.name].value))
            self.list_status.scrollToBottom()
        if det_type == DetType.VIDEODET or det_type == None:
            item = QListWidgetItem(message, self.list_status_3)
            item.setBackground(QColor(LogColor[log_level.name].value))
            self.list_status.scrollToBottom()

    def update_ModelTable(self):
        if self.imageDet.model != None:
            self.tb_modelInfo.item(0, 0).setText(self.imageDet.model.name)
            self.tb_modelInfo.item(1, 0).setText(self.imageDet.model.config)
            self.tb_modelInfo.item(2, 0).setText(str(self.imageDet.model.metadata))
            results_string = "\n".join(
                [f"- {result}" for result in self.imageDet.model.results]
            )
            self.tb_modelInfo.item(3, 0).setText(results_string)
            self.tb_modelInfo.item(4, 0).setText(self.imageDet.model.checkpoint)
        else:
            self.tb_modelInfo.item(0, 0).setText(" ")
            self.tb_modelInfo.item(1, 0).setText(" ")
            self.tb_modelInfo.item(2, 0).setText(" ")
            self.tb_modelInfo.item(3, 0).setText(" ")
            self.tb_modelInfo.item(4, 0).setText(" ")

    def update_userModels(self):
        self.combo_usrConfig.clear()
        self.combo_usrWeights.clear()
        for c in self.modelHandler.usrCheckpoints:
            self.combo_usrWeights.addItem(c)
        for c in self.modelHandler.usrConfigs:
            self.combo_usrConfig.addItem(c)
        self.combo_usrWeights.setCurrentIndex(0)
        self.combo_usrConfig.setCurrentIndex(0)

    def coll_changed(self, det_type):
        if det_type == DetType.IMAGEDET:
            if self.combo_collection.currentIndex() >= 0:
                self.imageDet.collection = self.modelHandler.find_collection(
                    self.combo_collection.currentText()
                )
                logger.log(
                    f"Collection changed to: " + self.imageDet.device,
                    LogLevel.INFO,
                    det_type,
                )
        elif det_type == DetType.WEBCAMDET:
            if self.combo_collection.currentIndex() >= 0:
                self.webcamDet.collection = self.modelHandler.find_collection(
                    self.combo_collection.currentText()
                )
                logger.log(
                    f"Collection changed to: " + self.webcamDet.device,
                    LogLevel.INFO,
                    det_type,
                )
        elif det_type == DetType.VIDEODET:
            if self.combo_collection.currentIndex() >= 0:
                self.videoDet.collection = self.modelHandler.find_collection(
                    self.combo_collection.currentText()
                )
                logger.log(
                    f"Collection changed to: " + self.videoDet.device,
                    LogLevel.INFO,
                    det_type,
                )
        self.update_CollTable()
        self.update_models()

    def device_changed(self, det_type):
        if det_type == DetType.IMAGEDET:
            self.imageDet.device = self.modelHandler.devices[
                self.combo_chooseDevice.currentIndex()
            ].inference_string
            logger.log(
                f"Device changed to: " + self.imageDet.device, LogLevel.INFO, det_type
            )
        elif det_type == DetType.WEBCAMDET:
            self.webcamDet.device = self.modelHandler.devices[
                self.combo_chooseDevice_2.currentIndex()
            ].inference_string
            logger.log(
                f"Device changed to: " + self.webcamDet.device, LogLevel.INFO, det_type
            )
        elif det_type == DetType.VIDEODET:
            self.videoDet.device = self.modelHandler.devices[
                self.combo_chooseDevice_3.currentIndex()
            ].inference_string
            logger.log(
                f"Device changed to: " + self.videoDet.device, LogLevel.INFO, det_type
            )

    def update_models(self):
        # init Model ComboBox
        self.combo_model.clear()
        self.imageDet.model = None
        for m in self.imageDet.collection.models:
            self.combo_model.addItem(m.name)

    def model_changed(self, det_type):
        if det_type == DetType.IMAGEDET:
            if self.combo_model.currentIndex() >= 0:
                self.imageDet.model = self.modelHandler.find_model(
                    self.combo_model.currentText()
                )
                self.imageDet.collection = self.modelHandler.find_collection(
                    self.imageDet.model.collection
                )
                logger.log(
                    "model changed to " + self.combo_model.currentText(),
                    LogLevel.INFO,
                    det_type,
                )
                self.update_ModelTable()
                self.update_CollTable()
        elif det_type == DetType.WEBCAMDET:
            if self.combo_model_2.currentIndex() >= 0:
                self.webcamDet.model = self.modelHandler.find_model(
                    self.combo_model_2.currentText()
                )
                self.webcamDet.collection = self.modelHandler.find_collection(
                    self.webcamDet.model.collection
                )
                logger.log(
                    "model changed to " + self.combo_model_2.currentText(),
                    LogLevel.INFO,
                    det_type,
                )
                self.update_ModelTable()
                self.update_CollTable()
        elif det_type == DetType.VIDEODET:
            if self.combo_model_3.currentIndex() >= 0:
                self.videoDet.model = self.modelHandler.find_model(
                    self.combo_model_3.currentText()
                )
                self.videoDet.collection = self.modelHandler.find_collection(
                    self.videoDet.model.collection
                )
                logger.log(
                    f"model changed to {self.combo_model_3.currentText()}",
                    LogLevel.INFO,
                    det_type,
                )
                self.update_ModelTable()
                self.update_CollTable()

    def usrWeights_changed(self, det_type):

        combos = [
            self.combo_usrWeights,
            self.combo_usrWeights_2,
            self.combo_usrWeights_3,
        ]
        combo = combos[self.detTypeToNumber(det_type)]

        detObject = self.detTypeToDetObject(det_type)
        try:
            if combo.currentIndex() >= 0 and detObject is not None:

                weightsFile = combo.currentText()

                if detObject.model.collection != "User":
                    detObject.collection = classes.Collection("USER")
                    detObject.model = classes.Model(
                        name="",
                        collection="User",
                        metadata=None,
                        config=None,
                        checkpoint=paths.USER_WEIGHTS + weightsFile,
                    )
                else:
                    detObject.model.checkpoint = paths.USER_WEIGHTS + weightsFile
                logger.log(f"weights changed to {weightsFile}", LogLevel.INFO, det_type)
                self.update_ModelTable()
                self.update_CollTable()
        except Exception as err:
            logger.log(
                f"Something went wrong updating the User Config\n: {err}",
                LogLevel.WARNING,
                det_type,
            )

    def detTypeToDetObject(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.imageDet
        elif det_type == DetType.WEBCAMDET:
            return self.webcamDet
        elif det_type == DetType.VIDEODET:
            return self.videoDet

    def detTypeToNumber(self, det_type):
        if det_type == DetType.IMAGEDET:
            return 0
        elif det_type == DetType.WEBCAMDET:
            return 1
        elif det_type == DetType.VIDEODET:
            return 2
        return -1

    def usrConfig_changed(self, det_type):
        combos = [self.combo_usrConfig, self.combo_usrConfig_2, self.combo_usrConfig_3]
        combo = combos[self.detTypeToNumber(det_type)]

        detObject = self.detTypeToDetObject(det_type)

        try:
            if combo.currentIndex() >= 0 and detObject != None:

                configFile = combo.currentText()
                name = configFile.strip(".py")

                if detObject.model != None and detObject.model.collection != "User":
                    detObject.collection = classes.Collection("USER")

                    detObject.model = classes.Model(
                        name=name,
                        collection="User",
                        metadata=None,
                        config=paths.USER_CONFIGS + configFile,
                        checkpoint=None,
                    )
                else:
                    detObject.model.name = name
                    detObject.model.config = paths.USER_CONFIGS + configFile
                logger.log(f"model changed to {configFile}", LogLevel.INFO, det_type)
                self.update_ModelTable()
                self.update_CollTable()
        except Exception as err:
            logger.log(
                f"Something went wrong updating the User Config\n: {err}",
                LogLevel.WARNING,
                det_type,
            )

    def api_changed(self, det_type):
        if det_type == DetType.IMAGEDET:
            self.imageDet.api = self.combo_api.currentText()
        elif det_type == DetType.WEBCAMDET:
            self.webcamDet.api = self.combo_api_2.currentText()
        elif det_type == DetType.VIDEODET:
            self.videoDet.api = self.combo_api_3.currentText()
        logger.log(
            f"API changed to {self.combo_api.currentText()}", LogLevel.DEBUG, det_type
        )

    def batchSize_changed(self, det_type):
        if det_type == DetType.IMAGEDET:
            self.imageDet.batch_size = int(self.ln_batchSize.text())
        elif det_type == DetType.VIDEODET:
            self.videoDet.batch_size = int(self.ln_batchSize_3.text())
        logger.log(
            f"Batchsize changed to {str(self.imageDet.batch_size)}",
            LogLevel.DEBUG,
            det_type,
        )

    def threshhold_changed(self, det_type):
        if det_type == DetType.IMAGEDET:
            self.imageDet.score_thr = float(self.ln_threshhold.text())
        elif det_type == DetType.WEBCAMDET:
            self.webcamDet.score_thr = float(self.ln_threshhold_2.text())
        elif det_type == DetType.VIDEODET:
            self.videoDet.score_thr = float(self.ln_threshhold_3.text())
        logger.log(
            f"Thresshold changed to {str(self.imageDet.score_thr)}",
            LogLevel.DEBUG,
            det_type,
        )

    def outputDir_changed(self, det_type):
        if det_type == DetType.IMAGEDET:
            self.imageDet.out_dir = self.ln_outputDir.text()
        elif det_type == DetType.VIDEODET:
            self.videoDet.out_dir = self.ln_outputDir_3.text()
        logger.log(
            f"outputDir changed to {self.imageDet.out_dir}", LogLevel.DEBUG, det_type
        )

    def open_FileDialog_Image(self):
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

    # Sonstige Funktionen
    def openImageDetection(self):
        self.tabWidget.setCurrentIndex(1)
        self.update_FilesList()

    def openVideoDetection(self):
        self.tabWidget.setCurrentIndex(2)

    def openWebcamDetection(self):
        self.tabWidget.setCurrentIndex(3)

    def update_FilesList(self):
        # clear list:
        self.list_filenames.clear()

        try:
            # assume the directory exists and contains some files and you want all jpg and JPG files
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
        # print(path)
        filters = ["*.jpg", "*.JPG"]
        dir.setNameFilters(filters)
        for filename in dir.entryList():
            self.list_resultDir.addItem(filename)

    def displayImageOrig(self):
        path = paths.IMAGES + self.list_filenames.currentItem().text()
        im_cv = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
        self.lb_image_orig.setPixmap(convert_cv_qt(im_cv))

    def list_resImages_event(self):
        path_img = paths.IMAGES_RES + "/vis/" + self.list_resultDir.currentItem().text()
        self.update_ResImg(path_img)
        path_pred = (
            paths.IMAGES_RES
            + "/preds/"
            + self.list_resultDir.currentItem().text().replace(".jpg", ".json")
        )

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
            logger.log("Specified Imagepath could not be read", LogLevel.WARNING)
            return
        logger.log("Processing Image from Path: {path}", LogLevel.INFO)

        ret = self.imageDet.process(path)
        if ret[0] == -1:
            # an error occured
            err = ret[1]
            logger.log(err, LogLevel.ERROR)
            return
        elif ret[1] != None:
            logger.log(
                f"Predictions Results for image {path}:\n {ret[1]}", LogLevel.DEBUG
            )
            self.displayImageRes()
            self.update_predTable(ret[1])
            self.update_resultImgList()
        else:
            logger.log("No objects detected", LogLevel.WARNING)

    def update_predTable(self, predTable):
        self.ln_ObjectCount.setText("Objects detected: " + str(len(predTable)))
        for r in range(self.tb_predictions.rowCount()):
            self.tb_predictions.removeRow(0)
        for i, r in enumerate(predTable):
            self.tb_predictions.insertRow(self.tb_predictions.rowCount())
            self.tb_predictions.setItem(
                self.tb_predictions.rowCount() - 1,
                0,
                QTableWidgetItem(str(r["labelno"]), 0),
            )
            self.tb_predictions.setItem(
                self.tb_predictions.rowCount() - 1,
                1,
                QTableWidgetItem("{:.2f}%".format(float(r["score"]) * 100), 0),
            )
            self.tb_predictions.setItem(
                self.tb_predictions.rowCount() - 1,
                2,
                QTableWidgetItem(r["labelclass"], 0),
            )
            self.update_resultImgList()

    def displayImageRes(self):
        path = (
            self.imageDet.out_dir + "/vis/" + self.list_filenames.currentItem().text()
        )
        logger.log("displaying result image at " + path, LogLevel.DEBUG)
        self.update_ResImg(path)
        self.tabWidget.setCurrentIndex(2)

    def openImageDialog(self):
        Imagedialog = classes.ImageLarge(self)
        Imagedialog.setImage(self)
        Imagedialog.exec()

    def changeTo_usrModelMode(self, det_type):
        combosConfig = [
            self.combo_usrConfig,
            self.combo_usrConfig_2,
            self.combo_usrConfig_3,
        ]
        combosCheckpoint = [
            self.combo_usrWeights,
            self.combo_usrWeights_2,
            self.combo_usrWeights_3,
        ]
        combosCollection = [
            self.combo_collection,
            self.combo_collection_2,
            self.combo_collection_3,
        ]
        combosModel = [self.combo_model, self.combo_model_2, self.combo_model_3]
        n = self.detTypeToNumber(det_type)
        combo_config = combosConfig[n]
        combo_checkpoint = combosCheckpoint[n]
        combo_collection = combosCollection[n]
        combo_model = combosModel[n]
        detObject = self.detTypeToDetObject(det_type)
        try:
            if detObject is not None and not self.imageDet.usrModelMode:
                detObject.usrModelMode = True
                combo_collection.setStyleSheet(
                    "color: rgba(255, 255, 255, 0.3); \
                                                    border: 1px solid rgba(255, 255, 255, 0.12);"
                )
                combo_model.setStyleSheet(
                    "color: rgba(255, 255, 255, 0.3); \
                                                border: 1px solid rgba(255, 255, 255, 0.12);"
                )
                combo_config.setStyleSheet("")
                combo_checkpoint.setStyleSheet("")

                self.usrConfig_changed(det_type)
                self.usrWeights_changed(det_type)
                logger.log("Swapped to User Model Mode", LogLevel.INFO, det_type)
        except Exception as e:
            logger.log(
                "Something went wrong while swapping to UserModelMode:\n{err}",
                LogLevel.WARNING,
                det_type,
            )

    def changeTo_MMDetModelMode(self, det_type):
        combosConfig = [
            self.combo_usrConfig,
            self.combo_usrConfig_2,
            self.combo_usrConfig_3,
        ]
        combosCheckpoint = [
            self.combo_usrWeights,
            self.combo_usrWeights_2,
            self.combo_usrWeights_3,
        ]
        combosCollection = [
            self.combo_collection,
            self.combo_collection_2,
            self.combo_collection_3,
        ]
        combosModel = [self.combo_model, self.combo_model_2, self.combo_model_3]
        n = self.detTypeToNumber(det_type)
        combo_config = combosConfig[n]
        combo_checkpoint = combosCheckpoint[n]
        combo_collection = combosCollection[n]
        combo_model = combosModel[n]
        detObject = self.detTypeToDetObject(det_type)
        try:
            if detObject is not None and detObject.usrModelMode:
                detObject.usrModelMode = False
                combo_config.setStyleSheet(
                    "color: rgba(255, 255, 255, 0.3); \
                                                    border: 1px solid rgba(255, 255, 255, 0.12);"
                )
                combo_checkpoint.setStyleSheet(
                    "color: rgba(255, 255, 255, 0.3); \
                                                    border: 1px solid rgba(255, 255, 255, 0.12);"
                )
                combo_collection.setStyleSheet("")
                combo_model.setStyleSheet("")

                self.model_changed(det_type)
                self.coll_changed(det_type)
                logger.log(
                    f"Swapped to MMDet Model Mode for {det_type}",
                    LogLevel.INFO,
                    det_type,
                )

        except Exception as err:
            logger.log(
                "Something went wrong while swapping to UserModelMode:\n{err}",
                LogLevel.WARNING,
                det_type,
            )

    # Webcam Detection
    def start_WebcamDet(self):
        try:
            self.webcamDet.run(self)
        except Exception as err:
            logger.log(f"{err}", LogLevel.ERROR, det_type=DetType.WEBCAMDET)

    # Webcam
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.lb_webcam.setPixmap(qt_img)

    # WebcamDetection
    @pyqtSlot(np.ndarray)
    def update_imageDet(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.lb_webcamDet_2.setPixmap(qt_img)
