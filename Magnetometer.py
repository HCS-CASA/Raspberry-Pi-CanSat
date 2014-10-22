import time, csv, I2Clib

class Magnetometer(I2Clib.sensor):
  def __init__(self):
    I2Clib.sensor.__init__(self, 0x1E) #Magnetometer's address is 0x1E
    self.write(0x02, 0x00) #Start continuous reading mode
    self.filename = "Magnetometer.csv"
    self.startTime = time.time()

  def getMagnet(self):
    while not self.readSigned(0x09) & 0x01 == 0x01: #Wait for data
      pass
    self.mag_x = self.readSignedDouble(0x03)
    self.mag_y = self.readSignedDouble(0x05)
    self.mag_z = self.readSignedDouble(0x07)
        
  def getResults(self):
    self.getMagnet()
        
  def returnResults(self):
    return [time.time() - self.startTime, self.mag_x, self.mag_y, self.mag_z]
    
  def createFile(self, filename=None):
    if not filename: filename = self.filename
    with open(filename, 'w') as csvfile:
      csvwriter = csv.writer(csvfile, dialect='excel')
      csvwriter.writerow(['Time', 'Mag x', 'Mag y', 'Mag z']) #print the measurment names
    
  def writeData(self, filename=None):
    if not filename: filename = self.filename
    with open(filename, 'a') as csvfile:
      csvwriter = csv.writer(csvfile, dialect='excel')
      csvwriter.writerow(self.returnResults())
    
if __name__ == '__main__':
  myMagnetometer = Magnetometer()
  myMagnetometer.createFile()
  for i in range(0, 100):
    myMagnetometer.getResults()
    myMagnetometer.writeData()
    time.sleep(1)
    print i, 'Mag x:', myMagnetometer.mag_x, 'Mag y:', myMagnetometer.mag_y, 'Mag z:', myMagnetometer.mag_z
