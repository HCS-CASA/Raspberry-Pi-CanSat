import smbus

class sensor():
	def __init__(self, address, bus=smbus.SMBus(1)):
		self.ICaddress = address
		self.bus = bus
	
	def readSignedDouble(self, address): #read 2 bytes
		msb = self.readSigned(address) #read first signed byte
		lsb = self.readUnsigned(address + 1) #read second byte from next address along
		return (msb << 8) + lsb #shift the first byte 1 bytes worth of bits (8 bits) to the left and add the second byte to this shifted number
		
	def readUnsignedDouble(self, address): #read 2 bytes
		msb = self.readUnsigned(address) #read first byte
		lsb = self.readUnsigned(address + 1) #read second byte from next address along
		return (msb << 8) + lsb #shift the first byte 1 bytes worth of bits (8 bits) to the left and add the second byte to this shifted number

	def readSigned(self, address): #read 1 byte
		result = self.bus.read_byte_data(self.ICaddress, address)
		if result > 127: #if the signed bit is used convert the number to negative
			result -= 256
		return result

	def readUnsigned(self, address): #read 1 byte
		result = self.bus.read_byte_data(self.ICaddress, address)
		return result
		
	def write(self, address, byte): #write 1 byte
		self.bus.write_byte_data(self.ICaddress, address, byte)