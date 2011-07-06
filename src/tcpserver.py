import time
import socket

class receiver:
	# public interface
	def receiveMsg(self): # commscontroller calls this method
		''' return decode(receive())'''
		self.receive()
	def setforwarder(self, forwarder):
		self.forwarder = forwarder
	# private interface specific to forwarder/receiver
	def receive(self):
		''' set up transmission to receive 
		... packet from forwarder. Optional timeout.
		... process message and close connection.
		... return message.'''
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind(("", 5000))
		server_socket.listen(1)
		while 1:
			print 'receiver waiting...'
			conn, address = server_socket.accept()
			print "Connection established with: ", address
			data = conn.recv(20)
			print 'message: %s' % data

	def decode(self, message):
		pass

class commscontroller:
	def __init__(self, forwarder, reciever):
		self.forwarder = forwarder
		self.reciever = reciever
		
x = receiver()
x.receive()