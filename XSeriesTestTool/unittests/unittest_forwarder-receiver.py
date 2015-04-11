"""
XSeriesTestTool - A NSW gaming protocol decoder/analyzer
    Copyright (C) 2012  Neville Tummon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest
from comms.peer import *
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