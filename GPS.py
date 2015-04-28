import serial, csv, Queue, threading, time

class GPS():
  def __init__(self):
    self.date = ''
    self.time = ''
    self.sats = ''
    self.lat = ''
    self.NS = ''
    self.lng = ''
    self.EW = ''
    self.alt = ''
    self.speed = ''
    self.hdop = ''
    
    self.port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0)
    
    self.workingSentence = ['$']
    self.sentenceQueue = Queue.Queue()
    self.checkQueue = Queue.Queue()
    self.processQueue = Queue.Queue()
    
    self.filename = "GPS.csv"
    
  def degrees(self, raw):
    if raw:
      if raw[0] == '0':
        degrees = round(int(raw[1:3]) + float(raw[3:]) / 60, 6)
        degrees -= 2 * degrees
      else:
        degrees = round(int(raw[0:2]) + float(raw[2:]) / 60, 6)
      return degrees
    else:
      return None
  
  def readData(self):    
    while self.port.inWaiting() > 0:
      lastChar = self.port.read()
      if lastChar == '$':
        if self.workingSentence:
          self.sentenceQueue.put(self.workingSentence)
          self.workingSentence = ['$']
      elif lastChar == '\n' or lastChar == '\r':
        pass
      elif lastChar == ',' or lastChar == '*':
        self.workingSentence.append('')
      else:
        self.workingSentence[-1] += lastChar
    
    while True:
      try:
        currentSentence = self.sentenceQueue.get(False)
        if currentSentence[0] == '$GPGGA' or currentSentence[0] == '$GPRMC':
          self.checkQueue.put(currentSentence)
        self.sentenceQueue.task_done()
      except Queue.Empty:
        break
    
    while True:
      try:
        currentSentence = self.checkQueue.get(False)
        currentSentence[0] = currentSentence[0][1:]
        check = int(currentSentence[-1], 16)
        del currentSentence[-1]
        
        calculatedCheck = 0
        for j in ','.join(currentSentence):
          calculatedCheck = calculatedCheck ^ ord(j)
      
        if check == calculatedCheck:
          self.processQueue.put(currentSentence)
          
        self.checkQueue.task_done()
      except Queue.Empty:
        break
    
    while True:
      try:
        currentSentence = self.processQueue.get(False)
        self.time = currentSentence[1][0:2] + ':' + currentSentence[1][2:4] + ':' + currentSentence[1][4:6]
          
        if currentSentence[0] == 'GPGGA':
          self.sats = currentSentence[7]
          self.hdop = currentSentence[8]    
          if currentSentence[6] > 0:
            self.lat = self.degrees(currentSentence[2])
            self.NS = currentSentence[3]
            self.lng = self.degrees(currentSentence[4])
            self.EW = currentSentence[5]
            self.alt = currentSentence[9]
          else:
            self.lat = self.NS = self.lng = self.EW = self.alt = ''
        
        elif currentSentence[0] == 'GPRMC':
          self.date = currentSentence[9][0:2] + '/' + currentSentence[1][2:4] + '/' + currentSentence[1][4:6]
          if currentSentence[2] == 'A':
            self.lat = self.degrees(currentSentence[3])
            self.NS = currentSentence[4]
            self.lng = self.degrees(currentSentence[5])
            self.EW = currentSentence[6]
            self.speed = currentSentence[7]
          else:
            self.lat = self.NS = self.lng = self.EW = self.speed = ''
            
      except Queue.Empty:
        break
    
  def readDataThread(self):
    while self.runThread:
      self.readData()
    
  def startRead(self):
    self.runThread = True
    self.readData() #Block this (main) thread until the initial set of data as been obtained
    self.readThread = threading.Thread(target=self.readDataThread) #Use a thread for the remaining reads
    self.readThread.start()
    
  def stopRead(self):
    self.runThread = False
    self.readThread.join()
  
  def createFile(self, filename=None):
    if not filename: filename = self.filename
    with open(filename, 'w') as csvfile:
      csvwriter = csv.writer(csvfile, dialect='excel')
      csvwriter.writerow(['date', 'time', 'sats', 'lat', 'NS', 'lng', 'EW', 'alt', 'speed', 'hdop'])
  
  def writeData(self, filename=None):
    if not filename: filename = self.filename
    with open(filename, 'a') as csvfile:
      csvwriter = csv.writer(csvfile, dialect='excel')
      csvwriter.writerow(self.returnResults())
      
  def returnResults(self):
    return [self.date, self.time, self.sats, self.lat, self.NS, self.lng, self.EW, self.alt, self.speed, self.hdop]
  
if __name__ == "__main__":
  myGPS = GPS()
  myGPS.createFile()
  myGPS.startRead()
  for i in range(0, 100):
    myGPS.writeData()
    print i, ': lat:', myGPS.lat, ' lng:', myGPS.lng
    time.sleep(1)
  myGPS.stopRead()