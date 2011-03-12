from datablockmodels import *

def charfilter(fileobj, *invalids):
    for char in fileobj.read():
        if char not in invalids:
            yield char
        
def charpacket(astream, size = 1):
    while True:
        x = ''
        while len(x) < size:
            x += astream.next()
        yield x

def datablockdispatcher(streamgenerator):
# INPUT: stream
# OUTPUT: array of packets
    hexptr = streamgenerator
    dict = {'00': 126, '22': 126, 'A3': 15,
            '70': 22, '71': 34}
    while True:
        BUFFER = [hexptr.next(), hexptr.next()]
        assert(BUFFER[0] == 'FF')
        for i in range(dict.get(BUFFER[1])):
            BUFFER.append(hexptr.next())
        yield BUFFER

def datablockfilter(streamgenerator, *match):
    for BUFFER in streamgenerator:
        if BUFFER[1] in match:
            yield BUFFER

def txtreporter(listgenerator):
# INPUT: array
# OUTPUT: stream formatted for display
# NOT COMPLETE.. STILL BUGGY!
    for packet in listgenerator:
        packetsize = len(packet)
        packet[-1] = '%s\n\n' % packet[-1]
        g = []
        for i in range(packetsize / 9):
            g.append('.'.join(packet[10*i:10*(i+1)]))

        for i in range(packetsize / 9):
            if (i % 2) == 0:
                g[i] = '%s\t' % g[i]
            else:
                g[i] = '%s\n' % g[i]
    
        yield ''.join(g)
        
def diffpacketfilter(listgenerator):
    duplicates = {}
    for packet in listgenerator:
        if packet != duplicates.get(packet[1]):
            yield packet
        duplicates[packet[1]] = packet

class packetswitch:
    def __init__(self):
        self.handle = {}
        
    def registermodelinstance(self, key, packetmodel):
        assert (isinstance(packetmodel, packetmdl))
        self.handle[key] = packetmodel #insert sdbMdl, mdbMdl
        
    def setstream(self, stream):
        self.stream = stream
        
    def run(self):
        for each in self.stream:
            self.dispatch(each)
    
    def dispatch(self, packet):
        assert(isinstance(packet, list))
        handle = self.handle.get(packet[1])
        if handle is not None:
            handle.setdata(packet)