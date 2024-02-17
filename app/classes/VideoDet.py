#class for processing Images with different models

from mmdet.apis import DetInferencer
from app.classes.ObjectDet import ObjectDet


class VideoDet(ObjectDet):
    def __init__(self):
        super().__init__() 

    def process(self,image_path): 
        if(self.api != None and self.model.name != ""):
            if(self.api == "OpenMMLab"): 
                return self.processImage_OpenMMLab(image_path)
        else:
            return (-1, "Wrong API")
    
    def processVideo_OpenMMLab(self,image_path):
        # build the model from a config file and a checkpoint file
        inferencer = None
        try: 
            if(not self.usrModelMode): 
                inferencer = DetInferencer(model=self.model.name, device=self.device)
            else: 
                inferencer = DetInferencer(model=self.model.config, weights = self.model.checkpoint, device=self.device)
        except Exception as e: 
            return(-1,e)   
        else: 
            try: 
                resultdict = inferencer(out_dir=self.out_dir, 
                                inputs=image_path, 
                                pred_score_thr=self.score_thr, 
                                batch_size=self.batch_size,
                                no_save_pred = False)
            except Exception as e: 
                return(-1, e)
            else: 
                predictions = resultdict["predictions"][0]
                predTable = self.getPredTable(predictions)
                return (1, predTable)
    

