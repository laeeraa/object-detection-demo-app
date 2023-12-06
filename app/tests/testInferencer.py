import sys

from mmdet.evaluation.functional.class_names import get_classes

# add your project directory to the sys.path
project_home = 'C:\cust\Studium_local\Studienprojekt'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
print(sys.path)

from app.classes.Model import Model
from app.constants import paths
from mmdet.apis.det_inferencer import DetInferencer

imagepath=""
model= Model(name ="YOLOV3",                     
                    collection = "User",                     
                    metadata=None       ,              
                    config = paths.USER_CONFIGS+"rtmdet_tiny_8xb32-300e_coco.py",                 
                    weights = paths.USER_WEIGHTS + "rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth" )
device="cpu"
palette="coco"
score_thr=float(0.3)
batch_size = 1
out_dir = paths.IMAGES_RES
api = "OpenMMLab"
usrModelMode = True
image_path = "C:\cust\Studium_local\Studienprojekt\data\images\\20230724_202525.jpg"
model = "mask2former_swin-s-p4-w7-224_8xb2-lsj-50e_coco-panoptic"

def main(): 

    inferencer = DetInferencer(model=model, device=device)
    resultdict = inferencer(out_dir=out_dir, 
                                    inputs=image_path, 
                                    pred_score_thr=score_thr, 
                                    batch_size=batch_size,
                                    #return_datasample = True, 
                                    no_save_pred = False,
                                    #print_result=True
                                    )
    print(resultdict)

def getPredTable(self, results): 
        #bbox_result = results["predictions"][0]["bboxes"]
        print(results)
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
        print(predtable)
        return predtable

if __name__ == '__main__':
    main()