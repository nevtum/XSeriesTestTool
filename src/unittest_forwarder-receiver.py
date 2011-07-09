from forwarder import forwarder
from receiver import receiver

x = receiver()
msg = x.receiveMsg() # currently blocking
print 'received: %s' % msg
f = forwarder()
f.transmitMsg(u'FF00020100563412')