# Drone_tracking_with_drone
 
## Requirements and Installation

The repo was written using Python 3.8 with conda on  Ubuntu 20.04

Dataset:

use your own drone data set.

Inspired from :

Keras YOLO V3 implementation : https://github.com/experiencor/keras-yolo3

Tello Python wrapper : https://github.com/damiafuentes/DJITelloPy

Drone tracking (DDPG) : Keras-rl / rkassana

```bash
$ conda create -n drone python=3.8
$ conda activate drone
$ pip3 install --upgrade pip
$ git clone https://github.com/ziya44/Drone_tracking_with_drone.git


# please install the following packages
```bash
Python 3.X
Keras GPU
Keras-rl
OpenCV
Numpy
CUDA & NVIDA Drivers(optional)
OpenAI Gym
```

## Make sure that the YOLO weight file VOC.h5 that you created with your own dataset is in the root folder.

1- Start main.py

2- Once the video is on, it will take 30 seconds for the YOLO and DDPG to initialize (model creation, loading, etc..).

3- Take off using T

4- Drone should track bounding box in screen.
```


# please install the following packages
```bash
Python 3.X
Keras GPU
Keras-rl
OpenCV
Numpy
CUDA & NVIDA Drivers(optional)
OpenAI Gym
```
