'''
Created on Nov 14, 2011

@author: nEVSTER
'''

class PacketEditor(object):
    def makeEmptyPacket(self, size):
        return ['00']*size
        