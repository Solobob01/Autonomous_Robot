from picamera.array import PiRGBArray
from picamera import PiCamera

def setUpCamera(size, framerate):
    camera = PiCamera()
    camera.resolution = size
    camera.framerate = framerate
    raw_capture = PiRGBArray(camera, size = size)
    return camera, raw_capture