import serial, csv

def degrees(raw):
  if raw[0] == '0':
    degrees = round(int(raw[1:3]) + float(raw[3:]) / 60, 6)
    degrees -= 2 * degrees
  else:
    degrees = round(int(raw[0:2]) + float(raw[2:]) / 60, 6)
  return degrees

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0)
sentenceStack = [['']]
checkStack = []
processStack = []

lat = NS = lng = EW = alt = speed = date = time = sats = hdop = ''

with open('gps.csv', 'w') as csvfile:
  csvwriter = csv.writer(csvfile, dialect='excel')
  csvwriter.writerow(['date', 'time', 'sats', 'lat', 'NS', 'lng', 'EW', 'alt', 'speed', 'hdop'])

while True:
  if port.inWaiting() > 0:
    lastChar = port.read()
    if lastChar == '$':
      sentenceStack.append([lastChar])
    elif lastChar == '\n' or lastChar == '\r':
      pass
    elif lastChar == ',' or lastChar == '*':
      sentenceStack[len(sentenceStack) - 1].append('')
    else:
      sentenceStack[len(sentenceStack) - 1][len(sentenceStack[len(sentenceStack) - 1]) - 1] += lastChar

  while len(sentenceStack) > 1:
    if sentenceStack[0][0] == '$GPGGA' or sentenceStack[0][0] == '$GPRMC':
      checkStack.append(sentenceStack[0])
    del sentenceStack[0]
    
  for sentence in checkStack:
    sentence[0] = sentence[0][1:]
    check = int(sentence[len(sentence) - 1], 16)
    del sentence[len(sentence) - 1]
    
    check2 = 0
    for j in ','.join(sentence):
      check2 = check2 ^ ord(j)
      
    if check == check2:
      processStack.append(sentence)
    
  checkStack = []
  
  for sentence in processStack:
    time = sentence[1][0:2] + ':' + sentence[1][2:4] + ':' + sentence[1][4:6]
    
    if sentence[0] == 'GPGGA':
      sats = sentence[7]
      hdop = sentence[8]    
      if sentence[6] > 0:
        lat = degrees(sentence[2])
        NS = sentence[3]
        lng = degrees(sentence[4])
        EW = sentence[5]
        alt = sentence[9]
      else:
        lat = NS = lng = EW = alt = ''
    
    elif sentence[0] == 'GPRMC':
      date = sentence[9][0:2] + '/' + sentence[1][2:4] + '/' + sentence[1][4:6]
      if sentence[2] == 'A':
        lat = degrees(sentence[3])
        NS = sentence[4]
        lng = degrees(sentence[5])
        EW = sentence[6]
        speed = sentence[7]      
      else:
        lat = NS = lng = EW = speed = ''
    
    with open('gps.csv', 'a') as csvfile:
      csvwriter = csv.writer(csvfile, dialect='excel')
      csvwriter.writerow([date, time, sats, lat, NS, lng, EW, alt, speed, hdop])
  
  processStack = []