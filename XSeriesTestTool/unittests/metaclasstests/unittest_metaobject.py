import unittest
from config.metaclasses import codecMetaObject
from cStringIO import StringIO
from xml.etree import cElementTree

class Test(unittest.TestCase):
    
    def setUp(self):
        file = StringIO('''
        <packet name="sdb" length="128" pattern='00'>
            <item name="version" type="integer-reverse">
                <startbyte>3</startbyte>
                <endbyte>4</endbyte>
            </item>
            <item name="gmid" type="integer-reverse">
                <startbyte>6</startbyte>
                <endbyte>8</endbyte>
            </item>
            <item name="gamecycle" type="boolean">
                <byte>9</byte>
                <bit>1</bit>
            </item>
        </packet>''')
        self.root = cElementTree.ElementTree()
        self.root.parse(file)
    
    def testEssentialMethods(self):
        cmo = codecMetaObject(self.root.getroot())
        self.assertEquals(128, cmo.getPacketLength())
        self.assertEquals('sdb', cmo.getPacketName())
        self.assertEquals('00', cmo.getPacketPattern())
    
    def testiterator(self):
        cmo = codecMetaObject(self.root.getroot())
        generator = cmo.allItems()
        item = generator.next()
        self.assertEquals('version', item.extract('name'))
        self.assertEquals('integer-reverse', item.extract('type'))
        result = {'startbyte': '3', 'endbyte': '4'}
        self.assertEquals(result, item.extractParams())
        item = generator.next()
        self.assertEquals('gmid', item.extract('name'))
        self.assertEquals('integer-reverse', item.extract('type'))
        result = {'startbyte': '6', 'endbyte': '8'}
        self.assertEquals(result, item.extractParams())
        item = generator.next()
        self.assertEquals('gamecycle', item.extract('name'))
        self.assertEquals('boolean', item.extract('type'))
        result = {'byte': '9', 'bit': '1'}
        self.assertEquals(result, item.extractParams())
        self.assertEquals(None, item.extract('unicode'))
        self.assertRaises(StopIteration, generator.next)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()