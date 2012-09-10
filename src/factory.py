from comms_threads import MessageQueue
from config.configmanager import metaRepository
from decoder import *
from views import Publisher, QtSQLWrapper

class TransmissionFactory:
    def __init__(self):
        self.xdec = None
        self.messagequeue = None
        self.publisher = None
        self.sqlwrapper = None

    def getMessageQueue(self):
        if self.messagequeue == None:
            self.messagequeue = MessageQueue()
        return self.messagequeue

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