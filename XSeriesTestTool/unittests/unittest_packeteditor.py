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
        for elem in packet1:
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
        # test boundaries
        test1 = self.pe.makeEmptyPacket(5)
        self.pe.putAscii(test1, 'test', 0, 3)
        self.assertEquals(['0x74', '0x65', '0x73', '0x74', '0x0'], test1)
        
        test2 = self.pe.makeEmptyPacket(5)
        self.pe.putAscii(test2, 'test', 0, 4)
        self.assertEquals(['0x74', '0x65', '0x73', '0x74', '0x0'], test2)
        
        test3 = self.pe.makeEmptyPacket(5)
        self.pe.putAscii(test3, 'test', 3, 4)
        self.assertEquals(['0x0', '0x0', '0x0', '0x74', '0x65'], test3)
        
        test4 = self.pe.makeEmptyPacket(2)
        self.assertRaises(AssertionError, self.pe.putAscii, test4, 'largestring', 2, 4)
        self.assertRaises(AssertionError, self.pe.putAscii, test4, 'largestring', -1, 1)
        self.pe.putAscii(test4, 'largestring', 0, 1)
        self.assertEquals(['0x6c', '0x61'], test4)
        
        # test reverse cases
        test5 = self.pe.makeEmptyPacket(5)
        self.pe.putAscii(test5, 'abc', 4, 0)
        self.assertEqual(['0x0', '0x0', '0x63', '0x62', '0x61'], test5)
        
        test6 = self.pe.makeEmptyPacket(3)
        self.pe.putAscii(test6, 'abc', 1, 0)
        self.assertEqual(['0x62', '0x61', '0x0'], test6)
        
        # test one character
        test7 = self.pe.makeEmptyPacket(4)
        self.pe.putAscii(test7, 'abc', 2, 2)
        self.assertEqual(['0x0', '0x0', '0x61', '0x0'], test7)
        
    def testBitToggle(self):
        pass
    
    def testCopyPaste(self):
        pass
    
    def testCRC(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()