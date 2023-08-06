import os; 

workingdir = os.getcwd()

MMDET_MODELS = workingdir +"/app/packages/OpenMMLab/mmdetection/configs"
USER_MODELS = workingdir + "/data/models"

IMAGES = workingdir + "/data/images/"
IMAGES_RES = IMAGES +"results"
