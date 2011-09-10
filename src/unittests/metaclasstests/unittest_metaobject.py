'''
Created on 31/08/2011

@author: ntummon
'''
import unittest
from config.metaclasses import codecMetaObject
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
        
    def testiterator(self):
        cmo = codecMetaObject(self.file)
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