'''
Created on 30/04/2011

@author: ntummon
'''
import unittest
from generators import CommandDispatcher

class MockReciever:
    def __init__(self):
        self.ischanged = False
    def set(self):
        self.ischanged = True
    def data(self):
        return self.ischanged

class MockCommand:
    def __init__(self, receiver):
        self.reciever = receiver
    def execute(self):
        self.reciever.set()

class Test(unittest.TestCase):
    def setUp(self):
        self.CmdDisp = CommandDispatcher()
        self.CmdDisp.start()

    def testName(self):
        reciever = MockReciever()
        cmd = MockCommand(reciever)
        self.CmdDisp.put(cmd)
        self.assertEquals(True, reciever.data())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()