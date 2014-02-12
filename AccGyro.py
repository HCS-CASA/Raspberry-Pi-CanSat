import time, csv, I2Clib
	
class accGyro(I2Clib.sensor):
	def __init__(self):
		I2Clib.sensor.__init__(self, 0x68) #accGyro's address is 0x68
		self.write(0x6B, 0x00) #set everything to default
		self.write(0x1B, 0x18) #gyro config +- 250 degree/second
		self.write(0x6C, 0x18) #accelerometer config +- 2g
		
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
		
	def returnResults(self):
		return [self.acc_x, self.acc_y, self.acc_z, self.temp, self.gyro_x, self.gyro_y, self.gyro_z]

if __name__ == '__main__':
	myAccGyro = accGyro()
	with open('AccGyro.csv', 'w') as csvfile: #open csv file
		csvwriter = csv.writer(csvfile, dialect='excel') #write in dos format
		csvwriter.writerow(['Acceleration x', 'Acceleration y', 'Acceleration z', 'Temperature', 'Gyroscope x', 'Gyroscope y', 'Gyroscope z']) #print the measurment names
		for i in range(0, 100):
			myAccGyro.getResults()
			csvwriter.writerow(myAccGyro.returnResults())
			time.sleep(1)
			print(i)
	