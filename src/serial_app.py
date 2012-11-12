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

import serial

class SerialModule:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout = 1)
        
    def Rx(self):
        data = self.ser.read(1)
        remainder = self.ser.inWaiting()
        data2 = self.ser.read(remainder)
        seq = [x for x in bytearray(data + data2)] # unmarshal data
        if len(seq) > 0:
            return seq
    
    def Tx(self, seq):
        assert(isinstance(seq, list))
        for byte in seq:
            assert(0 <= byte <= 255)
        self.ser.write(bytearray(seq)) # marshal data and write
        
    def __del__(self):
        self.ser.close()

    def close(self):
        self.ser.close()
