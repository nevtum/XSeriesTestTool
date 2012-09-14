class AbstractItemDecoder:
    def __init__(self, params):
        assert(isinstance(params, dict))
        self.params = params

    def returnValue(self, packet):
        raise RuntimeError('Abstract method, must be overloaded!')

    def getByteArray(self, packet, lbound, hbound):
        return packet[int(hbound)-1:int(lbound)-2:-1]

    def getByteString(self, packet, lbound, hbound):
        arr = ['%02X' % x for x in self.getByteArray(packet, lbound, hbound)]
        return ''.join(arr)

    def getBit(self, byte, n):
        return ((byte >> n) & 0x1)

    def getstartendbyte(self):
        startbyte = self.params.get('startbyte')
        endbyte = self.params.get('endbyte')
        if not startbyte:
            startbyte = endbyte = self.params.get('byte')
        assert(startbyte)
        assert(endbyte)
        return startbyte, endbyte

class reverseIntegerDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte()
        return self.getByteString(packet, l, h)

class booleanDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        byte = int(self.params.get('byte'))
        bit = int(self.params.get('bit'))
        return self.getBit(packet[byte-1], bit)

class reverseCurrencyDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte()
        x = int(self.getByteString(packet, l, h))/100.00
        return '%.2f' % x

class reverseAsciiDecoder(AbstractItemDecoder):
    def returnValue(self, packet):
        l, h = self.getstartendbyte()
        x = [chr(val) for val in self.getByteArray(packet, l, h)]
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
    
    def diffXMLPacket(self, seq1, seq2):
        if seq1[:2] != seq2[:2]:
            return None
        xor = [a^b for a, b in zip(seq1, seq2)]
        meta = self.getMetaData(seq1)
        
        # really need to reduce coupling here
        x = "<packet name=\"%s\">\n" % meta.getPacketName()
        for item in meta.allItems():
            dec = self.__getTypeDecoder(item)
            params = item.extractParams()
            start, end = dec.getstartendbyte()
            if max(dec.getByteArray(xor, start, end)) > 0:
                tag = item.extract('name')
                value1 = dec.returnValue(seq1)
                value2 = dec.returnValue(seq2)
                x += "\t<%s>\n" % tag
                x += "\t\t<changeset old=\"%s\" new=\"%s\"\>\n" % (value2, value1)
                #x += " <%s>%s</%s>\n" % ("new", value2, "new")
                x += "\t</%s>\n" % tag
        x += "</packet>"
        print x
        return x

    def createXMLPacket(self, seq):
        assert(isinstance(seq, list))
        try:
            meta = self.getMetaData(seq)
            packetlength = meta.getPacketLength()
        except ValueError:
            return "no logic defined to decode packet"
        except IndexError:
            return "start of block is not 0xff"

        if(len(seq) != packetlength):
            return "corrupted packet"

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
            raise IndexError("Start of block is not 0xFF!!")
            #return self.repo.getMetaObject(None)
        return self.repo.getMetaObject(seq[1])
        
