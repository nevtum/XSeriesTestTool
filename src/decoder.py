from config.metaclasses import codecMetaObject

class AbstractXDecoder:
    def returnValue(self):
        raise RuntimeError('Abstract method, must be overloaded!')
    
    def getByteVector(self, packet, lbound, hbound):
        return packet[int(hbound)-1:int(lbound)-2:-1]
            
    def getByteString(self, packet, lbound, hbound):
        return ''.join(self.getByteVector(packet, lbound, hbound))
    
    def getBit(self, byte, n):
        return ((byte >> n) & 0x1)
    
    def getstartendbyte(self, params):
        startbyte = params.get('startbyte')
        endbyte = params.get('endbyte')
        if not startbyte:
            startbyte = endbyte = params.get('byte')
        return startbyte, endbyte

class reverseIntegerDecoder(AbstractXDecoder):
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def returnValue(self):
        l, h = self.getstartendbyte(self.params)
        return self.getByteString(self.packet, l, h)
    
class booleanDecoder(AbstractXDecoder):
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def returnValue(self):
        byte = int(self.params.get('byte'))
        bit = int(self.params.get('bit'))
        return self.getBit(int(self.packet[byte-1], 16), bit)
    
class reverseCurrencyDecoder(AbstractXDecoder):
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def returnValue(self):
        l, h = self.getstartendbyte(self.params)
        x = int(self.getByteString(self.packet, l, h))/100.00
        return '%.2f' % x
    
class reverseAsciiDecoder(AbstractXDecoder):
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

class IDecoder:
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
        raise RuntimeError('Abstract method, must be overloaded!')

class XProtocolConverter(IDecoder):
    def __init__(self):
        self.decoderfactory = {}
        self.decoderfactory['integer-reverse'] = reverseIntegerDecoder
        self.decoderfactory['currency-reverse'] = reverseCurrencyDecoder
        self.decoderfactory['boolean'] = booleanDecoder
        self.decoderfactory['ascii-reverse'] = reverseAsciiDecoder

    def getMeta(self, packet):
        assert(packet)
        id = packet[1]
        if id == '00':
            return codecMetaObject('packetdef.xml')
        else:
            return None

    def decode(self, packet, type, params):
        dec = self.decoderfactory.get(type)(packet, params)
        return dec.returnValue()

from generators import *

file = open('SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t') # filter out given characters
b = charpacket(a, size = 2) # number of characters to extract from stream
c = datablockdispatcher(b) # extract only standard XSeries Packets
d = datablockfilter(c, '00') # select packets that match packet IDs
   
converter = XProtocolConverter()
for packet in d:
    converter.createXMLPacket(packet)