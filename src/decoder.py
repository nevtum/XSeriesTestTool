from config.metaclasses import codecMetaObject
from config.configmanager import metaRepository
from xml.etree import cElementTree
import sqlite3

class AbstractTypeDecoder:
    def __init__(self, params):
        self.params = params
        
    def returnValue(self, packet):
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

class reverseIntegerDecoder(AbstractTypeDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte(self.params)
        return self.getByteString(packet, l, h)
    
class booleanDecoder(AbstractTypeDecoder):
    def returnValue(self, packet):
        byte = int(self.params.get('byte'))
        bit = int(self.params.get('bit'))
        return self.getBit(int(packet[byte-1], 16), bit)
    
class reverseCurrencyDecoder(AbstractTypeDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte(self.params)
        x = int(self.getByteString(packet, l, h))/100.00
        return '%.2f' % x
    
class reverseAsciiDecoder(AbstractTypeDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte(self.params)
        x = [chr(int(val, 16)) for val in self.getByteVector(packet, l, h)]
        chars = ''.join(x).strip()
        if chars == '':
            return 'None'
        return chars
    
class nullDecoder(AbstractTypeDecoder):
    def returnValue(self, packet):
        return 'unknown decoding type'

class IDecoder:
    def __init__(self, repo):
        self.repo = repo
        self.decoderfactory = {}
        self.logger = DataLogger('test.db')
        
    def registerTypeDecoder(self, key, constructor):
        assert(isinstance(key, str))
        assert(issubclass(constructor, AbstractTypeDecoder))
        self.decoderfactory[key] = constructor
    
    def getTypeDecoder(self, item):
        type = item.extract('type')
        params = item.extractParams()
        dec = self.decoderfactory.get(type)(params)
        if dec is None:
            return nullDecoder
        return dec
    
    def createXMLPacket(self, packet):
        meta = self.getMetaData(packet)
        assert(len(packet) == meta.getPacketLength())
        print "<packet name=\"%s\">" % meta.getPacketName()
        for item in meta.allItems():
            dec = self.getTypeDecoder(item)
            value = dec.returnValue(packet)
            tag = item.extract('name')
            print "\t<%s>%s</%s>" % (tag, value, tag)
        print "</packet>"
        
        self.logger.logData("incoming", meta.getPacketName(), "".join(packet))
    
    def getMetaData(self, packet):
        raise RuntimeError('Abstract method, must be overloaded!')

class XProtocolDecoder(IDecoder):
    def getMetaData(self, packet):
        assert(packet)
        id = packet[1]
        return self.repo.getMetaObject(id)

class DataLogger:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename)
        cursor = self.con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS packetlog(
        timestamp DATETIME,
        direction TEXT NOT NULL,
        packetid TEXT NOT NULL,
        hex TEXT NOT NULL)"""
        cursor.execute(sql)
        self.con.commit()
        
    def logData(self, direction, packetid, data):
        if(direction not in ('incoming', 'outgoing')):
            raise ValueError()
        cursor = self.con.cursor()
        params = (direction, packetid, data)
        sql = "INSERT INTO packetlog VALUES(datetime(),'%s','%s','%s')" % params
        cursor.execute(sql)
        self.con.commit()

from generators import *

xmetadata = metaRepository('settings/')

file = open('unittests/SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t') # filter out given characters
b = charpacket(a, size = 2) # number of characters to extract from stream
c = datablockdispatcher(b) # extract only standard XSeries Packets
d = datablockfilter(c, '00', '22') # select packets that match packet IDs
   
xdec = XProtocolDecoder(xmetadata)
xdec.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
xdec.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
xdec.registerTypeDecoder('boolean', booleanDecoder)
xdec.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)


for packet in d:
    xdec.createXMLPacket(packet)
