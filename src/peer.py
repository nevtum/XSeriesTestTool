from forwarder import forwarder
from receiver import receiver
from threading import Thread

class repeater(Thread):
    def __init__(self):
    	Thread.__init__(self)
        self.receiver = receiver('', 12345)
        self.forwarder = forwarder('localhost', 33333)
    def run(self):
    	while self.isAlive():
    		repeatmsg = self.receiver.receiveMsg()
    		self.forwarder.transmitMsg(repeatmsg)
	
class peer(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.receiver = receiver('', 33333)
		self.forwarder = forwarder('localhost', 12345)
		self.msg = None
	def run(self):
		while self.isAlive():
			self.msg = self.receiver.receiveMsg()
	def sendMsg(self, msg):
		self.forwarder.transmitMsg(msg)
	def getMsg(self):
		return self.msg