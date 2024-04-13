# Steps to reproduce Anaconda Env
## Create empty Anaconda Env with python 3.8: 
`conda create --prefix ./env python=3.8`

## Setup Pytorch and Cuda properly: 
https://medium.com/@harunijaz/a-step-by-step-guide-to-installing-cuda-with-pytorch-in-conda-on-windows-verifying-via-console-9ba4cd5ccbef 

install pytorch 2.0.1 and cuda 11.8 on Windows: 
```
conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.8 -c pytorch -c nvidia
```

install pytorch 2.0.1 and cuda 11.8 on OSX: 
```
conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 -c pytorch
```

install pytorch 2.0.1 without cuda available on Windows: 
``` 
conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 cpuonly -c pytorch 
```

## Install additional packages: 
```
pip install -U openmim
mim install mmcv==2.0.0

pip install pyqt5-tools
pip install py-cpuinfo
pip install tensorflow
pip install mediapipe
```

## Export environment
Export full spec file: 
`conda env export > ./setup/env.yml`

Export from history (cross-platform compatible):
`conda env export --from-history > ./setup/env.yml`



