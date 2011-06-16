from datablockmodels import *
from sdbviews import *
from generators import *

file = open('SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t') # filter out given characters
b = charpacket(a, size = 2) # number of characters to extract from stream
c = datablockdispatcher(b) # extract only standard XSeries Packets
d = datablockfilter(c, '00', '22') # select packets that match packet IDs
e = diffpacketfilter(d) # only filter packets that have changed state

sdbhandle = sdbMdl() # Model
view = sdbreporter(sdbhandle) # View

mdbhandle = mdbMdl() # Model
view2 = mdbreporter(mdbhandle) # View

queue = CommandDispatcher()
queue.start()
packetswitch = packetswitch(queue)
packetswitch.registermodelinstance('00', sdbhandle)
packetswitch.registermodelinstance('22', mdbhandle)
packetswitch.setstream(e)
packetswitch.start()
