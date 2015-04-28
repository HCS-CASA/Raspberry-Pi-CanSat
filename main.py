from time import sleep
from Camera import camera
from gps import GPS
from AccGyro import accGyro
from TempPressureSensor import tempPressure
from Magnetometer import Magnetometer
from sys import argv
from json import load
from os.path import isfile
import threading

fileName = "config.json" if isfile("config.json") else "config-base.json"
with open(fileName) as configFile:
  config = load(configFile)

class sensorsClass():
  def __init__(self):
    self.sensors = []
    
  def addSensor(self, instance):
    self.sensors.append(instance)
    
  def startSensors(self):
    for sensor in self.sensors():
      sensor.start()
    
  def joinSensors(self)
    for sensor in self.sensors():
      sensor.join()

class sensorThread(threading.Thread):
  def __init__(self, **kwargs):
    self.end = False
    self.delay = 0
    for key, value in **kwargs:
      self.__dict__[key] = value
    threading.Thread.__init__(self)
    
  def run(self):
    while not self.end:
      self.runSensor()
      self.printSensor()
      sleep(self.delay)
    
  def join(self):
    self.end = True
    threading.Thread.join(self)
    
class gpsThread(sensorThread):
  def __init__(self, **kwargs):
    self.gps = GPS()
    self.fileName = None
    self.gps.createFile(filename=self.fileName)
    sensorThread.__init__(self, **kwargs)
    
  def runSensor(self):
    self.gps.startRead()
    self.gps.writeData()
    
  def printSensor(self):
    if config["print"]: print 'Latitude:', self.gps.lat, 'Longitude:', self.gps.lng, 'Altitude:', self.gps.alt, 'Date:', self.gps.date, 'Time:', self.gps.time
    
  def join(self):
    self.gps.stopRead()
    sensorThread.join(self)

class accGyroThread(sensorThread):
  def __init__(self, **kwargs):
    self.accGyro = accGyro()
    self.fileName = None
    self.accGyro.createFile(filename=self.fileName)
    sensorThread.__init__(self, **kwargs)
    
  def runSensor(self):
    self.accGyro.getResults()
    self.accGyro.writeData()
    
  def printSensor(self):
    if config["print"]: print 'Acceleration x:', self.accGyro.acc_x, 'Acceleration y:', self.accGyro.acc_y, 'Acceleration z:', self.accGyro.acc_z, 'Temperature:', self.accGyro.temp, 'Gyroscope x:', self.accGyro.gyro_x, 'Gyroscope y:', self.accGyro.gyro_y, 'Gyroscope z:', self.accGyro.gyro_z
    
class tempPressureThread(sensorThread):
  def __init__(self, **kwargs):
    self.tempPressure = tempPressure()
    self.fileName = None
    self.tempPressure.createFile(filename=self.fileName)
    sensorThread.__init__(self, **kwargs)
    
  def runSensor(self):
    self.tempPressure.getResults()
    self.tempPressure.writeData()
    
  def printSensor(self):
    if config["print"]: print "Temperature:", self.tempPressure.temp, "Pressure:", self.tempPressure.pressure
    
class cameraThread(sensorThread):
  def __init__(self, **kwargs):
     self.captureTime = 2
     sensorThread.__init__(self, **kwargs)
     
  def runSensor(self):
    with camera() as self.cam:
      self.cam.capture(self.captureTime)
      if config["print"]: print "Image Taken"
      
class magnetometerThread(sensorThread):
  def __init__(self, **kwargs):
    self.magnet = Magnetometer()
    self.fileName = None
    self.magnet.createFile(filename=self.fileName)
    sensorThread.__init__(self, **kwargs)
    
  def runSensor(self):
    self.magnet.getResults()
    self.magnet.writeData()
  
  def printSensor(self):
    if config["print"]: print 'Mag X:', self.magnet.mag_x, 'Mag Y:', self.magnet.mag_y, 'Mag Z', self.magnet.mag_z

#Wait Time
waitMin = int(argv[1] if len(argv) > 1 else 0)
waitSec = int(argv[2] if len(argv) > 2 else 0)
while waitMin >= 0:
  while waitSec >= 0:
    if config["print"]: print "T-Minus: %02d:%02d" % (waitMin, waitSec)
    sleep(1)
    waitSec -= 1
  waitSec = 59
  waitMin -= 1

sensorList = []
if config["magnetometer"]["active"]: sensorList.append(magnetometerThread(
  fileName=config["magnetometer"]["dataFileName"],
  delay=config["magnetometer"]["minTimePeriod"],
))
if config["pressureTemp"]["active"]: sensorList.append(tempPressureThread(
  fileName=config["pressureTemp"]["dataFileName"],
  delay=config["pressureTemp"]["minTimePeriod"],
))
if config["gps"]["active"]: sensorList.append(gpsThread(
  fileName=config["gps"]["dataFileName"],
  delay=config["gps"]["minTimePeriod"],
))
if config["accGyro"]["active"]: sensorList.append(accGyroThread(
  fileName=config["accGyro"]["dataFileName"],
  delay=config["accGyro"]["minTimePeriod"],
))
if config["camera"]["active"]: sensorList.append(cameraThread(
  delay=config["camera"]["minTimePeriod"],
  captureTime=config["camera"]["captureTime"],
))
  
mySensors = sensorsClass(*sensorList)
mySensors.startSensors()

while True:
  try:
    pass
  except KeyboardInterupt:
    mySensors.joinSensors()
