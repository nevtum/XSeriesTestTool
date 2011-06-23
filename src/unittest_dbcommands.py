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
        self.cmd = insertToDBCommand(self.data, None)

    def test_conversion(self):
        cmd = self.cmd
        self.assertEquals(0x1234, cmd.convert(['12', '34']))
        self.assertEquals(0xabcd12, cmd.convert(['ab', 'cd', '12']))
        
    def test_all_items(self):
        cmd = self.cmd
        self.assertEquals(0x00, cmd.get('ID'))
        self.assertEquals(0x0101, cmd.get('VersionNr'))
        self.assertEquals(0x563412, cmd.get('GMID'))
        self.assertEquals(0x15, cmd.get('StatusByte1'))
        self.assertEquals(0x55, cmd.get('StatusByte2'))
        self.assertEquals(0x55, cmd.get('StatusByte3'))
        self.assertEquals(0x55, cmd.get('StatusByte4'))
        self.assertEquals(0x01, cmd.get('StatusByte5'))
        self.assertEquals(0x00, cmd.get('MultiGameNumber'))
        self.assertEquals(0x00, cmd.get('MultiGameCombNumber'))
        self.assertEquals(0x0527010000, cmd.get('Turnover'))
        self.assertEquals(0x9078563412, cmd.get('TotalWins'))
        self.assertEquals(0x4025200000, cmd.get('CashBox'))
        self.assertEquals(0x9078563412, cmd.get('CancelledCredits'))
        self.assertEquals(0x0099999999, cmd.get('GamesPlayed'))
        self.assertEquals(0x5561050000, cmd.get('MoneyIn'))
        self.assertEquals(0x2222222222, cmd.get('MoneyOut'))
        self.assertEquals(0x9078563412, cmd.get('CashIn'))
        self.assertEquals(0x2040600000, cmd.get('CashOut'))
        self.assertEquals(0x1111111111, cmd.get('CurrentCredits'))
        self.assertEquals(0x0, cmd.get('MiscAccrual'))
        self.assertEquals(0x55555555, cmd.get('NrPowerUps'))
        self.assertEquals(0x84560000, cmd.get('GamesSinceLastPowerUp'))
        self.assertEquals(0x77777777, cmd.get('GamesSinceLastDoorOpen'))
        self.assertEquals(0x3f, cmd.get('PortStatusByte'))
        self.assertEquals(0x0100, cmd.get('BaseCreditValue'))
        self.assertEquals(0x3030373130304D47, cmd.get('programID1'))
        self.assertEquals(0x2020202020202020, cmd.get('programID2'))
        self.assertEquals(0x34303330304D4453, cmd.get('programID3'))
        self.assertEquals(0x3630373030583253, cmd.get('programID4'))
        self.assertEquals(0x9999, cmd.get('PRTP'))
        self.assertEquals(0x01, cmd.get('SecondaryFunctions'))
        
    def test_index_out_of_bound(self):
        cmd = self.cmd
        self.assertRaises(KeyError, cmd.get, 33)
        self.assertRaises(KeyError, cmd.get, 'UnknownKey')
        self.assertRaises(KeyError, cmd.get, '!@#$%^&*(ad124')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()