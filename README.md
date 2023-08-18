# Demonstrator for Object Detection using OpenMMLab

# Setting up Anaconda Environment

```bash
#setting up anaconda environment
conda create --name demonstrator_v1 python=3.8 -y
conda activate demonstrator_v1

#install dependencies for mmdetection package
conda install pytorch torchvision cpuonly -c pytorch

#nicht sicher ob man die folgenden beiden wirklich braucht
pip install -U openmim
mim install mmengine

pip install chardet
pip install "mmcv-full==1.6.0"

mkdir OpenMMLab
cd OpenMMLab

#für neustes mmdetection-Repo 
git clone https://github.com/open-mmlab/mmdetection.git
#für einheitliches mmdetection Repo zip datei aus ./packages verwenden und nach ./OpenMMLab entpacken:
Expand-Archive ./packages/mmdetection-main.zip -DestinationPath ./OpenMMLab

cd mmdetection
pip install -v -e .

#Verify Installation of mmdetection: 
mim download mmdet --config rtmdet_tiny_8xb32-300e_coco --dest .
python demo/image_demo.py demo/demo.jpg rtmdet_tiny_8xb32-300e_coco.py --weights rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth --device cpu

#für Handgesture Recognizer
pip install mediapipe 

#für YoloV4
pip install tensorflow
pip install tf2-yolov4

#QT5
pip install pyqt5-tools 

#Python Build tool 
pip install build 
```

### StartBefehle

```bash
#start pyqt5 designer
pyqt5-tools designer

#start app: 
python .UI\app.py

#convert newest qt-file to python: 
pyuic5 -o main_window_ui.py .\Main_Window.ui

#build project: 
python -m build --wheel
```


# Anaconda Environment aufbauen 
 
```
conda env create -f ./setup/environment.yml --prefix ./env 
conda activate ./env
```
