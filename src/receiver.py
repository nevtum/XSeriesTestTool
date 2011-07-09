import time
import socket

class receiver:
	# public interface
	def receiveMsg(self): # commscontroller calls this method
		return self.decode(self.receive())
	# private interface specific to forwarder/receiver
	def receive(self):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind(("", 5000))
		server_socket.listen(1)
		conn, address = server_socket.accept()
		data = conn.recv(256)
		conn.close()
		server_socket.close()
		return data
	def decode(self, msg):
		return msg
		
x = receiver()
msg = x.receiveMsg() # currently blocking
print 'received: %s' % msg