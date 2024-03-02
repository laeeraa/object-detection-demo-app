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

    def __init__(self, parent, stopEvent, camera_id, stopCallback):
        self.device = parent.device
        self.model = parent.model
        self.score_thr = parent.score_thr
        self.stopEvent = stopEvent
        self.palette = parent.palette
        self.usrModelMode = parent.usrModelMode
        self.camera_id = camera_id
        super().__init__()
        self.stopCallback = stopCallback

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

            camera = cv2.VideoCapture(self.camera_id)
        except Exception as e:
            logger.log(e, LogLevel.ERROR, DetType.WEBCAMDET)
            return
        else:
            logger.log("Detector set up successfully", LogLevel.INFO, DetType.WEBCAMDET)
        while True:
            ret_val, frame = camera.read()

            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            try:
                result = inference_detector(inferencer.model, frame)
            except Exception as e:
                logger.log(e, LogLevel.ERROR, DetType.WEBCAMDET)
                return
            # frame = mmcv.imconvert(frame, "bgr", "rgb")
            visualizer.add_datasample(
                name="result",
                image=framergb,
                data_sample=result,
                draw_gt=False,
                pred_score_thr=self.score_thr,
                show=False,
            )

            frame = visualizer.get_image()
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if ret_val:
                self.change_pixmap_signal.emit(framergb)

            if self.stopEvent.is_set():
                camera.release()
                cv2.destroyAllWindows()
                self.stopCallback()
                break
