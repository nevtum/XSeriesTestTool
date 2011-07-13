import socket

class forwarder:
    # public interface
    def __init__(self, hostname, portnr):
        self.hostname = hostname
        self.portnr = portnr
    def transmitMsg(self, msg): # commscontroller calls this method
        self.transmit(self.encode(msg))
    # private interface specific to forwarder/receiver
    def transmit(self, msg): # specific to receiver only
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.hostname, self.portnr))
        client_socket.send(msg)
        client_socket.close()
    def encode(self, msg):
        return msg
