from forwarder import forwarder
from receiver import receiver
from threading import Thread

class repeater(Thread):
	def __init__(self, portnr):
		Thread.__init__(self)
		self.receiver = receiver('', portnr)
	def setforwarder(self, location, portnr):
		self.forwarder = forwarder(location, portnr)
	def run(self):
		while self.isAlive():
			repeatmsg = self.receiver.receiveMsg()
			self.forwarder.transmitMsg(repeatmsg)
	
class peer(Thread):
	def __init__(self, portnr):
		Thread.__init__(self)
		self.receiver = receiver('', portnr)
		self.msg = None
	def setforwarder(self, location, portnr):
		self.forwarder = forwarder(location, portnr)
	def run(self):
		while self.isAlive():
			self.msg = self.receiver.receiveMsg()
	def sendMsg(self, msg):
		self.forwarder.transmitMsg(msg)
	def getMsg(self):
		return self.msg