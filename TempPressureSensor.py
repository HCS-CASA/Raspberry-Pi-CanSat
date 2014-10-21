import time, csv, I2Clib

class tempPressure(I2Clib.sensor):
    def __init__(self):
        I2Clib.sensor.__init__(self, 0x77) #tempPressure's address is 0x77
        self.oss = 3
        #read calibration data from device
        self.ac1 = self.readSignedDouble(0xAA);
        self.ac2 = self.readSignedDouble(0xAC);
        self.ac3 = self.readSignedDouble(0xAE);
        self.ac4 = self.readUnsignedDouble(0xB0);
        self.ac5 = self.readUnsignedDouble(0xB2);
        self.ac6 = self.readUnsignedDouble(0xB4);
        self.b1 = self.readSignedDouble(0xB6);
        self.b2 = self.readSignedDouble(0xB8);
        self.mb = self.readSignedDouble(0xBA);
        self.mc = self.readSignedDouble(0xBC);
        self.md = self.readSignedDouble(0xBE);
        self.startTime = time.time()

    def returnConstants(self):
        #return the constants in a dictionary
        return {'ac1': self.ac1, 'ac2': self.ac2, 'ac3': self.ac3, 'ac4': self.ac4, 'ac5': self.ac5, 'ac6': self.ac6, 'b1': self.b1, 'b2': self.b2, 'mb': self.mb, 'mc': self.mc, 'md': self.md, 'oss': self.oss}

    def getTemp(self):
        self.write(0xF4, 0x2E) #start a measurment
        time.sleep(0.005) #wait 5 ms for the measurment to be taken
        self.temp = self.readUnsignedDouble(0xF6) #get the measurment
    
    def getPressure(self):
        self.write(0xF4, 0x34 + (self.oss << 6))    
        #time.sleep(float((2 + (3 << 3)) / 1000))
        time.sleep(0.026)
        msb = self.readUnsigned(0xF6)
        lsb = self.readUnsigned(0xF7)
        xlsb = self.readUnsigned(0xF8)
        self.pressure = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self.oss)
        
    def getResults(self):
        self.getTemp()
        self.getPressure()
        
    def returnResults(self):
        return [time.time() - self.startTime, self.temp, self.pressure]
        
    def createFile(self, filename="TempPressure.csv"):
      with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(list(self.returnConstants().keys())) #print the constant names
        csvwriter.writerow(list(self.returnConstants().values())) #print constant values - yes this is messy code
        csvwriter.writerow(['Time', 'Temp', 'Pressure']) #print the measurment names
    
    def writeData(self, filename="TempPressure.csv"):
      with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(self.returnResults())
    
if __name__ == '__main__':
    myTempPressure = tempPressure()
    myTempPressure.createFile()
    with open('TempPressure.csv', 'w') as csvfile: #open csv file
      for i in range(0, 100):
        myTempPressure.getResults()
        myTempPressure.writeData()
        time.sleep(1)
        print i, "Temp:", myTempPressure.temp, "Pressure:", myTempPressure.pressure
