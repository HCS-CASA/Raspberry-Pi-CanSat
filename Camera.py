import picamera
from os import os.path
from time import sleep

class camera(picamera.PiCamera):
  def __init__(self):
    super(camera, self).__init__()
    camera.resolution = (2592, 1944) #2582x1944 = Max Resoloution
    camera.brightness = 50 #0 -> 100
	camera.contrast = 0 #-100 -> 100
	camera.exposure_mode = "auto" #"off", "auto", "night", "nightpreview", "backlight", "spotlight", "sports", "snow", "beach", "verylong", "fixedfps", "antishake", "fireworks"
	camera.led = True
	camera.meter_mode = "average" #"average", "spot", "backlit", "matrix"
	camera.rotation = 0 #0, 90, 180, 270
	camera.saturation = 0 #-100 -> 100
	camera.sharpness = 0 #-100 -> 100
	camera.shutter_speed = 0 #microseconds
	camera.hflip = False
	camear.vflip = False
	
  def capture(self):
    camera.start_preview()
    sleep(2)
    super(camera, self).capture_continuous(os.path.join(os.path.realpath(__file__),"img/image{counter:04d}.jpg"))
    camera.stop_preview()