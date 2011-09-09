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
            name, type = self.extract('name', item), self.extract('type', item)
            params = self.extractParams(item)
            self.decode(name, type, params)
            
    def decode(self, name, type, params):
        #delegate to type class
        #use polymorphism
        print type, name, params # temporary
            
    def extractParams(self, item):
        d = {}
        for params in list(item):
            d[params.tag] = params.text
        return d
            
    def extract(self, key, item):
        return item.attrib[key]
        
XDecoder = decoder()
XDecoder.createXMLPacket()