import time
import socket

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