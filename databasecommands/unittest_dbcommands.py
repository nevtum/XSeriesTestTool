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
        self.assertEquals(0x00, cmd.item(0))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()