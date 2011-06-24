# TCP client example
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5000))
while 1:
    data = client_socket.recv(128)
    print "RECIEVED:" , data