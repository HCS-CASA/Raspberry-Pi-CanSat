from time import sleep
#from transmitReceive import TransmitReceive
from Camera import camera
#from gps import GPS
from AccGyro import accGyro
from TempPressureSensor import tempPressure

#Setup Sensors
#AccGyro
myAccGyro = accGyro()
myAccGyro.createFile()

#TempPressure
myTempPressure = tempPressure()
myTempPressure.createFile()

#Loop
with camera() as cam:
  while True:
    #Record Data
    print "lat:", myGPS.lat, "lng:", myGPS.lng
    myAccGyro.getResults()
    myAccGyro.writeData()
    print 'Acceleration x:', myAccGyro.acc_x, 'Acceleration y:', myAccGyro.acc_y, 'Acceleration z:', myAccGyro.acc_z, 'Temperature:', myAccGyro.temp, 'Gyroscope x:', myAccGyro.gyro_x, 'Gyroscope y:', myAccGyro.gyro_y, 'Gyroscope z:', myAccGyro.gyro_z
    myTempPressure.getResults()
    myTempPressure.writeData()
    print "Temperature:", myTempPressure.temp, "Pressure:", myTempPressure.pressure
    
    cam.capture()
