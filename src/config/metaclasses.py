'''
Created on 31/08/2011

@author: ntummon
'''

from xml.etree import cElementTree

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
