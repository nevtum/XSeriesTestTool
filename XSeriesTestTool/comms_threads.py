"""
XSeriesTestTool - A NSW gaming protocol decoder/analyzer
    Copyright (C) 2012  Neville Tummon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time
from serial_app import SerialModule
from PyQt4.QtCore import QObject, QThread, SIGNAL
from debug import *

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
        db = self.factory.getQtSQLWrapper()
        dec = self.factory.getProtocolDecoder()

        # add a try/finally statement in the future
        serial = SerialModule(self.port, self.baud)
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
                except AssertionError:
                    DBGLOG("ListenThread: packet not large enough to determine SOB")

                type = packetinfo.getPacketName()
                if type == "unknown":
                    DBGLOG("ListenThread: Unknown packet type")
                    #queue.add(BUFFER[:])
                    db.addRecord("incoming", type, BUFFER[:])
                    BUFFER = []
                    break
                elif 0 < len(BUFFER) < expectedlength:
                    DBGLOG("ListenThread: packet length smaller than expected length")
                    DBGLOG("ListenThread: expected = %i, actual = %i" % (expectedlength, len(BUFFER)))
                    break
                elif len(BUFFER) >= expectedlength:
                    DBGLOG("ListenThread: expected = %i, actual = %i" % (expectedlength, len(BUFFER)))
                    #queue.add(BUFFER[:expectedlength])
                    db.addRecord("incoming", type, BUFFER[:expectedlength])
                    BUFFER = BUFFER[expectedlength:]
                else:
                    raise AssertionError('Code should never reach here')

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
        self.terminate = False
        DBGLOG("replaying data")
        db = self.factory.getQtSQLWrapper()
        dec = self.factory.getProtocolDecoder()
        serial = SerialModule(self.port, self.baud)
        query = "SELECT hex FROM packetlog where direction ='incoming' ORDER BY timestamp ASC LIMIT 100"
        for entry in db.runSelectQuery(query):
            if self.terminate:
                break
            seq = [x for x in bytearray.fromhex(entry)]
            packetinfo = dec.getMetaData(seq)
            DBGLOG(str(seq))
            serial.Tx(seq)
            db.addRecord("outgoing", packetinfo.getPacketName(), seq)
            time.sleep(1)
        serial.close()
        self.emit(SIGNAL("TxComplete"))

    def quit(self):
        # this bit is not thread safe. Make improvements later.
        self.terminate = True
