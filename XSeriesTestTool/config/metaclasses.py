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

from xml.etree import ElementTree as cElementTree

# This class contains the information of
# how all the elements inside a packet.
class itemElemWrapper:
    def __init__(self, elem):
        self.elem = elem

    def extractParams(self):
        d = {}
        for params in list(self.elem):
            d[params.tag] = params.text
        return d

    def extract(self, key):
        return self.elem.attrib.get(key)

# This object describes all the essential information
# required about the type of packet being received
class codecMetaObject:
    def __init__(self, root):
        assert(cElementTree.iselement(root))
        self.root = root
        
    def getPacketName(self):
        return self.root.attrib['name']
    
    def getPacketLength(self):
        return int(self.root.attrib['length'])
    
    def getPacketPattern(self):
        return self.root.attrib['pattern']
        
    def allItems(self):
        for elem in self.root.findall(".//item"):
            yield itemElemWrapper(elem)

class NullMetaObject:
    def getPacketName(self):
        return "unknown"
    
    def getPacketLength(self):
        raise ValueError("N/A. Unknown packet!")
        
    def allItems(self):
        return []