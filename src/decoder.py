from config.metaclasses import codecMetaObject
from config.configmanager import metaRepository
from xml.etree import cElementTree

class AbstractItemDecoder:
    def returnValue(self):
        raise RuntimeError('Abstract method, must be overloaded!')
    
    def getByteVector(self, packet, lbound, hbound):
        return packet[int(hbound)-1:int(lbound)-2:-1]
            
    def getByteString(self, packet, lbound, hbound):
        return ''.join(self.getByteVector(packet, lbound, hbound))
    
    def getBit(self, byte, n):
        return ((byte >> n) & 0x1)
    
    def getstartendbyte(self, params):
        assert(isinstance(params, dict))
        startbyte = params.get('startbyte')
        endbyte = params.get('endbyte')
        if not startbyte:
            startbyte = endbyte = params.get('byte')
        return startbyte, endbyte

class reverseIntegerDecoder(AbstractItemDecoder):
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def returnValue(self):
        l, h = self.getstartendbyte(self.params)
        return self.getByteString(self.packet, l, h)
    
class booleanDecoder(AbstractItemDecoder):
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def returnValue(self):
        byte = int(self.params.get('byte'))
        bit = int(self.params.get('bit'))
        return self.getBit(int(self.packet[byte-1], 16), bit)
    
class reverseCurrencyDecoder(AbstractItemDecoder):
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def returnValue(self):
        l, h = self.getstartendbyte(self.params)
        x = int(self.getByteString(self.packet, l, h))/100.00
        return '%.2f' % x
    
class reverseAsciiDecoder(AbstractItemDecoder):
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def returnValue(self):
        l, h = self.getstartendbyte(self.params)
        x = [chr(int(val, 16)) for val in self.getByteVector(self.packet, l, h)]
        chars = ''.join(x).strip()
        if chars == '':
            return 'None'
        return chars
    
class nullDecoder(AbstractItemDecoder):
    def __init__(self, packet, params):
        pass
    
    def returnValue(self):
        return 'unknown decoding type'

class IDecoder:
    def __init__(self):
        self.repo = metaRepository('settings/')
        self.decoderfactory = {}
        
    def registerTypeDecoder(self, key, constructor):
        assert(isinstance(key, str))
        assert(issubclass(constructor, AbstractItemDecoder))
        self.decoderfactory[key] = constructor
    
    def getConcreteDecoder(self, type):
        dec = self.decoderfactory.get(type)
        if dec is None:
            return nullDecoder
        return dec
    
    def createXMLPacket(self, packet):
        metaobj = self.getMeta(packet)
        assert(len(packet) == metaobj.getPacketLength())
        print "<packet name=\"%s\">" % metaobj.getPacketName()
        for item in metaobj.allItems():
            name = item.extract('name')
            type = item.extract('type')
            params = item.extractParams()
            value = self.decode(packet, type, params)
            print "\t<%s>%s</%s>" % (name, value, name)
        print "</packet>"
    
    def getMeta(self, packet):
        raise RuntimeError('Abstract method, must be overloaded!')
    
    def decode(self, packet, type, params):
        dec = self.getConcreteDecoder(type)(packet, params)
        return dec.returnValue()

class XProtocolDecoder(IDecoder):
    def getMeta(self, packet):
        assert(packet)
        id = packet[1]
        return self.repo.getMetaObject(id)

from generators import *

file = open('unittests/SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t') # filter out given characters
b = charpacket(a, size = 2) # number of characters to extract from stream
c = datablockdispatcher(b) # extract only standard XSeries Packets
d = datablockfilter(c, '22') # select packets that match packet IDs
   
xdec = XProtocolDecoder()
xdec.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
xdec.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
xdec.registerTypeDecoder('boolean', booleanDecoder)
xdec.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)


for packet in d:
    xdec.createXMLPacket(packet)