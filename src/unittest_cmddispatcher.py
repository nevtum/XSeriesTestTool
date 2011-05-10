'''
Created on 30/04/2011

@author: ntummon
'''
import time
import unittest
from generators import CommandDispatcher

class MockReciever:
    def __init__(self):
        self.ischanged = False
    def set(self):
        print "setting internal data of MockReciever..."
        self.ischanged = True
    def reset(self):
        print "resetting internal data of MockReciever..."
        self.ischanged = False
    def data(self):
        return self.ischanged

class MockCommandSet:
    def __init__(self, receiver):
        self.reciever = receiver
    def execute(self):
        self.reciever.set()
        
class MockCommandReset:
    def __init__(self, receiver):
        self.reciever = receiver
    def execute(self):
        self.reciever.reset()

class Test(unittest.TestCase):
    def setUp(self):
        self.CmdDisp = CommandDispatcher()
        self.CmdDisp.start()
        #time.sleep(0.2)

    def testName(self):
        rx = MockReciever()
        cmd = MockCommandSet(rx)
        self.CmdDisp.put(cmd)
        #time.sleep(0.2)
        self.assertEquals(True, rx.data())
        cmd = MockCommandReset(rx)
        self.CmdDisp.put(cmd)
        #time.sleep(0.2)
        self.assertEquals(False, rx.data())
    
    def testKill(self):
        rx = MockReciever()
        cmd = MockCommandSet(rx)
        self.CmdDisp.kill()
        #time.sleep(0.2)
        self.assertRaises(ValueError, self.CmdDisp.put, cmd)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()