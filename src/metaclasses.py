'''
Created on 31/08/2011

@author: ntummon
'''

from xml.etree import cElementTree

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
    
    # returns xml element object
    def getitem(self, key):
        return self.dict.get(key)
        
    def getallmetaitems(self):
        if self.p == None:
            self.p = self.tree.findall(".//item")
        return self.p

md = codecMetaObject("packetdef.xml")
p = md.getallmetaitems()
for item in p:
    type = item.attrib['type']
    if type == 'integer-reverse':
        print "processing '%s' as reverse order integer" % item.attrib['name']
        x = item.find('byte')
        if x is not None:
            print "... @ byte %s" % x.text
        else:
            start, end = item.find('startbyte').text, item.find('endbyte').text
            print "... @ bytes %s - %s" % (start, end)
    if type == 'boolean':
        name = item.attrib['name']
        print "processing '%s' as boolean" % name
        byte, bit = item.find('byte').text, item.find('bit').text
        print "... @ byte: %s, bit: %s" % (byte, bit)

elem = md.getitem('cancelcrediterror')
print elem.find('byte').text
print elem.find('bit').text
