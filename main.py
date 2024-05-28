from djitellopy import Tello
import cv2
import pygame
from pygame.locals import *
import numpy as np
import time
import os
import json
from utils.utils import get_yolo_boxes
from utils.bbox import draw_boxes
from keras.models import load_model
import logging
import threading
import queue
from agents.rl_drone import RLAgent
from agents.drone_sim_env import drone_sim

LOG_FILENAME = 'output.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)



# Speed of the drone
S = 60
# Frames per second of the pygame window display
FPS = 25

#setting config path for YOLO config
config_path = './zoo/config_voc.json'
with open(config_path) as config_buffer:
    config = json.load(config_buffer)


###############################
#   Set some parameter
###############################
net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
obj_thresh, nms_thresh = 0.90, 0.75

# Create queue for thread to find box in frame
box_q = queue.Queue()
frame_q = queue.Queue()
global frame_glob
frame_glob = []
box_glob = []




def box_thread():
    """box detection thread function. This function receives a frame every 200ms and return corresponding box and actions in a queue
    input : frame_glob (416x416)
    output : put box and actions in queue.
    """
    global frame_glob
    frame_glob = []
    ###############################
    #   Load the model for YOLO detection
    ###############################
    #os.environ['CUDA_VISIBLE_DEVICES'] = config['train']['gpus']
    infer_model = load_model(config['train']['saved_weights_name'])

    ###############################
    #   Load the model for RL agent
    ###############################
    ENV_NAME = 'drone'
    env = drone_sim()
    agent = RLAgent(env)
    agent.agent.load_weights('ddpg_{}_weights.h5f'.format(ENV_NAME))
    agent.agent.test(env, nb_episodes=1, visualize=False, verbose=1, nb_max_episode_steps=10, start_step_policy=1)
    logging.debug('x,y,area_p,Ax,Ay')

    while True:
        try:
            #print('thread size: ' + str(len(frame_glob)))
            # call prection function of YOLO algorithm to return boxes
            boxes = \
                get_yolo_boxes(infer_model, [frame_glob],
                               net_h, net_w, config['model']['anchors'], obj_thresh, nms_thresh)[0]
            frame_glob = []
            #print('ok')
            if len(boxes) > 0:          # only if a least one box is detected
                filter_boxes = []
                actions_f = []
                for box in boxes:
                    if box.get_label() == 0:  # filter on the person class (ID =14)
                        #print("beni buldu")
                        #calculate area of bounding box
                        area = (box.xmax - box.xmin) * (box.ymax - box.ymin) 
                        area_p = (area / 691200.) * 100.0
                        
                        #calculate center of bounding box
                        box_x = int((box.xmax - box.xmin) / 2) + box.xmin   
                        box_y = int((box.ymax - box.ymin) / 2) + box.ymin
                        
                        #pass x,y coordinate to DDPG to get actions
                        actions = agent.agent.forward([box_x, box_y])
                        
                        #log debug info
                        logging.debug('%d,%d,%d,%d,%d' % (box_x, box_y, area_p, actions[0], actions[1]))
                        
                        actions_f.append(actions)
                        filter_boxes.append(box)
                #send box, action in queue
                box_q.put(([filter_boxes[0]], [actions_f[0]]))
                print('thread : box, cmd sent')
        except Exception as e:
            pass

# start thread
thread_box = threading.Thread(target=box_thread, args=())
thread_box.setDaemon(True)
thread_box.start()


def get_dist(x, y):
    
    dist = np.sqrt((np.square(np.array([x, y]) - np.array([480, 360]))).sum())
    return dist

class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations
            - W and S: Up and down.
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 60

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(USEREVENT + 1, 50)
        pygame.time.set_timer(USEREVENT + 2, 250)

        # Run thread to find box in frame
        print('init done')



    def run(self):

        global frame_glob
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 25.0, (960, 720))
        self.tello.connect()
        self.tello.streamon()
      

        frame_read = self.tello.get_frame_read()

        should_stop = False

        print('loop started')

        last_yaw=0
        box_cnt = 0
        frame_glob = []
        frame = []

        while not should_stop:
            frame = frame_read.frame
            for event in pygame.event.get():
                if event.type == USEREVENT + 1:
                    self.update()
                if event.type == USEREVENT + 2:
                    frame_glob = frame
                elif event.type == QUIT:
                    should_stop = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == KEYUP:
                    self.keyup(event.key)
            if frame_read.stopped:
                frame_read.stop()
                break

            self.screen.fill([0, 0, 0])


            box_list = []
            try:
                box_list, actions_list = box_q.get_nowait()
                box = box_list[0]
                actions = actions_list[0]
            except Exception:
                pass
            box_x = 0
            box_y = 0

            if len(box_list) > 0:
                box_cnt = 0
                area = (box.xmax - box.xmin) * (box.ymax - box.ymin)
                area_p = (area / 691200.) * 100.0
                box_x = int((box.xmax - box.xmin) / 2) + box.xmin
                box_y = int((box.ymax - box.ymin) / 2) + box.ymin
                draw_boxes(frame, box_list, config['model']['labels'], obj_thresh)
                done = bool(get_dist(box_x, box_y) < 100 and (15 < area_p < 50))

                #If not done keep setting speeds
                if not done:
                    self.yaw_velocity = -int(actions[0])
                    last_yaw = self.yaw_velocity
                    self.up_down_velocity = int(actions[1])
                    if area_p < 25:
                        self.for_back_velocity = 200
                    elif area_p > 50:
                        self.for_back_velocity = -200
                    else:
                        self.for_back_velocity = 0
                    frame = cv2.circle(frame, (box_x, box_y), 5, (255, 0, 0), -1)
                else:
                    self.yaw_velocity = 0
                    self.up_down_velocity = 0
                    self.for_back_velocity = 0

            #if no box is detected set the last yaw command so the drone goes into search.
            else:
                box_cnt += 1
                if box_cnt > 70:
                    self.yaw_velocity = 40
                else:
                    self.yaw_velocity = 0
                    self.up_down_velocity = 0
                    self.for_back_velocity = 0

            frame = cv2.circle(frame, (480, 360), 5,(0, 0, 255),-1)
            out.write(frame)
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. I deallocate resources.
        self.tello.end()
        out.release()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw counter clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)

    def reset_speed(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(0, 0, 0, 0)


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
