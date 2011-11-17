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