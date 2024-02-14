#class for processing Images with different models
import os
import sys

from mmdet.apis.inference import inference_detector, init_detector
from mmdet.evaluation import get_classes
import torch

from app.classes.Model import Model 
from app.classes.Collection import Collection
from app.constants import paths

class ImageDet(): 

    def __init__(self):
        #defs for the model
        self.imagepath=""
        self.model = Model(name ="YOLOV3", 
                                  collection = "User", 
                                  metadata=None, 
                                  config = paths.USER_CONFIGS+"rtmdet_tiny_8xb32-300e_coco.py", 
                                  weights = paths.USER_WEIGHTS + "rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth")
        self.collection = Collection("USER")
        self.device="cpu"
        self.palette="coco"
        self.score_thr=float(0.3)
        #self.batch_size = 1
        #self.out_dir = paths.IMAGES_RES
        self.api = "OpenMMLab"
        self.usrModelMode = True
        self.camera_id = 0

    
    def run(self): 
        # build the model from a config file and a checkpoint file
        device = torch.device(self.device)
        model = init_detector(self.config, self.checkpoint, self.device)

        # init visualizer
        visualizer = VISUALIZERS.build(model.cfg.visualizer)
        # the dataset_meta is loaded from the checkpoint and
        # then pass to the model in init_detector
        visualizer.dataset_meta = model.dataset_meta

        camera = cv2.VideoCapture(args.camera_id)

        print('Press "Esc", "q" or "Q" to exit.')
        while True:
            ret_val, img = camera.read()
            result = inference_detector(model, img)

            img = mmcv.imconvert(img, 'bgr', 'rgb')
            visualizer.add_datasample(
                name='result',
                image=img,
                data_sample=result,
                draw_gt=False,
                pred_score_thr=args.score_thr,
                show=False)

            img = visualizer.get_image()
            img = mmcv.imconvert(img, 'bgr', 'rgb')
            cv2.imshow('result', img)

            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord('q') or ch == ord('Q'):
                break