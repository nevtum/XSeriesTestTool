import serial
import time
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
        DBGLOG("port = %s, baud = %s" % (self.commport, self.baud))
        while True:
            DBGLOG("Awaiting packet...")
            if self.stopped:
                DBGLOG("Serial thread stopped!")
                break
            newbuffer = com.Rx()
            if newbuffer:
                BUFFER += newbuffer
            while len(BUFFER) > 0:
                packetinfo = self.xdec.getMetaData(BUFFER)
                if packetinfo.getPacketName() == "unknown":
                    packet = BUFFER
                    BUFFER = []
                    break
                expectedlength = packetinfo.getPacketLength()
                if  len(BUFFER) > expectedlength:
                    DBGLOG("packet length larger than expected length")
                    DBGLOG('expected = %i, actual = %i' % (expectedlength, len(BUFFER)))
                    packet = BUFFER[:expectedlength]
                    BUFFER = BUFFER[expectedlength:]
                    logger.logData('incoming', packetinfo.getPacketName(), packet)
                    self.emit(SIGNAL("receivedpacket"))
                elif len(BUFFER) < expectedlength:
                    DBGLOG("packet length smaller than expected length")
                    break
                else:
                    packet = BUFFER[:]
                    BUFFER = []
                    logger.logData('incoming', packetinfo.getPacketName(), packet)
                    self.emit(SIGNAL("receivedpacket"))

                DBGLOG(packetinfo.getPacketName())
        com.close()

    def quit(self):
        # this bit is not thread safe. Make improvements later.
        self.stopped = True

class ReplayThread(QThread):
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
        print "replaying data"
        #logger = DataLogger('test.db')
        logger = DataLogger('replay.db')
        com = comms(self.commport, self.baud)
        list = logger.queryData("SELECT hex FROM packetlog ORDER BY timestamp ASC LIMIT 100")
        for entry in list:
            if self.stopped:
                return
            if len(entry) == 1:
                DBGLOG(entry[0])
                seq = [x for x in bytearray.fromhex(entry[0])]
                com.Tx(seq)
                packetinfo = self.xdec.getMetaData(seq)
                logger.logData('outgoing', packetinfo.getPacketName(), seq)
                time.sleep(1)
                
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
        seq = [x for x in bytearray(data + data2)] # unmarshal data
        if len(seq) > 0:
            print seq
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
