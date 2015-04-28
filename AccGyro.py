import time, csv, I2Clib

class accGyro(I2Clib.sensor):
    def __init__(self, gyroRange, accRange):
        raise Exception
        I2Clib.sensor.__init__(self, 0x68) #accGyro's address is 0x68
        self.write(0x6B, 0x00) #set everything to default
        self.write(0x1B, 0x00) #gyro config +- 2000 degree/second
        self.write(0x1C, 0x00) #accelerometer config +- 16g
        self.startTime = time.time()
        self.filename = "AccGyro.csv"
        
    def getGyroRange(self, gyroRange):
        gyroRanges = {
          250: 0x00,
          500: 
        }
        if gyro
        
    def getAcceleration(self):
        self.acc_x = self.readSignedDouble(0x3B)
        self.acc_y = self.readSignedDouble(0x3D)
        self.acc_z = self.readSignedDouble(0x3F)

    def getTemp(self):
        self.temp = self.readSignedDouble(0x41)

    def getGyro(self):
        self.gyro_x = self.readSignedDouble(0x43)
        self.gyro_y = self.readSignedDouble(0x45)
        self.gyro_z = self.readSignedDouble(0x47)
        
    def getResults(self):
        self.getAcceleration()
        self.getTemp()
        self.getGyro()
    
    def createFile(self, filename=None):
      if not filename: filename = self.filename
      with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(['Time', 'Acceleration x', 'Acceleration y', 'Acceleration z', 'Temperature', 'Gyroscope x', 'Gyroscope y', 'Gyroscope z'])
    
    def writeData(self, filename=None):
      if not filename: filename = self.filename
      with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(self.returnResults())
        
    def returnResults(self):
      return [time.time() - self.startTime, self.acc_x, self.acc_y, self.acc_z, self.temp, self.gyro_x, self.gyro_y, self.gyro_z]

if __name__ == '__main__':
    myAccGyro = accGyro()
    myAccGyro.createFile()
    for i in range(0, 100):
      myAccGyro.getResults()
      myAccGyro.writeData()
      time.sleep(1)
      print i, myAccGyro.returnResults()
