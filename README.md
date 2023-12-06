# PyQT Desktop-App for Object Detection using OpenMMLab
This Desktop-App can be used to test and evaluate different neuronal networks with the purpose for object detection on images and videos. 

## Setting up
### Setup Anaconda Environment
```bash
sudo choco install miniconda3 --params="'/AddToPath:1'"

#initialize anaconda
conda init

#setting up anaconda environment
conda env create -f ./setup/environment.yml --prefix ./env 
conda activate ./env

```
### Setup OpenMMLab
```bash
#Setup OpenMMLab
Expand-Archive ./packages/mmdetection-main.zip -DestinationPath ./OpenMMLab

cd mmdetection
pip install -v -e .

#Verify Installation of mmdetection: 
mim download mmdet --config rtmdet_tiny_8xb32-300e_coco --dest .
python demo/image_demo.py demo/demo.jpg rtmdet_tiny_8xb32-300e_coco.py --weights rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth --device cpu

```


## StartBefehle

```bash
#start app: 
python .\app\app.py
#start pyqt5 designer
pyqt5-tools designer

#convert newest qt-file to python: 
pyuic5 -o main_window_ui.py .\Main_Window.ui

#build project: 
python -m build --wheel

#create class-diagram with pyreverse
pyreverse -o png ./app/

```
## Some Examples 
![Alt text](./documentation/image-1.png)
![Alt text](./documentation/image.png)



# Anaconda Environment aufbauen 
 
```bash
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
