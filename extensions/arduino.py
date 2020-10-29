import serial

class Arduino():
    ser=None
    def __init__(self,port='/dev/ttyACM0'):
        self.ser=serial.Serial(port,115200)
	
    def sendtext(self,text):
        self.ser.write(text)


