import time
from decoder import *
from PyQt4.QtCore import QThread, SIGNAL
from debug import *

class ListenThread(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.factory = parent.factory
        self.filter = self.factory.getDuplicateDatablockFilter()
        self.terminate = False

    def setcommport(self, port):
        self.port = port

    def setbaud(self, baud):
        self.baud = int(baud)

    def run(self):
        dec = self.factory.getProtocolDecoder()
        publisher = self.factory.getPublisher()

        # add a try/finally statement in the future
        serial = self.factory.getSerialModule(self.port, self.baud)
        self.terminate = False
        BUFFER = []
        DBGLOG("Serial thread started!")
        DBGLOG("port = %s, baud = %s" % (self.port, self.baud))
        while True:
            DBGLOG("Awaiting packet...")
            if self.terminate:
                DBGLOG("Serial thread stopped!")
                break
            newbuffer = serial.Rx()
            if newbuffer:
                BUFFER += newbuffer
                DBGLOG("Bytes: %s" % str(BUFFER))
            while len(BUFFER) > 0:
                packetinfo = dec.getMetaData(BUFFER)
                expectedlength = packetinfo.getPacketLength()
                if packetinfo.getPacketName() == "unknown":
                    DBGLOG("Unknown packet received")
                    #packet = BUFFER
                    BUFFER = []
                    break
                elif expectedlength == 0:
                    break
                elif len(BUFFER) < expectedlength:
                    DBGLOG("packet length smaller than expected length")
                    DBGLOG('expected = %i, actual = %i' % (expectedlength, len(BUFFER)))
                    break

                if  len(BUFFER) > expectedlength:
                    DBGLOG("packet length larger than expected length")
                    DBGLOG('expected = %i, actual = %i' % (expectedlength, len(BUFFER)))
                    packet = BUFFER[:expectedlength]
                    BUFFER = BUFFER[expectedlength:]
                else:
                    packet = BUFFER[:]
                    BUFFER = []

                publisher.Record(packet)
                self.emit(SIGNAL("receivedpacket"))

                DBGLOG("TYPE: %s" % packetinfo.getPacketName())
        serial.close()

    def quit(self):
        # this bit is not thread safe. Make improvements later.
        self.terminate = True

class ReplayThread(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.factory = parent.factory
        self.terminate = False

    def setcommport(self, port):
        self.port = port

    def setbaud(self, baud):
        self.baud = int(baud)

    def run(self):
        DBGLOG("replaying data")
        dec = self.factory.getProtocolDecoder()
        logger = self.factory.getDataLogger('test.db')
        serial = self.factory.getSerialModule(self.port, self.baud)
        query = "SELECT hex FROM packetlog where direction ='incoming' ORDER BY timestamp ASC LIMIT 100"
        for entry in logger.queryData(query):
            if self.terminate:
                break
            if len(entry) == 1:
                seq = [x for x in bytearray.fromhex(entry[0])]
                DBGLOG(str(seq))
                serial.Tx(seq)
                packetinfo = dec.getMetaData(seq)
                #logger.logData('outgoing', packetinfo.getPacketName(), seq)
                self.emit(SIGNAL("sentpacket"))
                time.sleep(1)
        serial.close()

    def quit(self):
        # this bit is not thread safe. Make improvements later.
        self.terminate = True