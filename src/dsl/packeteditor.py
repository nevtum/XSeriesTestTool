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

class PacketEditor(object):
    def makeEmptyPacket(self, size):
        return [hex(0)]*size
        
    def putHex(self, packet, position, iVal):
        if not (0x0 <= iVal <= 0xff):
            raise ValueError
        packet[position] = hex(iVal)
        
    def putAscii(self, packet, string, startpos, endpos):
        assert(0 <= startpos <= len(packet))
        assert(0 <= endpos+1 <= len(packet))
        delta = endpos-startpos
        g = self.crop(string, abs(delta)+1)
        for index in range(len(g)):
            if delta >= 0:
                packet[startpos+index] = g[index]
            else:
                packet[startpos-index] = g[index]
            
    def crop(self, string, window):
        minsize = min(len(string), window)
        return [hex(ord(string[i])) for i in range(minsize)]