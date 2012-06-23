import serial
from time import sleep
from config.configmanager import metaRepository
from decoder import *

class comms:
	def __init__(self, port, baud):
		self.ser = serial.Serial(port, baud, timeout = 0)
		
	def read(self):
		data = self.ser.read(1000)
		if len(data) > 0:
			return ''.join(["%02X" % ord(x) for x in data])
			
	def startreceiving(self):
		xmetadata = metaRepository('settings/')
		self.xdec = XProtocolDecoder(xmetadata)
		self.xdec.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
		self.xdec.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
		self.xdec.registerTypeDecoder('boolean', booleanDecoder)
		self.xdec.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)
		
		while True:
			sleep(0.1)
			packet = self.read()
			if packet is not None:
				print self.xdec.createXMLPacket(packet)
		
	def __del__(self):
		self.ser.close()

c = comms(r"\\.\COM7", 38400)
c.startreceiving()
