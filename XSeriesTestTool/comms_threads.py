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
import debug
from serial_app import SerialModule
from PyQt4.QtCore import QObject, QThread, SIGNAL

class ListenThread(QThread):
    def __init__(self, decoder, publisher, parent = None):
        QThread.__init__(self, parent)
        self.decoder = decoder
        self.publisher = publisher
        self.terminate = False

    def setcommport(self, port):
        self.port = port

    def setbaud(self, baud):
        self.baud = int(baud)

    def run(self):
        # add a try/finally statement in the future
        serial = SerialModule(self.port, self.baud)
        self.terminate = False
        BUFFER = []
        debug.Log("ListenThread: Serial thread started!")
        debug.Log("ListenThread: port = %s, baud = %s" % (self.port, self.baud))
        while True:
            debug.Log("ListenThread: Awaiting packet...")
            if self.terminate:
                debug.Log("ListenThread: Serial thread stopped!")
                break
            newbuffer = serial.Rx()
            if newbuffer:
                BUFFER += newbuffer
                debug.Log("ListenThread: Bytes: %s" % str(BUFFER))
            while len(BUFFER) > 0:
                try:
                    packet_info = self.decoder.get_data_definition(BUFFER)
                    expectedlength = packet_info.getPacketLength()
                    
                    packet_type = packet_info.getPacketName()
                    if packet_type == "unknown":
                        self.notify_unknown_packet_received(BUFFER[:])
                        BUFFER = []
                        break
                    elif 0 < len(BUFFER) < expectedlength:
                        self.notify_unexpected_length(packet_info, BUFFER)
                        break
                    elif len(BUFFER) >= expectedlength:
                        self.notify_packet_received(packet_type, BUFFER[:expectedlength])
                        BUFFER = BUFFER[expectedlength:]
                    else:
                        pass
                        
                except ValueError:
                    debug.Log("ListenThread: length is zero")
                except AssertionError:
                    debug.Log("ListenThread: packet not large enough to determine SOB")
                except IndexError:
                    debug.Log("ListenThread: BUFFER Start of block not 0xFF. Clearing BUFFER!")
                    BUFFER = []

        serial.close()
    
    def notify_unexpected_length(self, packet_info, data):
        debug.Log("ListenThread: packet length smaller than expected length")
        debug.Log("ListenThread: expected = %i, actual = %i" % (packet_info.getPacketLength(), len(data)))
        self.publisher.notify_unexpected_length(packet_info, data)
        
    def notify_packet_received(self, packet_type, data):
        self.publisher.notify_packet_received(packet_type, data)
    
    def notify_unknown_packet_received(self, data):
        debug.Log("ListenThread: Unknown packet type")
        self.publisher.notify_unknown_packet_received(data)

    def quit(self):
        # this bit is not thread safe. Make improvements later.
        self.terminate = True
    
    def __del__(self):
        self.terminate()
        self.wait()