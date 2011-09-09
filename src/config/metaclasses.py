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
        return self.elem.attrib[key]

class codecMetaObject:
    def __init__(self, filepath):
        self.tree = cElementTree.ElementTree()
        self.tree.parse(filepath)
        self.p = None
        self.storeIntoDictionary()
        
    def storeIntoDictionary(self):
        self.dict = {}
        elems = self.tree.findall(".//item")
        for each in elems:
            self.dict[each.attrib['name']] = each
            
    def nextItem(self):
        for elem in self.tree.findall(".//item"):
            yield itemElemWrapper(elem)
    
    # returns xml element object
    def getitem(self, key):
        assert(isinstance(type, str))
        return self.dict.get(key)
        
    def getPacketName(self):
        return self.tree.getroot().attrib['name']
    
    def getPacketLength(self):
        return int(self.tree.getroot().attrib['length'])
    
    def getallmetaitems(self):
        if self.p == None:
            self.p = self.tree.findall(".//item")
        return self.p
    
    def getMetaItemsByType(self, type):
        assert(isinstance(type, str))
        result = self.tree.findall(".//item[@type='%s']" % type)
        if result == []:
            raise IndexError('No items found!')
        return result
