import socket

class forwarder:
    # public interface
    def transmitMsg(self): # commscontroller calls this method
        ''' encode(message)
        ... transmit()'''
    def setreceiver(self, receiver):
        self.receiver = receiver
    # private interface specific to forwarder/receiver
    def transmit(self): # specific to receiver only
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 5000))
        while 1:
            client_socket.send('Hey!!')
            client_socket.close()
    def encode(self, message):
        pass
    
f = forwarder()
f.transmit()
