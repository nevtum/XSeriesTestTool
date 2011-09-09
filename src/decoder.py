from config.metaclasses import codecMetaObject

class decoder(object):
    def getMeta(self, name):
        return codecMetaObject('packetdef.xml')

    def setpacket(self, packet):
        self.packet = packet

    def createXMLPacket(self):
        # if sdb packet
        metaobj = self.getMeta('sdb') # need more parameters
        for item in metaobj.nextItem():
            name = item.extract('name')
            type = item.extract('type')
            params = item.extractParams()
            self.decode(name, type, params)

    def decode(self, name, type, params):
        #delegate to type class
        #use polymorphism
        print type, name, params # temporary

XDecoder = decoder()
XDecoder.createXMLPacket()