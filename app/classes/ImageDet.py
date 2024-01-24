#class for processing Images with different models

import os
import sys

scriptpath = "C:\cust\Studium_local\Studienprojekt\OpenMMLab\mmdetection"
sys.path.append(os.path.abspath(scriptpath))

from mmdet.apis import DetInferencer
from mmdet.evaluation import get_classes

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
        self.batch_size = 1
        self.out_dir = paths.IMAGES_RES
        self.api = "OpenMMLab"
        self.usrModelMode = True

    def changemodelconfig(self,model): 
        self.model = model

    def processImage(self,image_path): 
        if(self.api != None and self.model.name != ""):
            if(self.api == "OpenMMLab"): 
                return self.processImage_OpenMMLab(image_path)
        else:
            return None
    
    def processImage_OpenMMLab(self,image_path):
        # build the model from a config file and a checkpoint file
        inferencer = None
        if(not self.usrModelMode): 
            inferencer = DetInferencer(model=self.model.name, device=self.device)
        else: 
            inferencer = DetInferencer(model=self.model.config, weights = self.model.weights, device=self.device)
        
        try: 
            resultdict = inferencer(out_dir=self.out_dir, 
                            inputs=image_path, 
                            pred_score_thr=self.score_thr, 
                            batch_size=self.batch_size,
                            no_save_pred = False)
        except Exception as e: 
            return(-1, e)
        else: 
            predTable = self.getPredTable(resultdict)
            return (1, predTable)
        
    
    def getPredTable(self, results): 
        #bbox_result = results["predictions"][0]["bboxes"]
        #print(results)
        labels = results["predictions"][0]["labels"]
        scores = results["predictions"][0]["scores"]
        classes = get_classes("coco")

        predtable = list()
        
        i = 0
        for s in scores: 
            if(s > self.score_thr): 
                pred = {
                    "labelno": labels[i],
                    "score": s,
                    "labelclass": classes[labels[i]]
                }
                predtable.append(pred)
            i+= 1
        return predtable
