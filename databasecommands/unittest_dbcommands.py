'''
Created on 17/06/2011

@author: nEVSTER
'''
import unittest
from dbcommands import *


class Test(unittest.TestCase):
    def setUp(self):
        f = open('sdbmockdata.txt', 'r')
        self.data = f.readline().split()

    def tearDown(self):
        pass
    
    def testName(self):
        cmd = insertToDBCommand(self.data)
        self.assertEquals(0x1234, cmd.convert(['12', '34']))
        self.assertEquals(0xabcd12, cmd.convert(['ab', 'cd', '12']))
        self.assertEquals(0xff, cmd.item(0))
        self.assertEquals(0x00, cmd.item(1))
        self.assertEquals(0x0101, cmd.item(2))
        self.assertEquals(0x563412, cmd.item(3))
        self.assertEquals(0x15, cmd.item(4))
        self.assertEquals(0x55, cmd.item(5))
        self.assertEquals(0x55, cmd.item(6))
        self.assertEquals(0x55, cmd.item(7))
        self.assertEquals(0x01, cmd.item(8))
        self.assertEquals(0x00, cmd.item(9))
        self.assertEquals(0x00, cmd.item(10))
        self.assertEquals(0x0527010000, cmd.item(11))
        self.assertEquals(0x9078563412, cmd.item(12))
        self.assertEquals(0x4025200000, cmd.item(13))
        self.assertEquals(0x9078563412, cmd.item(14))
        self.assertEquals(0x0099999999, cmd.item(15))
        self.assertEquals(0x5561050000, cmd.item(16))
        self.assertEquals(0x2222222222, cmd.item(17))
        self.assertEquals(0x9078563412, cmd.item(18))
        self.assertEquals(0x2040600000, cmd.item(19))
        self.assertEquals(0x1111111111, cmd.item(20))
        self.assertEquals(0x0, cmd.item(21))
        self.assertEquals(0x55555555, cmd.item(22))
        self.assertEquals(0x84560000, cmd.item(23))
        self.assertEquals(0x77777777, cmd.item(24))
        self.assertEquals(0x3f, cmd.item(25))
        self.assertEquals(0x0100, cmd.item(26))
        self.assertEquals(0x3030373130304D47, cmd.item(27))
        self.assertEquals(0x2020202020202020, cmd.item(28))
        self.assertEquals(0x34303330304D4453, cmd.item(29))
        self.assertEquals(0x3630373030583253, cmd.item(30))
        self.assertEquals(0x9999, cmd.item(31))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()