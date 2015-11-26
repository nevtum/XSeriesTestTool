import time
import debug
from serial_app import SerialModule
from PyQt4.QtCore import QObject, QThread, SIGNAL
from datetime import datetime
from xpacket import XPacket

class ListenThread(QThread):
    def __init__(self, factory, parent = None):
        QThread.__init__(self, parent)
        self.decoder = factory.getProtocolDecoder()
        self.publisher = factory.get_publisher()
        self.terminate = False
    
    def on_record_started(self, port):
        self.port = port
        self.baud = 9600
        self.start()
        
    def on_record_stopped(self):
        # this bit is not thread safe. Make improvements later.
        self.terminate = True

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
                    BUFFER = []
                except AssertionError:
                    debug.Log("ListenThread: packet not large enough to determine SOB")
                    BUFFER = []
                except IndexError:
                    debug.Log("ListenThread: BUFFER Start of block not 0xFF. Clearing BUFFER!")
                    BUFFER = []

        serial.close()
    
    def notify_unexpected_length(self, packet_info, data):
        debug.Log("ListenThread: packet length smaller than expected length")
        debug.Log("ListenThread: expected = %i, actual = %i" % (packet_info.getPacketLength(), len(data)))
        self.publisher.notify_unexpected_length(packet_info, data)
        
    def notify_packet_received(self, packet_type, data):
        timestamp = str(datetime.now())
        packet = XPacket(timestamp, packet_type, data)
        self.publisher.notify_packet_received(packet)
    
    def notify_unknown_packet_received(self, data):
        debug.Log("ListenThread: Unknown packet type")
        self.publisher.notify_unknown_packet_received(data)
    
    def __del__(self):
        self.terminate()
        self.wait()