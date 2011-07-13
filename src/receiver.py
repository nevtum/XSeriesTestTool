import time
import socket
from threading import Thread

class receiver(Thread):
	# public interface
	def __init__(self):
		Thread.__init__(self)
		self.msg = None
	def receiveMsg(self): # commscontroller calls this method
		return self.decode(self.msg) # add locking mechanism
	def run(self):
		while self.isAlive():
			self.receive()
		print 'finished listening'
	def kill(self):
		raise RuntimeError
	# private interface specific to forwarder/receiver
	def receive(self):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind(("", 5000))
		server_socket.listen(1)
		conn, address = server_socket.accept()
		self.msg = conn.recv(256)
		conn.close()
		server_socket.close()
	def decode(self, msg):
		return msg