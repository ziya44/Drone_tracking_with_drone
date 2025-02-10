# Drone_tracking_with_drone
 ## Project Overview 
In this project, a drone that can track a drone based on what it sees is realized. Using its camera, the drone can detect a drone and move according to its position. Apart from the camera itself, no other sensors are used.
To perform such an action, the drone must be able to perform two functions simultaneously: drone detection and drone tracking (motion control). 
If we look at these two problems and their solutions:
Object detection: The drone is equipped with a 720p camera. Using an artificial neural network, notably a convolutional network, we can detect the presence of an object in an image. With an architecture like YOLO, we even have extra information that tells us where this object is in the picture. It is essential to understand that to know where the drone should go, the computer must have a way to calculate its position relative to the object of interest. 
Motion control: Once we know where the object is in the picture, we need to tell the drone to move to center that object in its camera. We can command the drone to go clockwise, counterclockwise, up, down, forward, or backward.

## Data Exploration and Visualization 
This section will be divided into two subsections: object detection data and motion control. 
Object detection - Drone dataset (created by me) 
The dataset contains an object class and consists of approximately 6500 different drone images:
Each record consists of an image and an XML file containing information about that image. 
Each XML file refers to a single image. An XML file will list all classes in the image and indicate the coordinates of the drone's bounding box.

## Motion Control - Environment 

The image frame from the drone has a resolution of 960x720 pixels. The center of the frame is always x=480, y=360. 

Depending on where the drone is located in the image, we can calculate the center of the bounding box located by the model. 

Using the difference between the screen's center and the bounding box's center, we get a relative position that we can use to train a reinforcement learning agent (DDPG). Please note that x and y only track the direction and height of the drone relative to the target. The distance (z) between the objects cannot be found using x and y. 
We use the area of the bounding box to measure the distance. The area of the box will grow as the object gets closer and vice versa. The reinforcement learning agent is trained to give only x and y commands. The distance (z) component is controlled separately for this project with a simple if condition.
 
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
