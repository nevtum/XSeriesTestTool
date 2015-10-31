from generators import *
from decoder import *

xmetadata = metaRepository('../settings/')

file = open('SDB.MDB.Raw.Data.txt', 'r')
a = charfilter(file, '.', ' ', '\n', '\r', '\t') # filter out given characters
b = charpacket(a, size = 2) # number of characters to extract from stream
#c = datablockdispatcher(b) # extract only standard XSeries Packets
#d = datablockfilter(c, '00', '22') # select packets that match packet IDs
x = xpacketextractor(b)
   
xdec = XProtocolDecoder(xmetadata)
xdec.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
xdec.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
xdec.registerTypeDecoder('boolean', booleanDecoder)
xdec.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)


for packet in x:
    print xdec.createXMLPacket(packet)