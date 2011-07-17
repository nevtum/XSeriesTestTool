import time
import socket

####
import asyncore

class asyncreceiver(asyncore.dispatcher):
	def __init__(self, hostname, portnr):
		asyncore.dispatcher.__init__(self)
		self.hostname = hostname
		self.portnr = portnr
		self.msg = None
		self.startservice()
	def startservice(self):
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((self.hostname, self.portnr))
		self.listen(1)
	def handle_accept(self):
		self.accept()
		print 'accepted connection from client...'
	def handle_read(self):
		self.msg = self.recv(256)
		print 'received: %s' % self.msg
	def handle_close(self):
		self.close()
		self.startservice()
	def receiveMsg(self):
		return self.msg

class asyncforwarder(asyncore.dispatcher):
	def __init__(self, hostname, portnr):
		asyncore.dispatcher.__init__(self)
		self.hostname = hostname
		self.portnr = portnr
	def transmitMsg(self, msg):
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((self.hostname, self.portnr))
		self.send(msg)
		self.close()

f = asyncforwarder('localhost', 2020)
r = asyncreceiver('', 2020)
f.transmitMsg('hey there maddie!')
asyncore.loop()
f.transmitMsg('hey there maddie!')

####

class receiver:
	# public interface
	def __init__(self, hostname, portnr):
		self.hostname = hostname
		self.portnr = portnr
	def receiveMsg(self): # commscontroller calls this method
		return self.decode(self.receive()) # add locking mechanism
		print 'finished listening'
	# private interface specific to forwarder/receiver
	def receive(self):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((self.hostname, self.portnr))
		server_socket.listen(1)
		conn, address = server_socket.accept()
		msg = conn.recv(256)
		conn.close()
		server_socket.close()
		return msg
	def decode(self, msg):
		return msg