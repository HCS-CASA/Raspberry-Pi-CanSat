Raspberry Wheezy
============
http://www.raspberrypi.org/downloads/
Check the sha1-sum on downloading

Boot Options
============
```
sudo raspi-config
```

SSH -> Yes
Serial Console -> Yes
I2C -> Yes
SPI -> Yes

Reboot

Dependancies
============
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-pip python-smbus git
sudo pip install picamera
```

Modules
=======
```
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```
Ensure the following are commented out:
```
#blacklist spi-bcm2708
#blacklist i2c-bcm2708
```
    
```
sudo nano /etc/modules
```
Ensure the following are in the file
```
snd-bcm2835
i2c-dev
```

Main Code
=========
From Pi Home Dir
```
git clone https://github.com/william1616/CASA.git
cd CASA
sudo python main.py 10 0 (run the code with 10 minutes and 0 second countdown timer)
```
