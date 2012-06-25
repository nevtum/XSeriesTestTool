from config.configmanager import metaRepository
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
    
    def createXMLPacket(self, seq):
        # split up sequence in equal sized chunks of 2 characters (nibbles)
        assert(isinstance(seq, str))
        packet = [seq[i:i+2] for i in range(0, len(seq), 2)]
        meta = self.getMetaData(packet)
        if meta.getPacketLength() != 0:
            assert(len(packet) == meta.getPacketLength())
        x = "<packet name=\"%s\">\n" % meta.getPacketName()
        for item in meta.allItems():
            dec = self.getTypeDecoder(item)
            value = dec.returnValue(packet)
            tag = item.extract('name')
            x += "\t<%s>%s</%s>\n" % (tag, value, tag)
        x += "</packet>"
        return x
        
        self.logger.logData("incoming", meta.getPacketName(), "".join(packet))
    
    def getMetaData(self, packet):
        raise RuntimeError('Abstract method, must be overloaded!')

class XProtocolDecoder(IDecoder):
    def getMetaData(self, packet):
        assert(packet)
        if(len(packet) >= 2):
            if(packet[0] == 'FF'):
                return self.repo.getMetaObject(packet[1])
        return self.repo.getMetaObject(None)

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
