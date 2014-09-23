from time import sleep
from transmitReceive import TransmitReceive
from gps import GPS
from AccGyro import accGyro
from TempPressureSensor import tempPressure

#Setup Sensors
#GPS
myGPS = GPS()
myGPS.createFile()
myGPS.startRead()

#AccGyro
myAccGyro = accGyro()
myAccGyro.createFile()

#TempPressure
myTempPressure = tempPressure()
myTempPressure.createFile()

#TransmitReceive
myTransmitReceive = TransmitReceive()

#Loop
while True:
  #Record Data
  myGPS.writeData()
  print "lat:", myGPS.lat, "lng:", myGPS.lng
  myAccGyro.getResults()
  myAccGyro.writeData()
  print 'Acceleration x:', myAccGyro.acc_x, 'Acceleration y:', myAccGyro.acc_y, 'Acceleration z:', myAccGyro.acc_z, 'Temperature:', myAccGyro.temp, 'Gyroscope x:', myAccGyro.gyro_x, 'Gyroscope y:', myAccGyro.gyro_y, 'Gyroscope z:', myAccGyro.gyro_z
  myTempPressure.getResults()
  myTempPressure.writeData()
  print "Temperature:", myTempPressure.temp, "Pressure:", myTempPressure.pressure
  
  #Broadcast Data
  transmitString = "$" + str(myGPS.lat) + "*" + str(myGPS.lng) + "&"
  print transmitString
  myTransmitReceive.sendData([ord(char) for char in transmitString])
  
  #Sleep
  sleep(1)

#End
myGPS.stopRead()