#class for processing Images with different models and different libraries

#for openmmlab:
import sys
import os

import numpy as np
scriptpath = "C:\cust\Studium_local\Studienprojekt\OpenMMLab\mmdetection"
sys.path.append(os.path.abspath(scriptpath))
from mmdet.apis import (inference_detector,
                        init_detector, DetInferencer)

from mmdet.evaluation import get_classes

#for yolov4 with tensorflow: 
import tensorflow as tf
from tf2_yolov4.anchors import YOLOV4_ANCHORS
from tf2_yolov4.model import YOLOv4
import matplotlib.pyplot as plt

from ModelHandler import Model

class ImageDet(): 

    def __init__(self, parent=None):
        #defs for the model
        self.imagepath=""
        self.model= Model("YOLOV3", "./../OpenMMLab/mmdetection/yolov3_mobilenetv2_320_300e_coco.py", "./../OpenMMLab/mmdetection/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth" )
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
        if(self.api is not None and self.model.name is not ""):
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
        classes = get_classes("coco")

        predtable = list()
        
        i = 0
        for s in scores: 
            if(s > 0.3): 
                pred = {
                    "labelno": labels[i],
                    "score": s,
                    "labelclass": classes[labels[i]]
                }
                predtable.append(pred)
            i+= 1
        print(predtable)
        return predtable
    



    def processImage_tf_Yolov4(self, image_path):
        WIDTH, HEIGHT = (1024, 768)
        
        image = tf.io.read_file(image_path)
        image = tf.io.decode_image(image)
        image = tf.image.resize(image, (HEIGHT, WIDTH))
        images = tf.expand_dims(image, axis=0) / 255
        
        model = YOLOv4(
            input_shape=(HEIGHT, WIDTH, 3),
            anchors=YOLOV4_ANCHORS,
            num_classes=80,
            training=False,
            yolo_max_boxes=50,
            yolo_iou_threshold=0.5,
            yolo_score_threshold=0.5,
        )
        
        model.load_weights('./../Object_Detection/yolov4.h5')
        
        boxes, scores, classes, detections = model.predict(images)

        imgname = os.path.basename(image_path)
        
        boxes = boxes[0] * [WIDTH, HEIGHT, WIDTH, HEIGHT]
        scores = scores[0]
        classes = classes[0].astype(int)
        detections = detections[0]
        
        CLASSES = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
            'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
            'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
            'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
            'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
            'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
            'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
            'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant',
            'bed', 'dining table', 'toilet', 'tv', 'laptop',  'mouse', 'remote', 'keyboard',
            'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
            'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]
        
        plt.imshow(images[0])
        
        ax = plt.gca()
        
        for (xmin, ymin, xmax, ymax), score, class_idx in zip(boxes, scores, classes):
            if score > 0:
                rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                    fill=False, color='green')
                ax.add_patch(rect)
        
                text = CLASSES[class_idx] + ': {0:.2f}'.format(score)
                ax.text(xmin, ymin, text, fontsize=9, bbox=dict(facecolor='yellow', alpha=0.6))
        
        predtable = list()
        
        i = 0
        for s in scores: 
            if(s > 0.3): 
                pred = {
                    "labelno": detections[i],
                    "score": s,
                    "labelclass": classes[detections[i]]
                }
                predtable.append(pred)
            i+= 1
        print(predtable)

        plt.axis('off')
        plt.savefig("./../images/results/vis/"+imgname)
        plt.close()
        return predtable





