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
        return int(''.join(arr))

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
    def isNonzero(self, packet):
        l, h = self.getstartendbyte()
        array = self.getByteArray(packet, l, h)
        return max(array) != 0

    def returnValue(self, packet):
        l, h = self.getstartendbyte()
        return self.getByteString(packet, l, h)

class booleanDecoder(AbstractItemDecoder):
    def isNonzero(self, packet):
        byte = int(self.params.get('byte'))
        bit = int(self.params.get('bit'))
        return self.getBit(packet[byte-1], bit) != 0

    def returnValue(self, packet):
        byte = int(self.params.get('byte'))
        bit = int(self.params.get('bit'))
        if self.getBit(packet[byte-1], bit):
            return "ON"
        else:
            return "OFF"

class reverseCurrencyDecoder(AbstractItemDecoder):
    def isNonzero(self, packet):
        l, h = self.getstartendbyte()
        array = self.getByteArray(packet, l, h)
        return max(array) != 0

    def returnValue(self, packet):
        l, h = self.getstartendbyte()
        x = int(self.getByteString(packet, l, h))/100.00
        return "${:,.2f}".format(x)

class reverseAsciiDecoder(AbstractItemDecoder):
    def isNonzero(self, packet):
        l, h = self.getstartendbyte()
        array = self.getByteArray(packet, l, h)
        return max(array) != 0

    def returnValue(self, packet):
        l, h = self.getstartendbyte()
        x = [chr(val) for val in self.getByteArray(packet, l, h)]
        chars = ''.join(x).strip()
        if chars == '':
            return 'None'
        return chars

class nullDecoder(AbstractItemDecoder):
    def isNonzero(self, packet):
        return False

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

    def getDecodedData(self, seq):
        assert(isinstance(seq, list))
        try:
            meta = self.getMetaData(seq)
            packetlength = meta.getPacketLength()
        except ValueError:
            return "unknown", [("no logic defined to decode packet", "")]
        except IndexError:
            return "unknown", [("start of block is not 0xff", "")]

        if(len(seq) != packetlength):
            return meta.getPacketName(), [("corrupted packet", "")]

        array = []

        for item in meta.allItems():
            dec = self.__getTypeDecoder(item)
            try:
                value = dec.returnValue(seq)
            except ValueError:
                value = "CORRUPTED"
            key = item.extract('name')
            array.append((key, value))

        return meta.getPacketName(), array

    def getDiffPackets(self, seq1, seq2):
        try:
            meta1 = self.getMetaData(seq1)
            meta2 = self.getMetaData(seq2)
        except IndexError:
            return "Cannot compare different packet types", [("", "N/A", "N/A")]

        if meta1.getPacketName() != meta2.getPacketName():
            return "Cannot compare different packet types", [("", "N/A", "N/A")]
        xor = [a^b for a, b in zip(seq1, seq2)]
        if max(xor) == 0:
            return "{0} ==> (No change)".format(meta1.getPacketName()), []

        array = []

        for item in meta1.allItems():
            dec = self.__getTypeDecoder(item)
            params = item.extractParams()
            start, end = dec.getstartendbyte()
            if dec.isNonzero(xor):
                key = item.extract('name')
                try:
                    newvalue = dec.returnValue(seq1)
                    oldvalue = dec.returnValue(seq2)
                except:
                    newvalue = oldvalue = "CORRUPTED"
                array.append((key, newvalue, oldvalue))

        return meta1.getPacketName(), array

    def getMetaData(self, packet):
        raise RuntimeError('Abstract method, must be overloaded!')

class XProtocolDecoder(IDecoder):
    def getMetaData(self, seq):
        assert(len(seq) >= 2)
        if(seq[0] != 0xFF):
            raise IndexError("Start of block is not 0xFF!!")
            #return self.repo.getMetaObject(None)
        return self.repo.getMetaObject(seq[1])
        
