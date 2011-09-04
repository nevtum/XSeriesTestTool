'''
Created on 31/08/2011

@author: ntummon
'''
import unittest
from metaclasses import codecMetaObject
from cStringIO import StringIO

class Test(unittest.TestCase):
    
    def setUp(self):
        self.file = StringIO('''
        <packet name="sdb" length="128">
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
        
    def testsampleitems(self):
        cmo = codecMetaObject(self.file)
        elems = cmo.getallmetaitems()
        self.assertEquals(3, len(elems))
        self.assertEquals('version', elems[0].attrib['name'])
        self.assertEquals('integer-reverse', elems[0].attrib['type'])
        self.assertEquals('gmid', elems[1].attrib['name'])
        self.assertEquals('integer-reverse', elems[1].attrib['type'])
        self.assertEquals('gamecycle', elems[2].attrib['name'])
        self.assertEquals('boolean', elems[2].attrib['type'])
        
    def testpacketinfo(self):
        cmo = codecMetaObject(self.file)
        self.assertEquals('sdb', cmo.getPacketName())
        self.assertEquals(128, cmo.getPacketLength())
        
    def testmethods(self):
        cmo = codecMetaObject(self.file)
        intelems = cmo.getMetaItemsByType('integer-reverse')
        self.assertEquals(2, len(intelems))
        self.assertEquals('version', intelems[0].attrib['name'])
        self.assertEquals('gmid', intelems[1].attrib['name'])
        boolelems = cmo.getMetaItemsByType('boolean')
        self.assertEquals(1, len(boolelems))
        self.assertEquals('gamecycle', boolelems[0].attrib['name'])
        
    def testInvalidParams(self):
        cmo = codecMetaObject(self.file)
        self.assertRaises(IndexError, cmo.getMetaItemsByType, 'blurb')
        self.assertRaises(IndexError, cmo.getMetaItemsByType, '')
        self.assertRaises(AssertionError, cmo.getMetaItemsByType, [])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()