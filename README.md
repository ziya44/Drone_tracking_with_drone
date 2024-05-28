# Drone_tracking_with_drone
 
<<<<<<< HEAD
Requirements and Installation
The repo was written using Python 3.8 with conda on Ubuntu 20.04

On Ubuntu Major dependencies are gym, pybullet, stable-baselines3, and rllib -->

The repo is structured as a Gym Environment and can be installed with pip install 

$ conda create -n drone python=3.8
$ conda activate drone
$ pip3 install --upgrade pip
$ git clone https://github.com/ziya44/take_off_drone.git
$ cd take_off_drone/
Video recording requires to have ffmpeg installed, On Ubuntu

$ sudo apt install ffmpeg

please install the following packages
python = "^3.8"
numpy = "^1.22"
Pillow = "^9.0"
matplotlib = "^3.5"
cycler = "^0.10"
gym = "^0.21"
pybullet = "^3.2"
torch = "1.11.0"
"ray[rllib]" = "1.9"
stable-baselines3 = "1.5.0"
scipy = "^1.8"
tensorboard = "^2.9"
learn.py is an RL example to take-off using stable-baselines3's A2C or rllib's PPO

$ cd take_off_drone/drones/examples/
$ python3 learn.py  
=======
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
