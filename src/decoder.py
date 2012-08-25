from config.configmanager import metaRepository
import sqlite3
from datetime import datetime
from serial_app import *

class DuplicateDatablockFilter:
    def __init__(self, default = False):
        self.dupes = {}
        assert(isinstance(default, bool))
        self.filterduplicates(default)

    def filterduplicates(self, toggle):
        assert(isinstance(toggle, bool))
        self.filtered = toggle
        DBGLOG("Filtering enabled = %s" % toggle)

    def differentToPrevious(self, blocktype, seq):
        if not self.filtered:
            return True

        key = blocktype
        data = self.dupes.get(key)
        if data is None:
            DBGLOG("NEW DATABLOCK!")
            self.dupes[key] = seq
            return True

        assert(len(seq) == len(data))
        for i in range(len(seq)):
            if seq[i] != data[i]:
                self.dupes[key] = seq
                assert(seq == self.dupes.get(key))
                DBGLOG("DIFFERENT DATABLOCK!")
                return True
        DBGLOG("REPEATED!")
        return False

class TransmissionFactory:
    def __init__(self):
        self.xdec = None
        self.dupesfilter = None

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
        if self.dupesfilter == None:
            self.dupesfilter = DuplicateDatablockFilter(False)
        return self.dupesfilter

    def getSerialModule(self, port, baudrate):
        return SerialModule(port, baudrate)

class AbstractItemDecoder:
    def __init__(self, params):
        self.params = params

    def returnValue(self, packet):
        raise RuntimeError('Abstract method, must be overloaded!')

    def getByteVector(self, packet, lbound, hbound):
        return packet[int(hbound)-1:int(lbound)-2:-1]

    def getByteString(self, packet, lbound, hbound):
        arr = ['%02X' % x for x in self.getByteVector(packet, lbound, hbound)]
        return ''.join(arr)

    def getBit(self, byte, n):
        return ((byte >> n) & 0x1)

    def getstartendbyte(self, params):
        assert(isinstance(params, dict))
        startbyte = params.get('startbyte')
        endbyte = params.get('endbyte')
        if not startbyte:
            startbyte = endbyte = params.get('byte')
        assert(startbyte)
        assert(endbyte)
        return startbyte, endbyte

class reverseIntegerDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte(self.params)
        return self.getByteString(packet, l, h)

class booleanDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        byte = int(self.params.get('byte'))
        bit = int(self.params.get('bit'))
        return self.getBit(packet[byte-1], bit)

class reverseCurrencyDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte(self.params)
        x = int(self.getByteString(packet, l, h))/100.00
        return '%.2f' % x

class reverseAsciiDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte(self.params)
        x = [chr(val) for val in self.getByteVector(packet, l, h)]
        chars = ''.join(x).strip()
        if chars == '':
            return 'None'
        return chars

class nullDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        return 'unknown decoding type'

class IDecoder:
    def __init__(self, repo):
        self.repo = repo
        self.decoderfactory = {}
        
    def registerTypeDecoder(self, key, constructor):
        assert(isinstance(key, str))
        assert(issubclass(constructor, AbstractItemDecoder))
        self.decoderfactory[key] = constructor

    def __getTypeDecoder(self, item):
        type = item.extract('type')
        params = item.extractParams()
        dec = self.decoderfactory.get(type)(params)
        if dec is None:
            return nullDecoder
        return dec

    def createXMLPacket(self, seq):
        assert(isinstance(seq, list))
        meta = self.getMetaData(seq)
        if meta.getPacketLength() == 0:
            return "Empty packet"
        if(len(seq) != meta.getPacketLength()):
            return "invalid packet"

        x = "<packet name=\"%s\">\n" % meta.getPacketName()
        for item in meta.allItems():
            dec = self.__getTypeDecoder(item)
            value = dec.returnValue(seq)
            tag = item.extract('name')
            x += "\t<%s>%s</%s>\n" % (tag, value, tag)
        x += "</packet>"
        return x

    def getMetaData(self, packet):
        raise RuntimeError('Abstract method, must be overloaded!')

class XProtocolDecoder(IDecoder):
    def getMetaData(self, seq):
        assert(len(seq) >= 2)
        if(seq[0] != 0xFF):
            return self.repo.getMetaObject(None)
        return self.repo.getMetaObject(seq[1])

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
        self.duplicates = {}

    def logData(self, direction, packetid, seq):
        assert(isinstance(seq, list))
        data = ''.join(["%02X" % byte for byte in seq])
        if(direction not in ('incoming', 'outgoing')):
            raise ValueError()
        cursor = self.con.cursor()
        params = (str(datetime.now()), direction, packetid, data)
        sql = "INSERT INTO packetlog VALUES('%s','%s','%s','%s')" % params
        cursor.execute(sql)
        self.con.commit()

    def queryData(self, query):
        assert(isinstance(query, str))
        cursor = self.con.cursor()
        return cursor.execute(query)
        
