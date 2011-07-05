# TCP server example
from generators import *
import time
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5000))
server_socket.listen(5)

file = open('SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t')
b = charpacket(a, size = 2)
c = datablockdispatcher(b)

print "TCPServer Waiting for client on port 5000"

while 1:
	client_socket, address = server_socket.accept()
	print "Connection established with: ", address
	for eachpacket in c:
		client_socket.send(''.join(eachpacket))
		time.sleep(0.5)

class forwarder:
	# public interface
	def transmitMsg(self): # commscontroller calls this method
		''' encode(message)
		... transmit()'''
	def setreceiver(self, receiver):
		self.receiver = receiver
	# private interface specific to forwarder/receiver
	def transmit(self): # specific to receiver only
		''' set up transmission to dispatch
		... packet to receiver.
		... when finished close connection'''
	def encode(self, message):
		pass

class receiver:
	# public interface
	def recieveMsg(self): # commscontroller calls this method
		''' return decode(receive())'''
	def setforwarder(self, forwarder):
		self.forwarder = forwarder
	# private interface specific to forwarder/receiver
	def receive(self):
		''' set up transmission to receive 
		... packet from forwarder. Optional timeout.
		... process message and close connection.
		... return message.'''
	def decode(self, message):
		pass

class commscontroller:
	def __init__(self, forwarder, reciever):
		self.forwarder = forwarder
		self.reciever = reciever