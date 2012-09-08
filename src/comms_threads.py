import time
import Queue
from serial_app import SerialModule
from PyQt4.QtCore import QObject, QThread, SIGNAL
from debug import *

class MessageQueue(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.q = Queue.LifoQueue(10)

    def add(self, message):
        DBGLOG("MessageQueue: adding new message to queue")
        assert(message)
        self.q.put(message)
        DBGLOG("MessageQueue: finished adding message")
        self.emit(SIGNAL("receivedpacket"))

    def dequeue(self):
        item = self.q.get()
        return item

    def isEmpty(self):
        return self.q.empty()

class ListenThread(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.factory = parent.getFactory()
        self.terminate = False

    def setcommport(self, port):
        self.port = port

    def setbaud(self, baud):
        self.baud = int(baud)

    def run(self):
        dec = self.factory.getProtocolDecoder()

        # add a try/finally statement in the future
        serial = SerialModule(self.port, self.baud)
        queue = self.factory.getMessageQueue()
        self.terminate = False
        BUFFER = []
        DBGLOG("ListenThread: Serial thread started!")
        DBGLOG("ListenThread: port = %s, baud = %s" % (self.port, self.baud))
        while True:
            #DBGLOG("ListenThread: Awaiting packet...")
            if self.terminate:
                DBGLOG("ListenThread: Serial thread stopped!")
                break
            newbuffer = serial.Rx()
            if newbuffer:
                BUFFER += newbuffer
                #DBGLOG("ListenThread: Bytes: %s" % str(BUFFER))
            while len(BUFFER) > 0:
                try:
                    packetinfo = dec.getMetaData(BUFFER)
                    expectedlength = packetinfo.getPacketLength()
                except ValueError:
                    DBGLOG("ListenThread: length is zero")

                if packetinfo.getPacketName() == "unknown":
                    DBGLOG("ListenThread: Unknown packet received")
                    queue.add(BUFFER[:])
                    BUFFER = []
                    break
                elif len(BUFFER) < expectedlength:
                    DBGLOG("ListenThread: packet length smaller than expected length")
                    DBGLOG("ListenThread: expected = %i, actual = %i" % (expectedlength, len(BUFFER)))
                    break
                elif len(BUFFER) > expectedlength:
                    DBGLOG("ListenThread: packet length larger than expected length")
                    DBGLOG("ListenThread: expected = %i, actual = %i" % (expectedlength, len(BUFFER)))
                    queue.add(BUFFER[:expectedlength])
                    BUFFER = BUFFER[expectedlength:]
                    break
                else:
                    DBGLOG("ListenThread: length matches")
                    queue.add(BUFFER[:])
                    BUFFER = []

                DBGLOG("ListenThread: TYPE = %s" % packetinfo.getPacketName())
        serial.close()

    def quit(self):
        # this bit is not thread safe. Make improvements later.
        self.terminate = True

class ReplayThread(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.factory = parent.getFactory()
        self.terminate = False

    def setcommport(self, port):
        self.port = port

    def setbaud(self, baud):
        self.baud = int(baud)

    def run(self):
        DBGLOG("replaying data")
        wrapper = self.factory.getQtSQLWrapper()
        serial = SerialModule(self.port, self.baud)
        queue = self.factory.getMessageQueue()
        query = "SELECT hex FROM packetlog where direction ='incoming' ORDER BY timestamp ASC LIMIT 100"
        for entry in wrapper.runQuery(query):
            if self.terminate:
                break
            if len(entry) == 1:
                seq = [x for x in bytearray.fromhex(entry[0])]
                DBGLOG(str(seq))
                serial.Tx(seq)
                queue.add(seq)
                time.sleep(1)
        serial.close()

    def quit(self):
        # this bit is not thread safe. Make improvements later.
        self.terminate = True