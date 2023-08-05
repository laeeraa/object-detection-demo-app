#class for processing Images with different models and different libraries

#for openmmlab:
import os
import sys
#from packages.OpenMMLab.mmdetection.mmdet.evaluation.functional.class_names import get_classes

scriptpath = "C:\cust\Studium_local\Studienprojekt\OpenMMLab\mmdetection"
sys.path.append(os.path.abspath(scriptpath))

from mmdet.apis import (inference_detector,
                        init_detector, DetInferencer)

from mmdet.evaluation import get_classes

#from packages.OpenMMLab.mmdetection.mmdet.apis import DetInferencer

#from packages.OpenMMLab.mmdetection.mmdet.evaluation import get_classes

#for yolov4 with tensorflow: 
import tensorflow as tf
from tf2_yolov4.anchors import YOLOV4_ANCHORS
from tf2_yolov4.model import YOLOv4
import matplotlib.pyplot as plt

import classes

class ImageDet(): 

    def __init__(self, parent=None):
        #defs for the model
        self.imagepath=""
        self.model= classes.Model("YOLOV3", "./../OpenMMLab/mmdetection/yolov3_mobilenetv2_320_300e_coco.py", "./../OpenMMLab/mmdetection/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth" )
        self.device="cpu"
        self.palette="coco"
        self.score_thr=float(0.3)
        self.api = "OpenMMLab"


    def changemodelconfig(self,model): 
        self.model = model
        if(self.model.name == "YOLOV3"): 
            self.score_thr=float(0.3)
        elif(self.model.name == "Yolov4 with Tensorflow"): 
            self.model.config="./"
            self.model.checkpoint=" "  

    def processImage(self,image_path): 
        if(self.api != None and self.model.name != ""):
            if(self.api == "OpenMMLab"): 
                return self.processImage_OpenMMLab(image_path)
            elif (self.api == "Tensorflow"): 
                return self.processImage_tf_Yolov4(image_path)
        else:
            return None

    def processImage_OpenMMLab(self,image_path):
        outFile="./../images/results/"
        #print("Configpath", self.model.configPath)
        #print("Weightspath", self.model.weightPath)

        # build the model from a config file and a checkpoint file
        inferencer = DetInferencer(model=self.model.name, device=self.device)
        resultdict = inferencer(out_dir=outFile, inputs=image_path)

        predTable = self.getPredTable(resultdict)

        return predTable
    
    def getPredTable(self, results): 
        bbox_result = results["predictions"][0]["bboxes"]
        labels = results["predictions"][0]["labels"]
        scores = results["predictions"][0]["scores"]
        #classes = get_classes("coco")

        predtable = list()
        
        i = 0
        for s in scores: 
            if(s > 0.3): 
                pred = {
                    "labelno": labels[i],
                    "score": s,
                    #"labelclass": classes[labels[i]]
                }
                predtable.append(pred)
            i+= 1
        print(predtable)
        return predtable




