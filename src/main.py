from datablockmodels import *
from sdbviews import *
from generators import *

file = open('SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t')
b = charpacket(a, size = 2)
c = datablockdispatcher(b)
d = datablockfilter(c, '00', '22')
e = diffpacketfilter(d)

sdbhandle = sdbMdl() # Model
view = sdbreporter(sdbhandle) # View

queue = CommandDispatcher()
queue.start()
packetswitch = packetswitch(queue)
packetswitch.registermodelinstance('00', sdbhandle)
packetswitch.registermodelinstance('22', mdbMdl())
packetswitch.setstream(e)
packetswitch.start()
