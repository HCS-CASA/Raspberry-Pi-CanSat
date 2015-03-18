from time import sleep
#from transmitReceive import TransmitReceive
from Camera import camera
#from gps import GPS
from AccGyro import accGyro
from TempPressureSensor import tempPressure
from sys import argv
import threading

class accGyroThread(threading.Thread):
  def __init__(self):
    self.accGyro = accGyro()
    self.accGyro.createFile()
    self.end = False
    threading.Thread.__init__(self)
    
  def run(self):
    while not self.end:
      self.accGyro.getResults()
      self.accGyro.writeData()
      print 'Acceleration x:', self.accGyro.acc_x, 'Acceleration y:', self.accGyro.acc_y, 'Acceleration z:', self.accGyro.acc_z, 'Temperature:', self.accGyro.temp, 'Gyroscope x:', self.accGyro.gyro_x, 'Gyroscope y:', self.accGyro.gyro_y, 'Gyroscope z:', self.accGyro.gyro_z
      #sleep(1)
      
  def join(self):
    self.end = True
    threading.Thread.join(self)

class tempPressureThread(threading.Thread):
  def __init__(self):
    self.tempPressure = tempPressure()
    self.tempPressure.createFile()
    self.end = False
    threading.Thread.__init__(self)
    
  def run(self):
    while not self.end:
      self.tempPressure.getResults()
      self.tempPressure.writeData()
      print "Temperature:", self.tempPressure.temp, "Pressure:", self.tempPressure.pressure
      #sleep(1)
      
  def join(self):
    self.end = True
    threading.Thread.join(self)
    
class cameraThread(threading.Thread):
  def __init__(self):
    self.end = False
    threading.Thread.__init__(self)
    
  def run(self):
    while not self.end:
      with camera() as self.cam:
        self.cam.capture()
        print "Image Taken"
        
  def join(self):
    self.end = True
    threading.Thread.join(self)

#Wait Time
waitMin = int(argv[1])
waitSec = int(argv[2])
while waitMin >= 0:
  while waitSec >= 0:
    print "T-Minus: %02d:%02d" % (waitMin, waitSec)
    sleep(1)
    waitSec -= 1
  waitSec = 59
  waitMin -= 1
  
myAccGyro = accGyroThread()
myTempPressure = tempPressureThread()
myCamera = cameraThread()

myAccGyro.start()
myTempPressure.start()
myCamera.start()

while True:
  try:
    pass
  except KeyboardInterrupt: 
    myAccGyro.join()
    myTempPressure.join()
    myCamera.join()
