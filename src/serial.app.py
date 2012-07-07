import serial
from config.configmanager import metaRepository
from decoder import *

class comms:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout = None)
        
    def Rx(self):
        data = self.ser.read(1)
        remainder = self.ser.inWaiting()
        data2 = self.ser.read(remainder)
        BUFFER = bytearray(data + data2)
        if len(data) > 0:
            return [x for x in BUFFER]
    
    def Tx(self):
        pass
        
    def __del__(self):
        self.ser.close()

xmetadata = metaRepository('settings/')
xdec = XProtocolDecoder(xmetadata)
xdec.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
xdec.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
xdec.registerTypeDecoder('boolean', booleanDecoder)
xdec.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)

logger = DataLogger('test.db')
com = comms(r"\\.\COM7", 9600)

while True:
    packet = com.Rx()
    meta = xdec.getMetaData(packet)
    if packet is not None:
        #print meta.getPacketName(), ''.join(["%02X" % x for x in packet])
        print xdec.createXMLPacket(packet)
        logger.logData('incoming', meta.getPacketName(), packet)

