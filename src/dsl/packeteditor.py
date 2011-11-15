'''
Created on Nov 14, 2011

@author: nEVSTER
'''

class PacketEditor(object):
    def makeEmptyPacket(self, size):
        return [hex(0)]*size
        
    def putHex(self, packet, position, iVal):
        if not (0x0 <= iVal <= 0xff):
            raise ValueError
        packet[position] = hex(iVal)
        
    def putAscii(self, packet, string, startpos, endpos):
        x = [hex(ord(i)) for i in list(string)]
        for index in xrange(startpos, endpos+1):
            packet[startpos+index] = x[index]