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

def charfilter(fileobj, *invalids):
    for char in fileobj.read():
        if char not in invalids:
            yield char

def xpacketextractor(streamgenerator):
    hexptr = streamgenerator
    dict = {0x00: 126, 0x22: 126, 0xA3: 15,
            0x70: 22, 0x71: 34}
    while True:
        BUFFER = bytearray()
        BUFFER.append(hexptr.next())
        BUFFER.append(hexptr.next())
        assert(BUFFER[0] == 0xFF)
        for i in range(dict.get(BUFFER[1])):
            BUFFER.append(hexptr.next())
        #yield ''.join(["%02X" % x for x in BUFFER]) # temporary fix
        yield [x for x in BUFFER]
        
def charpacket(astream, size = 1):
    while True:
        x = ''
        while len(x) < size:
            x += astream.next()
        yield int(x, 16)
    
# to remove once all functions been moved over to packetextractor
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
        
def diffpacketfilter(listgenerator):
    duplicates = {}
    for packet in listgenerator:
        if packet != duplicates.get(packet[1]):
            yield packet
        duplicates[packet[1]] = packet