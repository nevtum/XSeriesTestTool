from config.configmanager import metaRepository
from decoder import *
from views import QtSQLWrapper
from comms_threads import ListenThread
from notifications import Publisher

class TransmissionFactory:
    def __init__(self, parent):
        self.publisher = Publisher()
        self.xdec = self._build_protocol_decoder()
        self.sqlwrapper = QtSQLWrapper("test.db", self.publisher, parent)
        self.serial_thread = ListenThread(self.xdec, self.publisher, parent)
    
    def _build_protocol_decoder(self):
        xmetadata = metaRepository('settings/')
        decoder = XProtocolDecoder(xmetadata)
        decoder.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
        decoder.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
        decoder.registerTypeDecoder('boolean', booleanDecoder)
        decoder.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)
        return decoder

    def getProtocolDecoder(self):
        return self.xdec
    
    def getQtSQLWrapper(self):
        return self.sqlwrapper
    
    def get_serial_thread(self):
        return self.serial_thread
    
    def get_publisher(self):
        return self.publisher