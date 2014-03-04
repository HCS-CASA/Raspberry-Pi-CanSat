import RPi.GPIO as GPIO
import spidev
from time import sleep

class TransmitReceive():
    def __init__(self):
        self.initVar()
        self.initSPI()
        self.reset()
        self.initReg()
        self.write(self.PATABLE, self.PATABELVAL)
        
    def initVar(self):
        #CC1101 CONFIG REGSITER
        self.IOCFG2 = 0x00           # GDO2 output pin configuration
        self.IOCFG1 = 0x01           # GDO1 output pin configuration
        self.IOCFG0 = 0x02           # GDO0 output pin configuration
        self.FIFOTHR = 0x03          # RX FIFO and TX FIFO thresholds
        self.SYNC1 = 0x04            # Sync word, high INT8U
        self.SYNC0 = 0x05            # Sync word, low INT8U
        self.PKTLEN = 0x06           # Packet length
        self.PKTCTRL1 = 0x07         # Packet automation control
        self.PKTCTRL0 = 0x08         # Packet automation control
        self.ADDR = 0x09                 # Device address
        self.CHANNR = 0x0A           # Channel number
        self.FSCTRL1 = 0x0B          # Frequency synthesizer control
        self.FSCTRL0 = 0x0C          # Frequency synthesizer control
        self.FREQ2 = 0x0D            # Frequency control word, high INT8U
        self.FREQ1 = 0x0E            # Frequency control word, middle INT8U
        self.FREQ0 = 0x0F            # Frequency control word, low INT8U
        self.MDMCFG4 = 0x10          # Modem configuration
        self.MDMCFG3 = 0x11          # Modem configuration
        self.MDMCFG2 = 0x12          # Modem configuration
        self.MDMCFG1 = 0x13          # Modem configuration
        self.MDMCFG0 = 0x14          # Modem configuration
        self.DEVIATN = 0x15          # Modem deviation setting
        self.MCSM2 = 0x16            # Main Radio Control State Machine configuration
        self.MCSM1 = 0x17            # Main Radio Control State Machine configuration
        self.MCSM0 = 0x18            # Main Radio Control State Machine configuration
        self.FOCCFG = 0x19           # Frequency Offset Compensation configuration
        self.BSCFG = 0x1A            # Bit Synchronization configuration
        self.AGCCTRL2 = 0x1B         # AGC control
        self.AGCCTRL1 = 0x1C         # AGC control
        self.AGCCTRL0 = 0x1D         # AGC control
        self.WOREVT1 = 0x1E          # High INT8U Event 0 timeout
        self.WOREVT0 = 0x1F          # Low INT8U Event 0 timeout
        self.WORCTRL = 0x20          # Wake On Radio control
        self.FREND1 = 0x21           # Front end RX configuration
        self.FREND0 = 0x22           # Front end TX configuration
        self.FSCAL3 = 0x23           # Frequency synthesizer calibration
        self.FSCAL2 = 0x24           # Frequency synthesizer calibration
        self.FSCAL1 = 0x25           # Frequency synthesizer calibration
        self.FSCAL0 = 0x26           # Frequency synthesizer calibration
        self.RCCTRL1 = 0x27          # RC oscillator configuration
        self.RCCTRL0 = 0x28          # RC oscillator configuration
        self.FSTEST = 0x29           # Frequency synthesizer calibrationa control
        self.PTEST = 0x2A            # Production test
        self.AGCTEST = 0x2B          # AGC test
        self.TEST2 = 0x2C            # Various test settings
        self.TEST1 = 0x2D            # Various test settings
        self.TEST0 = 0x2E            # Various test settings
        
        #CC1101 STROBE COMMANDS
        self.SRES = 0x30             # Reset chip.
        self.SFSTXON = 0x31          # Enable and calibrate frequency synthesizer (if MCSM0.FS_AUTOCAL=1).
                                     # If in RX/TX: Go to a wait state where only the synthesizer is
                                     # running (for quick RX / TX turnaround).
        self.SXOFF = 0x32            # Turn off crystal oscillator.
        self.SCAL = 0x33             # Calibrate frequency synthesizer and turn it off
                                     # (enables quick start).
        self.SRX = 0x34              # Enable RX. Perform calibration first if coming from IDLE and
                                     # MCSM0.FS_AUTOCAL=1.
        self.STX = 0x35              # In IDLE state: Enable TX. Perform calibration first if
                                     # MCSM0.FS_AUTOCAL=1. If in RX state and CCA is enabled:
                                     # Only go to TX if channel is clear.
        self.SIDLE = 0x36            # Exit RX / TX, turn off frequency synthesizer and exit
                                     # Wake-On-Radio mode if applicable.
        self.SAFC = 0x37             # Perform AFC adjustment of the frequency synthesizer
        self.SWOR = 0x38             # Start automatic RX polling sequence (Wake-on-Radio)
        self.SPWD = 0x39             # Enter power down mode when CSn goes high.
        self.SFRX = 0x3A             # Flush the RX FIFO buffer.
        self.SFTX = 0x3B             # Flush the TX FIFO buffer.
        self.SWORRST = 0x3C          # Reset real time clock.
        self.SNOP = 0x3D             # No operation. May be used to pad strobe commands to two
                                     # INT8Us for simpler software.
                                     
        #CC1101 STATUS REGSITER
        self.PARTNUM = 0x30
        self.VERSION = 0x31
        self.FREQEST = 0x32
        self.LQI = 0x33
        self.RSSI = 0x34
        self.MARCSTATE = 0x35
        self.WORTIME1 = 0x36
        self.WORTIME0 = 0x37
        self.PKTSTATUS = 0x38
        self.VCO_VC_DAC = 0x39
        self.TXBYTES = 0x3A
        self.RXBYTES = 0x3B

        #CC1101 PATABLE,TXFIFO,RXFIFO
        self.PATABLE = 0x3E
        self.TXFIFO = 0x3F
        self.RXFIFO = 0x3F
        
        #bit constsants
        self.WRITE_BURST = 0x40      #write burst
        self.READ_SINGLE = 0x80      #read single
        self.READ_BURST = 0xC0       #read burst
        self.BYTES_IN_RXFIFO = 0x7F  #byte number in RXfifo
        
        #Patable
        self.PATABELVAL = [0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60]
        
    def initSPI(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.cshigh = False
        
    def reset(self):
        self.write(self.SRES)
        
    def initReg(self):
        self.write(self.FSCTRL1, 0x08)
        self.write(self.FSCTRL0, 0x00)
        self.write(self.FREQ2, 0x10)
        self.write(self.FREQ1, 0xA7)
        self.write(self.FREQ0, 0x62)
        self.write(self.MDMCFG4, 0x5B)
        self.write(self.MDMCFG3, 0xF8)
        self.write(self.MDMCFG2, 0x03)
        self.write(self.MDMCFG1, 0x22)
        self.write(self.MDMCFG0, 0xF8)
        self.write(self.CHANNR, 0x00)
        self.write(self.DEVIATN, 0x47)
        self.write(self.FREND1, 0xB6)
        self.write(self.FREND0, 0x10)
        self.write(self.MCSM0 , 0x18)
        self.write(self.FOCCFG, 0x1D)
        self.write(self.BSCFG, 0x1C)
        self.write(self.AGCCTRL2, 0xC7)
        self.write(self.AGCCTRL1, 0x00)
        self.write(self.AGCCTRL0, 0xB2)
        self.write(self.FSCAL3, 0xEA)
        self.write(self.FSCAL2, 0x2A)
        self.write(self.FSCAL1, 0x00)
        self.write(self.FSCAL0, 0x11)
        self.write(self.FSTEST, 0x59)
        self.write(self.TEST2, 0x81)
        self.write(self.TEST1, 0x35)
        self.write(self.TEST0, 0x09)
        self.write(self.IOCFG2, 0x0B)    #serial clock.synchronous to the data in synchronous serial mode
        self.write(self.IOCFG0, 0x06)    #asserts when sync word has been sent/received, and de-asserts at the end of the packet 
        self.write(self.PKTCTRL1, 0x04)  #two status bytes will be appended to the payload of the packet,including RSSI LQI and CRC OK
                                         #No address check
        self.write(self.PKTCTRL0, 0x05)  #whitening offCRC Enable variable length packets, packet length configured by the first byte after sync word
        self.write(self.ADDR, 0x00)      #address used for packet filtration.
        self.write(self.PKTLEN, 0x3D)    #61 bytes max length
    
    def sendData(self, data):
        #data must be a list
        self.write(self.TXFIFO, len(data))
        data.append(len(data))
        self.write(self.TXFIFO, data)
        self.write(self.STX)
        while self.read(self.PKTSTATUS) & 0x01 == 0:
            pass
        while self.read(self.PKTSTATUS) & 0x01 == 1:
            pass
        self.write(self.SFTX)
    
    def write(self, addr, val=None):  
        if val:
            data = [addr | self.WRITE_BURST]
            if isinstance(val, int):
                val = [val]
            elif not isinstance(val, list):
                raise TypeError("val must be a list or an integer")
            data.extend(val)
        else:
            data = [addr]
        
        self.spi.writebytes(data)
        
    def read(self, addr, num=1):
        if num == 1: 
            data = [addr | self.READ_SINGLE]
        else:
            data = [addr | self.READ_BURST]
            
        data.extend([0] * num)
        
        if num ==1:
            return self.spi.xfer2(data)[1]
        else:
            return self.spi.xfer2(data)[1:]
