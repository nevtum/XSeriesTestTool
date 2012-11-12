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

import os
from xml.etree import cElementTree
from config.metaclasses import *

# This repository is a dictionary of all meta objects.
# All knowledge of every type of packet can be found
# in the meta repository
class metaRepository:
    def __init__(self, filepath):
        self.filepath = filepath
        self.collection = {}
        self.__createRepository()
        
    def __createRepository(self):
        dupes = set()
        for cmo in self.__allMetaObjects():
            t = cmo.getPacketName(), cmo.getPacketLength(), cmo.getPacketPattern()
            if t in dupes:
                raise IndexError('Duplicate metadata!!')
            dupes.add(t)
            self.collection[int(cmo.getPacketPattern(), 16)] = cmo
        if (len(self.collection) == 0):
            raise ValueError('No metadata found!!')
            
    def __allMetaObjects(self):
        for root, dirs, files in os.walk(self.filepath):
            for file in files:
                pathname = os.path.join(root, file)
                if 'xml' in pathname:
                    tree = cElementTree.ElementTree()
                    tree.parse(pathname)
                    for each in tree.findall('.//packet'):
                        yield codecMetaObject(each)
                        
    def getMetaObject(self, key):
        obj = self.collection.get(key)
        if(obj is None):
            return NullMetaObject()
        return obj