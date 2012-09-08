'''
Created on 31/08/2011

@author: ntummon
'''

from xml.etree import ElementTree as cElementTree

# This class contains the information of
# how all the elements inside a packet.
class itemElemWrapper:
    def __init__(self, elem):
        self.elem = elem

    def extractParams(self):
        d = {}
        for params in list(self.elem):
            d[params.tag] = params.text
        return d

    def extract(self, key):
        return self.elem.attrib.get(key)

# This object describes all the essential information
# required about the type of packet being received
class codecMetaObject:
    def __init__(self, root):
        assert(cElementTree.iselement(root))
        self.root = root
        
    def getPacketName(self):
        return self.root.attrib['name']
    
    def getPacketLength(self):
        return int(self.root.attrib['length'])
    
    def getPacketPattern(self):
        return self.root.attrib['pattern']
        
    def allItems(self):
        for elem in self.root.findall(".//item"):
            yield itemElemWrapper(elem)

class NullMetaObject:
    def getPacketName(self):
        return "unknown"
    
    def getPacketLength(self):
        raise ValueError("N/A. Unknown packet!")
        
    def allItems(self):
        return []