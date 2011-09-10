from config.metaclasses import codecMetaObject

class decoder(object):
    def __init__(self):
        self.packet = []

    def getMeta(self, name):
        return codecMetaObject('packetdef.xml')

    def setpacket(self, packet):
        self.packet = packet
        
    def readpacketheader(self):
        pass
        
    def createXMLPacket(self):
        # if sdb packet
        metaobj = self.getMeta('sdb') # need more parameters
        assert(len(self.packet) == metaobj.getPacketLength())
        print "<packet name=\"%s\">" % metaobj.getPacketName()
        for item in metaobj.allItems():
            name = item.extract('name')
            type = item.extract('type')
            params = item.extractParams()
            value = self.decode(type, params)
            print "\t<%s>%s</%s>" % (name, value, name)
        print "</packet>"
        
    def getstartendbyte(self, params):
        startbyte = params.get('startbyte')
        endbyte = params.get('endbyte')
        if not startbyte:
            startbyte = endbyte = params.get('byte')
        return startbyte, endbyte

    def decode(self, type, params):
        #delegate to type class
        #use polymorphism
        if type == 'integer-reverse':
            l, h = self.getstartendbyte(params)
            return self.getByteString(l, h)
        elif type == 'currency-reverse':
            l, h = self.getstartendbyte(params)
            x = int(self.getByteString(l, h))/100.00
            return '%.2f' % x
        elif type == 'boolean':
            byte = int(params.get('byte'))
            bit = int(params.get('bit'))
            return self.getBit(int(self.packet[byte-1], 16), bit)
        else:
            return 'unknown'

    def getBit(self, byte, n):
        return ((byte >> n) & 0x1)

    def getByteVector(self, lbound, hbound):
        return self.packet[int(hbound)-1:int(lbound)-2:-1]
            
    def getByteString(self, lbound, hbound):
        return ''.join(self.getByteVector(lbound, hbound))


from generators import *

file = open('SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t') # filter out given characters
b = charpacket(a, size = 2) # number of characters to extract from stream
c = datablockdispatcher(b) # extract only standard XSeries Packets
d = datablockfilter(c, '00') # select packets that match packet IDs
   
XDecoder = decoder()
for packet in d:
    XDecoder.setpacket(packet)
    XDecoder.createXMLPacket()