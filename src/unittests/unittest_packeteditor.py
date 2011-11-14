'''
Created on Nov 14, 2011

@author: nEVSTER
'''
import unittest
from dsl.packeteditor import PacketEditor

class Test(unittest.TestCase):

    def setUp(self):
        self.pe = PacketEditor()

    def testMakePacket(self):
        packet1 = self.pe.makeEmptyPacket(5)
        packet2 = self.pe.makeEmptyPacket(3)
        self.assertEquals(5, len(packet1))
        self.assertEquals(3, len(packet2))
        for elem in packet2:
            self.assertEquals('00', elem)
    
    def testPutX(self):
        pass
    
    def testBitToggle(self):
        pass
    
    def testCopyPaste(self):
        pass
    
    def testCRC(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()