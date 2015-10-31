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