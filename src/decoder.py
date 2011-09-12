from config.metaclasses import codecMetaObject

class reverseIntegerDecoder:
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def getstartendbyte(self, params):
        startbyte = params.get('startbyte')
        endbyte = params.get('endbyte')
        if not startbyte:
            startbyte = endbyte = params.get('byte')
        return startbyte, endbyte
        
    def returnValue(self):
        l, h = self.getstartendbyte(self.params)
        return self.getByteString(l, h)
    
    def getByteVector(self, lbound, hbound):
        return self.packet[int(hbound)-1:int(lbound)-2:-1]
            
    def getByteString(self, lbound, hbound):
        return ''.join(self.getByteVector(lbound, hbound))
    
class booleanDecoder:
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def returnValue(self):
        byte = int(self.params.get('byte'))
        bit = int(self.params.get('bit'))
        return self.getBit(int(self.packet[byte-1], 16), bit)
    
    def getBit(self, byte, n):
        return ((byte >> n) & 0x1)
    
class reverseCurrencyDecoder:
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def getstartendbyte(self, params):
        startbyte = params.get('startbyte')
        endbyte = params.get('endbyte')
        if not startbyte:
            startbyte = endbyte = params.get('byte')
        return startbyte, endbyte
        
    def returnValue(self):
        l, h = self.getstartendbyte(self.params)
        x = int(self.getByteString(l, h))/100.00
        return '%.2f' % x

    def getByteVector(self, lbound, hbound):
        return self.packet[int(hbound)-1:int(lbound)-2:-1]
            
    def getByteString(self, lbound, hbound):
        return ''.join(self.getByteVector(lbound, hbound))
    
class reverseAsciiDecoder:
    def __init__(self, packet, params):
        self.packet = packet
        self.params = params
        
    def getstartendbyte(self, params):
        startbyte = params.get('startbyte')
        endbyte = params.get('endbyte')
        if not startbyte:
            startbyte = endbyte = params.get('byte')
        return startbyte, endbyte
        
    def returnValue(self):
        l, h = self.getstartendbyte(self.params)
        x = [chr(int(val, 16)) for val in self.getByteVector(l, h)]
        chars = ''.join(x).strip()
        if chars == '':
            return 'None'
        return chars
            
    def getByteVector(self, lbound, hbound):
        return self.packet[int(hbound)-1:int(lbound)-2:-1]
        
class packetConverter(object):
    def __init__(self):
        self.packet = []

    def getMeta(self, name):
        return codecMetaObject('packetdef.xml')

    def setpacket(self, packet):
        self.packet = packet
        id = self.readpacketheader()
        self.meta = self.getMeta(id)
        
    def readpacketheader(self):
        pass
        
    def createXMLPacket(self):
        metaobj = self.meta
        assert(len(self.packet) == metaobj.getPacketLength())
        print "<packet name=\"%s\">" % metaobj.getPacketName()
        for item in metaobj.allItems():
            name = item.extract('name')
            type = item.extract('type')
            params = item.extractParams()
            value = self.decode(type, params)
            print "\t<%s>%s</%s>" % (name, value, name)
        print "</packet>"

    def decode(self, type, params):
        if type == 'integer-reverse':
            return reverseIntegerDecoder(self.packet, params).returnValue()
        elif type == 'currency-reverse':
            return reverseCurrencyDecoder(self.packet, params).returnValue()
        elif type == 'boolean':
            return booleanDecoder(self.packet, params).returnValue()
        elif type == 'ascii-reverse':
            return reverseAsciiDecoder(self.packet, params).returnValue()
        else:
            return 'unknown'

from generators import *

file = open('SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t') # filter out given characters
b = charpacket(a, size = 2) # number of characters to extract from stream
c = datablockdispatcher(b) # extract only standard XSeries Packets
d = datablockfilter(c, '00') # select packets that match packet IDs
   
converter = packetConverter()
for packet in d:
    converter.setpacket(packet)
    converter.createXMLPacket()