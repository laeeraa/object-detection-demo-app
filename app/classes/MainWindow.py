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
from app.constants.types import (
    STYLESHEET_DISABLED,
    STYLESHEET_ENABLED,
    DetType,
    Filetype,
    LogColor,
    LogLevel,
)
from app.qt import Ui_MainWindow
from app.scripts.helpers import convert_cv_qt, get_available_cameras


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
        self.init_cameras()

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
        self.btn_process.clicked.connect(self.process_image)
        self.ln_batchSize.editingFinished.connect(self.batchSize_changed)
        self.ln_outputDir.editingFinished.connect(
            lambda i=None: self.outputDir_changed(DetType.IMAGEDET)
        )
        self.ln_threshhold.editingFinished.connect(
            lambda i=None: self.threshhold_changed(DetType.IMAGEDET)
        )
        self.btn_uploadConfig.clicked.connect(self.open_FileDialog_Configs)
        self.btn_uploadWeights.clicked.connect(self.open_FileDialog_Weights)

        # Comboboxes
        self.combo_chooseDevice.currentIndexChanged.connect(
            lambda i=None: self.device_changed(DetType.IMAGEDET)
        )
        self.combo_api.currentIndexChanged.connect(
            lambda i=None: self.api_changed(DetType.IMAGEDET)
        )
        self.combo_model.currentIndexChanged.connect(
            lambda i=None: self.model_changed(DetType.IMAGEDET)
        )
        self.combo_collection.currentIndexChanged.connect(
            lambda i=None: self.collection_changed(DetType.IMAGEDET)
        )
        self.combo_usrConfig.currentIndexChanged.connect(
            lambda i=None: self.usrConfig_changed(DetType.IMAGEDET)
        )
        self.combo_usrWeights.currentIndexChanged.connect(
            lambda i=None: self.usrWeights_changed(DetType.IMAGEDET)
        )
        self.combo_model.activated.connect(
            lambda i=None: self.changeTo_MMDetModelMode(DetType.IMAGEDET)
        )
        self.combo_collection.activated.connect(
            lambda i=None: self.changeTo_MMDetModelMode(DetType.IMAGEDET)
        )
        self.combo_usrConfig.activated.connect(
            lambda i=None: self.changeTo_usrModelMode(DetType.IMAGEDET)
        )
        self.combo_usrWeights.activated.connect(
            lambda i=None: self.changeTo_usrModelMode(DetType.IMAGEDET)
        )

        # change SizeAdjustPolicy to none instead of AdjustToContentsOnFirstShow
        # so that it doesn't adjust once the stylesheet is changed
        self.combo_collection.setSizeAdjustPolicy(5)
        self.combo_model.setSizeAdjustPolicy(5)
        self.combo_usrConfig.setSizeAdjustPolicy(5)
        self.combo_usrWeights.setSizeAdjustPolicy(5)

    def connectSignalsSlots_WebcamDet(self):
        self.btn_startWebcamDet_2.clicked.connect(self.start_webcam_det)
        self.btn_stopWebcamDet_2.clicked.connect(self.stop_webcam_det)
        self.combo_chooseDevice_2.currentIndexChanged.connect(
            lambda i=None: self.device_changed(DetType.WEBCAMDET)
        )
        self.ln_threshhold_2.editingFinished.connect(
            lambda i=None: self.threshhold_changed(DetType.WEBCAMDET)
        )
        self.btn_uploadConfig_2.clicked.connect(self.open_FileDialog_Configs)
        self.btn_uploadWeights_2.clicked.connect(self.open_FileDialog_Weights)
        self.combo_api_2.currentIndexChanged.connect(
            lambda i=None: self.api_changed(DetType.WEBCAMDET)
        )
        self.combo_model_2.currentIndexChanged.connect(
            lambda i=None: self.model_changed(DetType.WEBCAMDET)
        )
        self.combo_usrConfig_2.currentIndexChanged.connect(
            lambda i=None: self.usrConfig_changed(DetType.WEBCAMDET)
        )
        self.combo_usrWeights_2.currentIndexChanged.connect(
            lambda i=None: self.usrWeights_changed(DetType.WEBCAMDET)
        )
        self.combo_collection_2.currentIndexChanged.connect(
            lambda i=None: self.collection_changed(DetType.WEBCAMDET)
        )

        self.combo_model_2.activated.connect(
            lambda i=None: self.changeTo_MMDetModelMode(DetType.WEBCAMDET)
        )
        self.combo_collection_2.activated.connect(
            lambda i=None: self.changeTo_MMDetModelMode(DetType.WEBCAMDET)
        )
        self.combo_usrConfig_2.activated.connect(
            lambda i=None: self.changeTo_usrModelMode(DetType.WEBCAMDET)
        )
        self.combo_usrWeights_2.activated.connect(
            lambda i=None: self.changeTo_usrModelMode(DetType.WEBCAMDET)
        )
        self.combo_chooseCamera.currentIndexChanged.connect(self.camera_changed)

    def connectSignalsSlots_VideoDet(self):
        self.combo_chooseDevice_3.currentIndexChanged.connect(
            lambda i=None: self.device_changed(DetType.VIDEODET)
        )
        pass

    def connectSignalsSlots_Results(self):
        self.btn_openImageDialog.clicked.connect(self.open_image_dialog)
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

    def init_cameras(self):
        available_cameras = get_available_cameras()
        for c in available_cameras:
            self.combo_chooseCamera.addItem(str(c))

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
        qSlider.valueChanged.connect(self.scale_image)

    # update ResultImage on Result Page
    def update_result_image(self, image_path):
        self.qGScene.clear()
        self.qGItemGrp = QGraphicsItemGroup()
        qImg = QImage(image_path).scaledToWidth(600)
        qGItemImg = QGraphicsPixmapItem(QPixmap.fromImage(qImg))
        qGItemImg.setTransform(
            QTransform().translate(-0.5 * qImg.width(), -0.5 * qImg.height())
        )
        self.qGItemGrp.addToGroup(qGItemImg)
        self.qGScene.addItem(self.qGItemGrp)

    def scale_image(self, value):
        exp = value * 0.01
        scl = 10.0**exp
        self.qGItemGrp.setTransform(QTransform().scale(scl, scl))

    # update Functions
    def update_collection_table(self, det_type):
        tb_coll_info = self.get_tb_coll_info(det_type)
        det_object = self.get_det_object(det_type)
        if tb_coll_info and det_object:
            tb_coll_info.item(0, 0).setText(det_object.collection.name)
            tb_coll_info.item(1, 0).setText(
                det_object.collection.metadata.training_data
            )
            tb_coll_info.item(2, 0).setText(
                det_object.collection.metadata.training_techniques
            )
            tb_coll_info.item(3, 0).setText(
                det_object.collection.metadata.training_resources
            )
            tb_coll_info.item(4, 0).setText(det_object.collection.metadata.architecture)
            tb_coll_info.item(5, 0).setText(str(det_object.collection.paper))
            tb_coll_info.item(6, 0).setText(det_object.collection.readme)
            tb_coll_info.item(7, 0).setText(str(det_object.collection.code))

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

    def update_model_table(self, det_type):
        tb_model_info = self.get_tb_model_info(det_type)
        det_object = self.get_det_object(det_type)
        if det_object and tb_model_info:
            if det_object.model != None:
                tb_model_info.item(0, 0).setText(det_object.model.name)
                tb_model_info.item(1, 0).setText(det_object.model.config)
                tb_model_info.item(2, 0).setText(str(det_object.model.metadata))
                results_string = "\n".join(
                    [f"- {result}" for result in det_object.model.results]
                )
                tb_model_info.item(3, 0).setText(results_string)
                tb_model_info.item(4, 0).setText(det_object.model.checkpoint)
            else:
                tb_model_info.item(0, 0).setText(" ")
                tb_model_info.item(1, 0).setText(" ")
                tb_model_info.item(2, 0).setText(" ")
                tb_model_info.item(3, 0).setText(" ")
                tb_model_info.item(4, 0).setText(" ")

    def update_user_models(self):
        det_types = [DetType.IMAGEDET, DetType.WEBCAMDET, DetType.VIDEODET]
        for det_type in det_types:
            combo_usrConfig = self.get_combo_usrConfig(det_type)
            combo_usrCheckpoint = self.get_combo_usrCheckpoint(det_type)
            if combo_usrConfig and combo_usrCheckpoint:
                combo_usrConfig.clear()
                combo_usrCheckpoint.clear()
                for c in self.modelHandler.usrCheckpoints:
                    combo_usrCheckpoint.addItem(c)
                for c in self.modelHandler.usrConfigs:
                    combo_usrConfig.addItem(c)
                combo_usrCheckpoint.setCurrentIndex(0)
                combo_usrConfig.setCurrentIndex(0)

    def collection_changed(self, det_type):
        combo_collection = self.get_combo_collection(det_type)
        det_object = self.get_det_object(det_type)
        if det_object and combo_collection:
            if combo_collection.currentIndex() >= 0:
                det_object.collection = self.modelHandler.find_collection(
                    combo_collection.currentText()
                )
                logger.log(
                    f"Collection changed to: " + combo_collection.currentText(),
                    LogLevel.INFO,
                    det_type,
                )
            self.update_collection_table(det_type)
            self.update_models(det_type)

    def device_changed(self, det_type):
        det_object = self.get_det_object(det_type)
        combo_device = self.get_combo_device(det_type)
        if det_object and combo_device:
            self.imageDet.device = self.modelHandler.devices[
                combo_device.currentIndex()
            ].inference_string
            logger.log(
                f"Device changed to: " + det_object.device, LogLevel.INFO, det_type
            )

    def camera_changed(self):
        self.webcamDet.camera_id = int(self.combo_chooseCamera.currentText())
        logger.log(
                f"Camera Id chosen: " + self.webcamDet.camera_id, LogLevel.INFO, DetType.WEBCAMDET
            )

    def update_models(self, det_type):
        combo_model = self.get_combo_model(det_type)
        det_object = self.get_det_object(det_type)
        # init Model ComboBox
        if det_object and combo_model:
            combo_model.clear()
            det_object.model = None
            for m in det_object.collection.models:
                combo_model.addItem(m.name)

    def model_changed(self, det_type):

        combo_model = self.get_combo_model(det_type)
        det_object = self.get_det_object(det_type)

        if not combo_model.currentIndex() >= 0:
            logger.log("no model config chosen", LogLevel.WARNING, det_type)
        elif det_object and combo_model:
            det_object.model = self.modelHandler.find_model(combo_model.currentText())
            det_object.collection = self.modelHandler.find_collection(
                det_object.model.collection
            )
            logger.log(
                "model changed to " + combo_model.currentText(),
                LogLevel.INFO,
                det_type,
            )
            self.update_model_table(det_type)
            self.update_collection_table(det_type)
        else:
            logger.log(
                "det_object or combo_model not defined", LogLevel.WARNING, det_type
            )

    def usrWeights_changed(self, det_type):
        combo = self.get_combo_usrCheckpoint(det_type)
        det_object = self.get_det_object(det_type)
        try:
            if combo.currentIndex() >= 0 and det_object is not None:

                weightsFile = combo.currentText()

                if det_object.model.collection != "User":
                    det_object.collection = classes.Collection("USER")
                    det_object.model = classes.Model(
                        name="",
                        collection="User",
                        metadata=None,
                        config=None,
                        checkpoint=paths.USER_WEIGHTS + weightsFile,
                    )
                else:
                    det_object.model.checkpoint = paths.USER_WEIGHTS + weightsFile
                logger.log(
                    f"checkpoint changed to {weightsFile}", LogLevel.INFO, det_type
                )
                self.update_model_table(det_type)
                self.update_collection_table(det_type)
        except Exception as err:
            logger.log(
                f"Something went wrong updating the User Checkpoint\n: {err}",
                LogLevel.WARNING,
                det_type,
            )

    def usrConfig_changed(self, det_type):
        combo = self.get_combo_usrConfig(det_type)
        det_object = self.get_det_object(det_type)
        try:
            if (
                combo is not None
                and combo.currentIndex() >= 0
                and det_object is not None
            ):

                configFile = combo.currentText()
                name = configFile.strip(".py")

                if det_object.model != None and det_object.model.collection != "User":
                    det_object.collection = classes.Collection("USER")

                    det_object.model = classes.Model(
                        name=name,
                        collection="User",
                        metadata=None,
                        config=paths.USER_CONFIGS + configFile,
                        checkpoint=None,
                    )
                else:
                    det_object.model.name = name
                    det_object.model.config = paths.USER_CONFIGS + configFile
                logger.log(f"model changed to {configFile}", LogLevel.INFO, det_type)
                self.update_model_table(det_type)
                self.update_collection_table(det_type)
        except Exception as err:
            logger.log(
                f"Something went wrong updating the User Config\n: {err}",
                LogLevel.WARNING,
                det_type,
            )

    def api_changed(self, det_type):

        combo_api = self.get_combo_api(det_type)
        det_object = self.get_det_object(det_type)
        if combo_api and det_object:
            det_object.api = combo_api.currentText()
            logger.log(
                f"API changed to {combo_api.currentText()}",
                LogLevel.INFO,
                det_type,
            )
            if det_type == DetType.WEBCAMDET:
                self.set_style_webcamDet()

    def set_style_webcamDet(self):
        qtObjects = [
            self.combo_collection_2,
            self.combo_model_2,
            self.combo_usrConfig_2,
            self.combo_usrWeights_2,
            self.ln_threshhold_2,
        ]
        for q in qtObjects:
            if self.webcamDet.api == "TechVidvan":
                q.setStyleSheet(STYLESHEET_DISABLED)
            else:
                q.setStyleSheet(STYLESHEET_ENABLED)
                if self.webcamDet.usrModelMode:
                    self.combo_collection_2.setStyleSheet(STYLESHEET_DISABLED)
                    self.combo_model_2.setStyleSheet(STYLESHEET_DISABLED)
                else:
                    self.combo_usrConfig_2.setStyleSheet(STYLESHEET_DISABLED)
                    self.combo_usrWeights_2(STYLESHEET_DISABLED)

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
        self.update_user_models()

    def open_FileDialog_Configs(
        self,
    ):
        classes.FileDialog(self, Filetype.CONFIG)
        self.modelHandler.get_UserModels()
        self.update_user_models()

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
        self.update_result_image(path_img)
        path_pred = (
            paths.IMAGES_RES
            + "/preds/"
            + self.list_resultDir.currentItem().text().replace(".jpg", ".json")
        )

        # Load the JSON data from the file
        with open(path_pred) as f:
            data = json.load(f)
            predTable = self.imageDet.getPredTable(data)
            self.update_prediction_table(predTable)

    def process_image(self, det_type=DetType.IMAGEDET):
        path = ""
        try:
            path = paths.IMAGES + self.list_filenames.currentItem().text()
        except Exception as err:
            logger.log(
                "Specified Imagepath could not be read", LogLevel.WARNING, det_type
            )
            return
        logger.log(f"Processing Image from Path: {path}", LogLevel.INFO, det_type)

        ret = self.imageDet.process(path)
        if ret[0] == -1:
            # an error occured
            err = ret[1]
            logger.log(err, LogLevel.ERROR, det_type)
            return
        elif ret[1] != None:
            logger.log(
                f"Predictions Results for image {path}:\n {ret[1]}",
                LogLevel.DEBUG,
                det_type,
            )
            self.display_result_image()
            self.update_prediction_table(ret[1])
            self.update_resultImgList()
        else:
            logger.log("No objects detected", LogLevel.WARNING, det_type)

    def update_prediction_table(self, predTable):
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

    def display_result_image(self):
        path = (
            self.imageDet.out_dir + "/vis/" + self.list_filenames.currentItem().text()
        )
        logger.log("displaying result image at " + path, LogLevel.DEBUG)
        self.update_result_image(path)
        self.tabWidget.setCurrentIndex(4)

    def open_image_dialog(self):
        Imagedialog = classes.ImageLarge(self)
        Imagedialog.setImage(self)
        Imagedialog.exec()

    def changeTo_usrModelMode(self, det_type):
        combo_config = self.get_combo_usrConfig(det_type)
        combo_checkpoint = self.get_combo_usrCheckpoint(det_type)
        combo_collection = self.get_combo_collection(det_type)
        combo_model = self.get_combo_model(det_type)
        det_object = self.get_det_object(det_type)
        try:
            if det_object is not None and not det_object.usrModelMode:
                det_object.usrModelMode = True
                combo_collection.setStyleSheet(STYLESHEET_DISABLED)
                combo_model.setStyleSheet(STYLESHEET_DISABLED)
                combo_config.setStyleSheet(STYLESHEET_ENABLED)
                combo_checkpoint.setStyleSheet(STYLESHEET_ENABLED)

                self.usrConfig_changed(det_type)
                self.usrWeights_changed(det_type)
                logger.log("Swapped to User Model Mode", LogLevel.INFO, det_type)
        except Exception as e:
            logger.log(
                f"Something went wrong while swapping to UserModelMode:\n{e}",
                LogLevel.WARNING,
                det_type,
            )

    def changeTo_MMDetModelMode(self, det_type):
        combo_config = self.get_combo_usrConfig(det_type)
        combo_checkpoint = self.get_combo_usrCheckpoint(det_type)
        combo_collection = self.get_combo_collection(det_type)
        combo_model = self.get_combo_model(det_type)
        det_object = self.get_det_object(det_type)
        try:
            if det_object is not None and det_object.usrModelMode:
                det_object.usrModelMode = False
                combo_config.setStyleSheet(STYLESHEET_DISABLED)
                combo_checkpoint.setStyleSheet(STYLESHEET_DISABLED)
                combo_collection.setStyleSheet(STYLESHEET_ENABLED)
                combo_model.setStyleSheet(STYLESHEET_ENABLED)

                self.model_changed(det_type)
                self.collection_changed(det_type)
                logger.log(
                    f"Swapped to MMDet Model Mode",
                    LogLevel.INFO,
                    det_type,
                )

        except Exception as err:
            logger.log(
                f"Something went wrong while swapping to UserModelMode:\n{err}",
                LogLevel.WARNING,
                det_type,
            )

    # Webcam Detection
    def start_webcam_det(self):
        try:
            self.webcamDet.run(self)
        except Exception as err:
            logger.log(f"{err}", LogLevel.ERROR, det_type=DetType.WEBCAMDET)

    def stop_webcam_det(self):
        self.webcamDet.stop_WebcamDetEvent.set()

    # WebcamDetection
    @pyqtSlot(np.ndarray)
    def update_image_det(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.lb_webcamDet_2.setPixmap(qt_img)

    def get_det_object(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.imageDet
        elif det_type == DetType.WEBCAMDET:
            return self.webcamDet
        elif det_type == DetType.VIDEODET:
            return self.videoDet

    def get_combo_collection(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.combo_collection
        elif det_type == DetType.WEBCAMDET:
            return self.combo_collection_2
        elif det_type == DetType.VIDEODET:
            return self.combo_collection_3

    def get_combo_model(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.combo_model
        elif det_type == DetType.WEBCAMDET:
            return self.combo_model_2
        elif det_type == DetType.VIDEODET:
            return self.combo_model_3

    def get_combo_usrConfig(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.combo_usrConfig
        elif det_type == DetType.WEBCAMDET:
            return self.combo_usrConfig_2
        elif det_type == DetType.VIDEODET:
            return self.combo_usrConfig_3

    def get_combo_usrCheckpoint(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.combo_usrWeights
        elif det_type == DetType.WEBCAMDET:
            return self.combo_usrWeights_2
        elif det_type == DetType.VIDEODET:
            return self.combo_usrWeights_3

    def get_tb_coll_info(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.tb_collInfo
        elif det_type == DetType.WEBCAMDET:
            return self.tb_collInfo_2
        elif det_type == DetType.VIDEODET:
            return self.tb_collInfo_3

    def get_combo_device(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.combo_chooseDevice
        elif det_type == DetType.WEBCAMDET:
            return self.combo_chooseDevice_2
        elif det_type == DetType.VIDEODET:
            return self.combo_chooseDevice_3

    def get_tb_model_info(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.tb_modelInfo
        elif det_type == DetType.WEBCAMDET:
            return self.tb_modelInfo_2
        elif det_type == DetType.VIDEODET:
            return self.tb_modelInfo_3

    def get_combo_api(self, det_type):
        if det_type == DetType.IMAGEDET:
            return self.combo_api
        elif det_type == DetType.WEBCAMDET:
            return self.combo_api_2
        elif det_type == DetType.VIDEODET:
            return self.combo_api_3
