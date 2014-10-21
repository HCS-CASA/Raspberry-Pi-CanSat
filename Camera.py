import picamera, os
from time import sleep

class camera(picamera.PiCamera):
  def __init__(self):
    super(camera, self).__init__()
    self.imgGen = super(camera, self).capture_continuous(os.path.join(os.path.dirname(os.path.realpath(__file__)),"img/image{counter:04d}.jpg"))
    self.resolution = (2592, 1944) #2582x1944 = Max Resoloution
    self.brightness = 50 #0 -> 100
    self.contrast = 0 #-100 -> 100
    self.exposure_mode = "auto" #"off", "auto", "night", "nightpreview", "backlight", "spotlight", "sports", "snow", "beach", "verylong", "fixedfps", "antishake", "fireworks"
    self.led = False
    self.meter_mode = "average" #"average", "spot", "backlit", "matrix"
    self.rotation = 0 #0, 90, 180, 270
    self.saturation = 0 #-100 -> 100
    self.sharpness = 0 #-100 -> 100
    self.shutter_speed = 0 #microseconds
    self.hflip = True
    self.vflip = True
    
  def capture(self):
    if sum(os.path.getsize(file) for file in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),"img")) if os.path.isfile(file)) < 13958643712:
        self.start_preview()
        sleep(2)
        self.imgGen.next()
        self.stop_preview()
