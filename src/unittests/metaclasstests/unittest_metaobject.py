"""
XSeriesTestTool - A NSW gaming protocol decoder/analyzer
    Copyright (C) 2012  Neville Tummon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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