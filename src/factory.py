from comms_threads import MessageQueue
from config.configmanager import metaRepository
from decoder import *
from views import Publisher

class TransmissionFactory:
    def __init__(self):
        self.xdec = None
        self.messagequeue = None
        self.publisher = None

    def getMessageQueue(self):
        if self.messagequeue == None:
            self.messagequeue = MessageQueue()
        return self.messagequeue
    
    def getPublisher(self):
        if self.publisher == None:
            self.publisher = Publisher()
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