'''
Created on 17/06/2011

@author: nEVSTER
'''
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        f = open('sdbmockdata.txt', 'r')
        data1 = f.readline().split()

    def tearDown(self):
        pass
    
    def testName(self):
        self.assertEquals(0x1234, cmd.convert(['12', '34']))
        self.assertEquals(0x)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()