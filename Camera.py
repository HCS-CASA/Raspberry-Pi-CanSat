import picamera
from os import path
from time import sleep

class camera(picamera.PiCamera):
  def __init__(self):
    super(camera, self).__init__()
    self.resolution = (2592, 1944) #2582x1944 = Max Resoloution
    self.brightness = 50 #0 -> 100
    self.contrast = 0 #-100 -> 100
    self.exposure_mode = "auto" #"off", "auto", "night", "nightpreview", "backlight", "spotlight", "sports", "snow", "beach", "verylong", "fixedfps", "antishake", "fireworks"
    self.led = True
    self.meter_mode = "average" #"average", "spot", "backlit", "matrix"
    self.rotation = 0 #0, 90, 180, 270
    self.saturation = 0 #-100 -> 100
    self.sharpness = 0 #-100 -> 100
    self.shutter_speed = 0 #microseconds
    self.hflip = False
    self.vflip = False
    
  def capture(self):
    self.start_preview()
    sleep(2)
    super(camera, self).capture_continuous(path.join(path.realpath(__file__),"img/image{counter:04d}.jpg"))
    self.stop_preview()