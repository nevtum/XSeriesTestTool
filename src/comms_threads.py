import timefrom decoder import *from PyQt4.QtCore import QThread, SIGNALclass ListenThread(QThread):    def __init__(self, parent):        QThread.__init__(self, parent)        self.factory = parent.factory        self.stopped = False    def setcommport(self, port):        self.port = port    def setbaud(self, baud):        self.baud = int(baud)    def run(self):        dec = self.factory.getProtocolDecoder()        logger = self.factory.getDataLogger('test.db')        serial = self.factory.getSerialModule(self.port, self.baud)        self.stopped = False        BUFFER = []        DBGLOG("Serial thread started!")        DBGLOG("port = %s, baud = %s" % (self.port, self.baud))        while True:            DBGLOG("Awaiting packet...")            if self.stopped:                DBGLOG("Serial thread stopped!")                break            newbuffer = serial.Rx()            if newbuffer:                BUFFER += newbuffer                DBGLOG(str(BUFFER))            while len(BUFFER) > 0:                packetinfo = dec.getMetaData(BUFFER)                if packetinfo.getPacketName() == "unknown":                    packet = BUFFER                    BUFFER = []                    break                expectedlength = packetinfo.getPacketLength()                if expectedlength == 0:                    break                if  len(BUFFER) > expectedlength:                    DBGLOG("packet length larger than expected length")                    DBGLOG('expected = %i, actual = %i' % (expectedlength, len(BUFFER)))                    packet = BUFFER[:expectedlength]                    BUFFER = BUFFER[expectedlength:]                    logger.logData('incoming', packetinfo.getPacketName(), packet)                    self.emit(SIGNAL("receivedpacket"))                elif len(BUFFER) < expectedlength:                    DBGLOG("packet length smaller than expected length")                    break                else:                    packet = BUFFER[:]                    BUFFER = []                    logger.logData('incoming', packetinfo.getPacketName(), packet)                    self.emit(SIGNAL("receivedpacket"))                DBGLOG(packetinfo.getPacketName())        serial.close()    def quit(self):        # this bit is not thread safe. Make improvements later.        self.stopped = Trueclass ReplayThread(QThread):    def __init__(self, parent):        QThread.__init__(self, parent)        self.factory = parent.factory        self.stopped = False    def setcommport(self, port):        self.port = port    def setbaud(self, baud):        self.baud = int(baud)    def run(self):        DBGLOG("replaying data")        dec = self.factory.getProtocolDecoder()        logger = self.factory.getDataLogger('test.db')        serial = self.factory.getSerialModule(self.port, self.baud)        query = "SELECT hex FROM packetlog where direction ='incoming' ORDER BY timestamp ASC LIMIT 100"        for entry in logger.queryData(query):            if self.stopped:                return            if len(entry) == 1:                DBGLOG(entry[0])                seq = [x for x in bytearray.fromhex(entry[0])]                serial.Tx(seq)                packetinfo = dec.getMetaData(seq)                logger.logData('outgoing', packetinfo.getPacketName(), seq)                self.emit(SIGNAL("sentpacket"))                time.sleep(1)                    def quit(self):        # this bit is not thread safe. Make improvements later.        self.stopped = True