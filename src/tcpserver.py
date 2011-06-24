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