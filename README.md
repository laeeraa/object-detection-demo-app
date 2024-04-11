# PyQT Desktop-App for Object Detection using OpenMMLab

This Desktop-App can be used to test and evaluate different neuronal networks with the purpose for object detection on images and videos.
# Start Commands
Start App: 
`python .\app\app.py`

Start pyqt5 Designer:
`pyqt5-tools designer`

Convert newest Qt-Main-Window-File to python:
`pyuic5 -o main_window_ui.py .\Main_Window.ui`
  
Freeze anaconda environment:
`conda env export --no-builds > ./setup/env_linux.yml`

# Some Demo Pictures: 

![alt text](documentation/runtime-pictures/ImageDetection-1.png)
![alt text](documentation/runtime-pictures/ImageDetection-FileDialog.png)
![alt text](documentation/runtime-pictures/results-2.png)
![alt text](documentation/runtime-pictures/WebcamDetection-2.png)
![alt text](documentation/runtime-pictures/WebcamDetection-TechVidvan.png)

# Setting up
## 1. Install Miniconda3
#### On Linux: 
```
mkdir -p ~/miniconda3

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh

bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

rm -rf ~/miniconda3/miniconda.sh
````
init the command line
```
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```
#### On MacOS 
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
```
#### On Windows

```bash
#download SetUP:
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe

#Run Setup
#don't forget to add miniconda to the Path-Variable when asked
start .\miniconda.exe

#delete setup again
del miniconda.exe

#initialize anaconda in Command Line (restart of cmd required before conda command is available) 
conda init
```
## 2. Setup Environment
```
conda env create -f ./setup/env_windows.yml --prefix ./env
conda activate ./env
```
### 3. Setup CUDA 
ONLY if a NVIDIA GPU is available   
follow Tutorial on: https://medium.com/@harunijaz/a-step-by-step-guide-to-installing-cuda-with-pytorch-in-conda-on-windows-verifying-via-console-9ba4cd5ccbef and install for the recently created environment


### 3. Setup Packages
### On Linux: 
```
unzip -d ./app/packages/OpenMMLab ./setup/packages/mmdetection.zip
cd ./app/packages/OpenMMLab/mmdetection-main

unzip -d ./app/packages/ ./setup/packages/Hand_Gesture_Recognizer.zip
```
### On Windows: 
```
Expand-Archive ./setup/packages/Hand_Gesture_Recognizer.zip -DestinationPath ./app/packages/
Expand-Archive ./setup/packages/mmdetection.zip -DestinationPath ./app/packages/OpenMMLab
mim install "mmcv==2.0.0"
```
### Continue for all platforms: 
```bash

cd ./app/packages/OpenMMLab/mmdetection-main
pip install -v -e .

#Verify Installation of mmdetection if no cuda available
python demo/image_demo.py demo/demo.jpg rtmdet-ins-s --show --device cpu

#Verifying Installation of mmdetection with cuda enabled:
python demo/image_demo.py demo/demo.jpg rtmdet-ins-s --show
```

If everything worked fine you can now go back to your root-directory 
`cd ../../../..` and

### start the app 
`python app/app.py`


