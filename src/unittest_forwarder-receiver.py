import unittest
import socket
from forwarder import forwarder
from receiver import receiver
from peer import *
import time

class TestRepeater(unittest.TestCase):
    def setUp(self):
        self.repeat = repeater(12345)
        self.repeat.setforwarder('localhost', 33333)
        self.source = peer(33333)
        self.source.setforwarder('localhost', 12345)
        self.source.start()
        self.repeat.start()

    def testitems(self):
        self.source.sendMsg('hello there')
        time.sleep(3) # try refactoring to take no delay
        self.assertEquals('hello there', self.source.getMsg())
        self.source.sendMsg('FF001122334455')
        time.sleep(3) # try refactoring to take no delay
        self.assertEquals('FF001122334455', self.source.getMsg())