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
from generators import *
from cStringIO import StringIO

class Test(unittest.TestCase):
    def testunfilteredcharstream(self):
        string = ''
        file = StringIO('a.b c, d$e')
        a = charfilter(file)
        for i in range(10):
            string += a.next()
        self.assertEquals('a.b c, d$e', string)
        self.assertRaises(StopIteration, a.next)
        
    def testfilteredcharstream(self):
        string = ''
        file = StringIO('!a.b c$d*e')
        invalid_chars =  ('.', ' ', '$', '*', '!')
        a = charfilter(file, *invalid_chars)
        for i in range(5):
            string += a.next()
        self.assertEquals('abcde', string)
        self.assertRaises(StopIteration, a.next)
        
    def testcharpacket(self):
        a = iter(b'12345678')
        b = charpacket(a, size = 2)
        self.assertEquals(0x12, b.next())
        self.assertEquals(0x34, b.next())
        c = charpacket(a, size = 3)
        self.assertEquals(0x567, c.next())
        d = charpacket(a)
        self.assertEquals(0x8, d.next())
        self.assertRaises(StopIteration, d.next)
        
    def testdiffpacketfilter(self):
        a = [['FF', '00', '20']]
        a.append(['FF', '00', '20'])
        a.append(['FF', '00', '21'])
        x = diffpacketfilter(a)
        self.assertEquals(a[0], x.next())
        self.assertEquals(a[2], x.next())
        self.assertRaises(StopIteration, x.next)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()