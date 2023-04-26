#class for processing Images with different models and different libraries

#for openmmlab:
import sys
import os
from mmdet.models.detectors.base import BaseDetector
scriptpath = "C:\cust\Studium_local\Studienprojekt\OpenMMLab\mmdetection"
sys.path.append(os.path.abspath(scriptpath))
from mmdet.apis import (async_inference_detector, inference_detector,
                        init_detector)

#for yolov4 with tensorflow: 
import tensorflow as tf
from tf2_yolov4.anchors import YOLOV4_ANCHORS
from tf2_yolov4.model import YOLOv4
import matplotlib.pyplot as plt

class ImageDet(): 

    def __init__(self, parent=None):
        #defs for the model
        self.imagepath=""
        self.model=""
        self.config="./../OpenMMLab/mmdetection/yolov3_mobilenetv2_320_300e_coco.py"
        self.checkpoint="./../OpenMMLab/mmdetection/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth"
        self.device="cpu"
        self.palette="coco"
        self.score_thr=float(0.3)


    def changemodelconfig(self,model): 
        self.model = model
        if(self.model == "Yolov3 with OpenMMLab"): 
            self.config="./../OpenMMLab/mmdetection/yolov3_mobilenetv2_320_300e_coco.py"
            self.checkpoint="./../OpenMMLab/mmdetection/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth"
            self.score_thr=float(0.3)
        elif(self.model == "Faster rcnn r50 with OpenMMLab"): 
            self.config="./../OpenMMLab/mmdetection/configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py"
            self.checkpoint="./../OpenMMLab/mmdetection/checkpoints/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth"
        elif(self.model == "Yolov4 with Tensorflow"): 
            self.config="./"
            self.checkpoint=" "  

    def processImage(self,image_path): 
        if (self.model == "Yolov3 with OpenMMLab" or self.model == "Faster rcnn r50 with OpenMMLab"): 
            return self.processImage_OpenMMLab(image_path)
        elif (self.model == "Yolov4 with Tensorflow"): 
            return self.processImage_tf_Yolov4(image_path)
        else:
            return -1

    def processImage_OpenMMLab(self,image_path):
        out_file="./../images/result.jpg"
            # build the model from a config file and a checkpoint file
        model = init_detector(self.config, self.checkpoint, self.device)
            # test a single image
        result = inference_detector(model,image_path)
            # show the results
        #res = BaseDetector.show_result(img, result, model.CLASSES, score_thr=0.3, wait_time=1)
        #cv.imwrite(result_path, res)
        # show_result_pyplot(
        #         model,
        #         image_path,
        #         result,
        #         self.score_thr,
        #         'result',
        #         0,
        #         self.palette, 
        #         out_file)
        return 1 

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
        
        plt.savefig("./../images/result.jpg")
        plt.close()
        return detections
        #plt.title('Objects detected: {}'.format(detections))
        #plt.axis('off')
        #plt.show()





