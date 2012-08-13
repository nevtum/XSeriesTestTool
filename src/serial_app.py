import serial
from datetime import datetime

log = open('DebugLog.txt', 'w')

def DBGLOG(message):
    print message
    log.write("%s %s\n" % (str(datetime.now()), message))

class SerialModule:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout = 10)
        
    def Rx(self):
        data = self.ser.read(1)
        remainder = self.ser.inWaiting()
        data2 = self.ser.read(remainder)
        seq = [x for x in bytearray(data + data2)] # unmarshal data
        if len(seq) > 0:
            DBGLOG(str(seq))
            return seq
    
    def Tx(self, seq):
        assert(isinstance(seq, list))
        for byte in seq:
            assert(0 <= byte <= 255)
        self.ser.write(bytearray(seq)) # marshal data and write
        
    def __del__(self):
        self.ser.close()

    def close(self):
        self.ser.close()
