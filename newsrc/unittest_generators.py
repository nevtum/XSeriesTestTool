'''
Created on Feb 19, 2011

@author: nevster
'''
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
        a = iter('12345678')
        b = charpacket(a, size = 2)
        self.assertEquals('12', b.next())
        self.assertEquals('34', b.next())
        c = charpacket(a, size = 3)
        self.assertEquals('567', c.next())
        d = charpacket(a)
        self.assertEquals('8', a.next())
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