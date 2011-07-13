from forwarder import forwarder
from receiver import receiver
import time

x = receiver()
x.start()
f = forwarder()
f.transmitMsg(u'FF00020100563412')
time.sleep(0.1)
msg = x.receiveMsg()
print 'received: %s' % msg
f.transmitMsg(u'Hello there')
time.sleep(0.1)
msg = x.receiveMsg()
print 'received: %s' % msg
x.join()