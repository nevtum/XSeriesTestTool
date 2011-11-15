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
            self.assertEquals('0x0', elem)
    
    def testClone(self):
        pass
    
    def testPutHex(self):
        packet = self.pe.makeEmptyPacket(4)
        self.assertRaises(ValueError, self.pe.putHex, packet, 4, 0xff1234)
        self.assertRaises(ValueError, self.pe.putHex, packet, 3, -12)
        self.assertRaises(ValueError, self.pe.putHex, packet, 3, 'not valid')
        self.assertRaises(IndexError, self.pe.putHex, packet, 5, 0x01)
        self.pe.putHex(packet, 0, 0x30)
        self.pe.putHex(packet, 1, 0xab)
        self.assertEquals(packet[0], '0x30')
        self.assertEquals(packet[1], '0xab')
        
    def testPutAscii(self):
        test1 = self.pe.makeEmptyPacket(5)
        self.pe.putAscii(test1, 'test', 0, 3)
        result = ['0x74', '0x65', '0x73', '0x74', '0x0']
        self.assertEquals(result, test1)
        
        test2 = self.pe.makeEmptyPacket(5)
        self.pe.putAscii(test2, 'test', 0, 4)
        self.assertEquals(result, test2)
        
        test3 = self.pe.makeEmptyPacket(5)
        self.pe.putAscii(test3, 'test', 3, 4)
        result = ['0x0', '0x0', '0x0', '0x74', '0x65']
        self.assertEquals(result, test3)
        
    def testBitToggle(self):
        pass
    
    def testCopyPaste(self):
        pass
    
    def testCRC(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()