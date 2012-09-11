from config.configmanager import metaRepository
from decoder import *
from views import QtSQLWrapper

class TransmissionFactory:
    def __init__(self):
        self.xdec = None
        self.sqlwrapper = None

    def getProtocolDecoder(self):
        if self.xdec == None:
            xmetadata = metaRepository('settings/')
            self.xdec = XProtocolDecoder(xmetadata)
            self.xdec.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
            self.xdec.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
            self.xdec.registerTypeDecoder('boolean', booleanDecoder)
            self.xdec.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)
        return self.xdec
    
    def getQtSQLWrapper(self):
        if self.sqlwrapper == None:
            self.sqlwrapper = QtSQLWrapper("test.db")
        return self.sqlwrapper