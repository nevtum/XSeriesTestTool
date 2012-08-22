import timefrom decoder import *from PyQt4.QtCore import QThread, SIGNALclass DuplicateDatablockFilter:    def __init__(self, default = False):        self.dupes = {}        assert(isinstance(default, bool))        self.filterduplicates(default)    def filterduplicates(self, toggle):        assert(isinstance(toggle, bool))        self.filtered = toggle    def differentToPrevious(self, blocktype, seq):        if not self.filtered:            return True        key = blocktype        data = self.dupes.get(key)        if data is None:            DBGLOG("NEW DATABLOCK!")            self.dupes[key] = seq            return True        assert(len(seq) == len(data))        for i in range(len(seq)):            if seq[i] != data[i]:                self.dupes[key] = seq                assert(seq == self.dupes.get(key))                DBGLOG("DIFFERENT DATABLOCK!")                return True        DBGLOG("REPEATED!")        return Falseclass ListenThread(QThread):    def __init__(self, parent):        QThread.__init__(self, parent)        self.factory = parent.factory        self.filter = DuplicateDatablockFilter(False)        self.terminate = False    def setcommport(self, port):        self.port = port    def setbaud(self, baud):        self.baud = int(baud)            def filterduplicates(self, toggle):        assert(isinstance(toggle, bool))        DBGLOG("Listener Thread: ignoring duplicate datablocks = %s" % toggle)        self.filter.filterduplicates(toggle)    def run(self):        dec = self.factory.getProtocolDecoder()        logger = self.factory.getDataLogger('test.db')        serial = self.factory.getSerialModule(self.port, self.baud)        self.terminate = False        BUFFER = []        DBGLOG("Serial thread started!")        DBGLOG("port = %s, baud = %s" % (self.port, self.baud))        while True:            DBGLOG("Awaiting packet...")            if self.terminate:                DBGLOG("Serial thread stopped!")                break            newbuffer = serial.Rx()            if newbuffer:                BUFFER += newbuffer                DBGLOG("Bytes: %s" % str(BUFFER))            while len(BUFFER) > 0:                packetinfo = dec.getMetaData(BUFFER)                if packetinfo.getPacketName() == "unknown":                    packet = BUFFER                    BUFFER = []                    break                expectedlength = packetinfo.getPacketLength()                if expectedlength == 0:                    break                if  len(BUFFER) > expectedlength:                    DBGLOG("packet length larger than expected length")                    DBGLOG('expected = %i, actual = %i' % (expectedlength, len(BUFFER)))                    packet = BUFFER[:expectedlength]                    BUFFER = BUFFER[expectedlength:]                    if self.filter.differentToPrevious(packetinfo.getPacketName(), packet):                        logger.logData('incoming', packetinfo.getPacketName(), packet)                    self.emit(SIGNAL("receivedpacket"))                elif len(BUFFER) < expectedlength:                    DBGLOG("packet length smaller than expected length")                    break                else:                    packet = BUFFER[:]                    BUFFER = []                    if self.filter.differentToPrevious(packetinfo.getPacketName(), packet):                        logger.logData('incoming', packetinfo.getPacketName(), packet)                    self.emit(SIGNAL("receivedpacket"))                DBGLOG("TYPE: %s" % packetinfo.getPacketName())        serial.close()    def quit(self):        # this bit is not thread safe. Make improvements later.        self.terminate = Trueclass ReplayThread(QThread):    def __init__(self, parent):        QThread.__init__(self, parent)        self.factory = parent.factory        self.terminate = False    def setcommport(self, port):        self.port = port    def setbaud(self, baud):        self.baud = int(baud)    def run(self):        DBGLOG("replaying data")        dec = self.factory.getProtocolDecoder()        logger = self.factory.getDataLogger('test.db')        serial = self.factory.getSerialModule(self.port, self.baud)        query = "SELECT hex FROM packetlog where direction ='incoming' ORDER BY timestamp ASC LIMIT 100"        for entry in logger.queryData(query):            if self.terminate:                return            if len(entry) == 1:                DBGLOG(entry[0])                seq = [x for x in bytearray.fromhex(entry[0])]                serial.Tx(seq)                packetinfo = dec.getMetaData(seq)                logger.logData('outgoing', packetinfo.getPacketName(), seq)                self.emit(SIGNAL("sentpacket"))                time.sleep(1)                    def quit(self):        # this bit is not thread safe. Make improvements later.        self.terminate = True