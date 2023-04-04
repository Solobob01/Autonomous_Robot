from __future__ import print_function
from __future__ import division
from camera import setUpCamera

import motor
import image_processing
import time
import threading
import gopigo3
import numpy as np
import cv2

BIGGEST_BOTTLE_POSITION = (-1, -1, -1, -1)

def cameraFunction(camera, raw_capture):
    global BIGGEST_BOTTLE_POSITION
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        image = cv2.rotate(image, cv2.ROTATE_180)
        BIGGEST_BOTTLE_POSITION = image_processing.processFrame(image)
        #cv2.imshow("Original frame", image)
        key = cv2.waitKey(1) & 0xFF
        raw_capture.truncate(0)
        if key == ord('q'):
            break

def motorControl(GPG):
    global BIGGEST_BOTTLE_POSITION
    time.sleep(0.5)
    while 1:
        if motor.controlAutonomous(GPG, BIGGEST_BOTTLE_POSITION) == 0:
            print("Am iesit!")
            break

        

if __name__ == "__main__":
    GPG = gopigo3.GoPiGo3()
    camera, raw_capture = setUpCamera(size = (640, 480), framerate = 32)
    threads = list()
    x = threading.Thread(target = cameraFunction, args = (camera, raw_capture, ))
    y = threading.Thread(target = motorControl, args = (GPG,))
    threads.append(x)
    threads.append(y)
    for thread in threads:
        thread.start()
    time.sleep(0.1)
    for thread in threads:
        thread.join()
    GPG.reset_all()
