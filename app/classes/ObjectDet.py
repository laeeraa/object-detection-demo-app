from mmdet.evaluation import get_classes

from app.classes.Collection import Collection
from app.classes.Model import Model
from app.constants import paths


class ObjectDet:
    def __init__(self):
        # Inference parameters
        self.model = Model(
            name="YOLOV3",
            collection="User",
            metadata=None,
            config=paths.USER_CONFIGS + "rtmdet_tiny_8xb32-300e_coco.py",
            checkpoint=paths.USER_WEIGHTS
            + "rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth",
        )
        self.collection = Collection("USER")
        self.device = "cpu"
        self.palette = "coco"
        self.score_thr = float(0.3)
        self.batch_size = 1
        self.out_dir = paths.IMAGES_RES
        self.api = "OpenMMLab"
        self.usrModelMode = True

    def update_modelConfig(self, model):
        self.model = model

    def process(self):
        pass

    def getPredTable(self, results):
        labels = results["labels"]
        scores = results["scores"]
        classes = get_classes(self.palette)

        predtable = list()

        i = 0
        for s in scores:
            if s > self.score_thr:
                pred = {
                    "labelno": labels[i],
                    "score": s,
                    "labelclass": classes[labels[i]],
                }
                predtable.append(pred)
            i += 1
        return predtable
