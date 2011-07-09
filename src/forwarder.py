import socket

class forwarder:
    # public interface
    def transmitMsg(self, msg): # commscontroller calls this method
        self.transmit(self.encode(msg))
    # private interface specific to forwarder/receiver
    def transmit(self, msg): # specific to receiver only
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 5000))
        client_socket.send(msg)
        client_socket.close()
    def encode(self, msg):
        return msg
    
f = forwarder()
f.transmitMsg(u'FF00020100563412')
