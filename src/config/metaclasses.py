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
    def __init__(self, filepath):
        self.tree = cElementTree.ElementTree()
        self.tree.parse(filepath)
        
    def getPacketName(self):
        return self.tree.getroot().attrib['name']
    
    def getPacketLength(self):
        return int(self.tree.getroot().attrib['length'])
        
    def allItems(self):
        for elem in self.tree.findall(".//item"):
            yield itemElemWrapper(elem)
