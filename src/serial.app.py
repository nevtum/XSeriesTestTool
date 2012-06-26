import serial
from time import sleep
from config.configmanager import metaRepository
from decoder import *

class comms:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout = 0)
        
    def Rx(self):
        data = self.ser.read(1000)
        if len(data) > 0:
            return ''.join(["%02X" % ord(x) for x in data])
    
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
com = comms(r"\\.\COM7", 38400)

while True:
    sleep(0.1)
    packet = com.Rx()
    meta = xdec.getMetaData(packet)
    if packet is not None:
        print meta.getPacketName(), packet
        logger.logData('incoming', meta.getPacketName(), packet)

