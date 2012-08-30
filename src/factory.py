from serial_app import SerialModule
from config.configmanager import metaRepository
from decoder import *
from views import *

class TransmissionFactory:
    def __init__(self):
        self.xdec = None
        self.dupesfilter = None
        
        # code to remove when all connections
        # established in gui layer
        self.publisher = Publisher()
        self.dupesfilter = DuplicateDatablockFilter(self.publisher)
    
    def getPublisher(self):
        #if self.publisher == None:
        #    self.publisher = Publisher()
        return self.publisher

    def getProtocolDecoder(self):
        if self.xdec == None:
            xmetadata = metaRepository('settings/')
            self.xdec = XProtocolDecoder(xmetadata)
            self.xdec.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
            self.xdec.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
            self.xdec.registerTypeDecoder('boolean', booleanDecoder)
            self.xdec.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)
        return self.xdec

    def getDataLogger(self, filename):
        return DataLogger(filename)

    def getDuplicateDatablockFilter(self):
        #if self.dupesfilter == None:
        #    self.dupesfilter = DuplicateDatablockFilter()
        return self.dupesfilter

    def getSerialModule(self, port, baudrate):
        return SerialModule(port, baudrate)