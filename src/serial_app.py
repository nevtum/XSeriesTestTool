import serial
from config.configmanager import metaRepository
from decoder import *
from PyQt4.QtCore import QThread, SIGNAL


class CommsThread(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.meta = metaRepository('settings/')
        self.xdec = XProtocolDecoder(self.meta)
        self.stopped = False

    def run(self):
        com = comms(r"\\.\COM17", 9600)
        logger = DataLogger('test.db')
        self.stopped = False
        print "Serial thread started!"
        while True:
            #print "Awaiting packet..."
            if self.stopped:
                print "Serial thread stopped!"
                break
            packet = com.Rx()
            packetinfo = self.xdec.getMetaData(packet)
            if packet is not None:
                #print packetinfo.getPacketName(), ''.join(["%02X" % x for x in packet])
                logger.logData('incoming', packetinfo.getPacketName(), packet) #not currently working
                self.emit(SIGNAL("receivedpacket"))
        com.close()

    def quit(self):
        # this bit is not thread safe. Make improvements later.
        self.stopped = True

class comms:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout = 10)
        
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

    def close(self):
        self.ser.close()
