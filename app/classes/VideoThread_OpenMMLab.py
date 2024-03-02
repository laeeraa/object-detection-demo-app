import os
import warnings

import cv2
import mmcv
import numpy as np
import torch
from mmdet.apis.det_inferencer import DetInferencer
from mmdet.apis.inference import inference_detector, init_detector
from mmdet.registry import VISUALIZERS
from PyQt5.QtCore import QThread, pyqtSignal

from app.classes.CustomLogger import logger
from app.constants.types import DetType, LogLevel


class VideoDetThread_OpenMMLab(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, parent, stopEvent):
        self.device = parent.device
        self.model = parent.model
        self.score_thr = parent.score_thr
        self.stopEvent = stopEvent
        self.palette = parent.palette
        self.usrModelMode = parent.usrModelMode
        super().__init__()

    def run(self):
        # build the model from a config file and a checkpoint file
        device = torch.device(self.device)
        try:
            if self.usrModelMode:
                inferencer = DetInferencer(
                    model=self.model.config,
                    weights=self.model.checkpoint,
                    palette=self.palette,
                    device=device,
                )
            else:
                inferencer = DetInferencer(
                    model=self.model.name,
                    palette=self.palette,
                    device=device,
                )
            visualizer = inferencer.visualizer
            # the dataset_meta is loaded from the checkpoint and
            # then pass to the model in init_detector
            # visualizer.dataset_meta = model.dataset_meta

            camera = cv2.VideoCapture(0)
        except Exception as e:
            logger.log(e, LogLevel.ERROR, DetType.WEBCAMDET)
            return
        else:
            logger.log("Detector set up successfully", LogLevel.INFO, DetType.WEBCAMDET)
        while True:
            ret_val, img = camera.read()
            try:
                result = inference_detector(inferencer.model, img)
            except Exception as e:
                logger.log(e, LogLevel.ERROR, DetType.WEBCAMDET)
                return
            img = mmcv.imconvert(img, "bgr", "rgb")
            visualizer.add_datasample(
                name="result",
                image=img,
                data_sample=result,
                draw_gt=False,
                pred_score_thr=self.score_thr,
                show=False,
            )

            img = visualizer.get_image()
            img = mmcv.imconvert(img, "bgr", "rgb")

            if ret_val:
                self.change_pixmap_signal.emit(img)

            if self.stopEvent.is_set():
                camera.release()
                cv2.destroyAllWindows()
                break
