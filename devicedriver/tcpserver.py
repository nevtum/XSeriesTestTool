# TCP server example
import time
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5000))
server_socket.listen(5)

print "TCPServer Waiting for client on port 5000"

while 1:
	client_socket, address = server_socket.accept()
	print "Connection established with: ", address
	while 1:
		data = '1'
		client_socket.send(data)
		time.sleep(0.5)