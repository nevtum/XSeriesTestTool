import serial

class SerialModule:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout = 1)
        
    def Rx(self):
        data = self.ser.read(1)
        remainder = self.ser.inWaiting()
        data2 = self.ser.read(remainder)
        seq = [x for x in bytearray(data + data2)] # unmarshal data
        if len(seq) > 0:
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

import platform

def list_serial_ports():
    system_name = platform.system()
    if system_name == "Windows":
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append(i+1)
                s.close()
            except serial.SerialException:
                pass
        return available