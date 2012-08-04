import serial
from config.configmanager import metaRepository
from decoder import *
from PyQt4.QtCore import QThread, SIGNAL

log = open('DebugLog.txt', 'w')

def DBGLOG(message):
    print message
    log.write(message + '\n')

class CommsThread(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.meta = metaRepository('settings/')
        self.xdec = XProtocolDecoder(self.meta)
        self.stopped = False

    def setcommport(self, port):
        self.commport = port

    def setbaud(self, baud):
        self.baud = int(baud)

    def run(self):
        com = comms(self.commport, self.baud)
        logger = DataLogger('test.db')
        self.stopped = False
        BUFFER = []
        DBGLOG("Serial thread started!")
        print self.commport, self.baud
        while True:
            DBGLOG("Awaiting packet...")
            if self.stopped:
                DBGLOG("Serial thread stopped!")
                break
            newbuffer = com.Rx()
            if newbuffer:
                BUFFER += newbuffer
            while len(BUFFER) > 0:
                DBGLOG(''.join(["%02X" % x for x in BUFFER]))
                packetinfo = self.xdec.getMetaData(BUFFER)
                if packetinfo.getPacketName() == "unknown":
                    packet = BUFFER
                    BUFFER = []
                    break
                expectedlength = packetinfo.getPacketLength()
                if expectedlength < len(BUFFER):
                    DBGLOG("packet length larger than expected length")
                    DBGLOG('expected = %i, actual = %i' % (expectedlength, len(BUFFER)))
                    packet = BUFFER[:expectedlength]
                    BUFFER = BUFFER[expectedlength:]
                    logger.logData('incoming', packetinfo.getPacketName(), packet)
                    self.emit(SIGNAL("receivedpacket"))
                elif expectedlength > len(BUFFER):
                    DBGLOG("packet length smaller than expected length")
                    break
                else:
                    packet = BUFFER[:]
                    BUFFER = []
                    logger.logData('incoming', packetinfo.getPacketName(), packet)
                    self.emit(SIGNAL("receivedpacket"))

                print packetinfo.getPacketName()

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
